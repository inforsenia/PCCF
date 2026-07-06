#!/usr/bin/env python3

"""
Sondeja plantilles_{FAMILIA}_{CICLO}/ ja sincronitzades (OneDrive) i, per a
cada cicle, regenera SEMPRE el report (barat: regex + openpyxl, sense
LaTeX) quan detecta un canvi de mtime. Només compila i publica els PDFs
(car: pandoc + xelatex) quan l'estat "verificat" (sense incidències
pendents) canvia respecte de l'última vegada -- sense cap fitxer disparador
ni acció manual del docent/cap de departament.

Diferència amb tools/local_sync_poller.py (memòries): ací cal un "bootstrap"
(generar-plantilles-pccf-{cicle}) abans que hi haja res per editar, perquè el
docent no parteix de zero (calen BORRADOR + Excel generats des del JSON del
BOE). Com que eixe pas ja és idempotent per disseny (mai sobreescriu feina
existent), es reexecuta a cada passada sense risc.

Ús:
    python3 tools/pccf_sync_poller.py --once   # una sola passada
    python3 tools/pccf_sync_poller.py          # bucle continu
"""

import argparse
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pccf_utils import CICLES_INF, CICLES_SCO, get_familia
from report_pccf import compute_status, format_report, is_verified

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CICLES_ALL = CICLES_INF + CICLES_SCO

# Estat intern del poller (últim mtime processat + últim booleà verificat per
# cicle). MAI dins la carpeta sincronitzada: és bookkeeping del poller, no
# contingut per als docents. Es perd sense risc si s'esborra (pitjor cas:
# una recompilació de més al següent cicle).
STATE_PATH = os.path.join(PROJECT_DIR, "temp", "pccf_poller_state.json")


def load_state():
    if not os.path.exists(STATE_PATH):
        return {}
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f)


def plantilles_dir(sync_root, familia, cicle):
    return os.path.join(sync_root, f"plantilles_{familia}_{cicle}")


def latest_source_mtime(pdir):
    mtimes = []
    if os.path.isdir(pdir):
        for f in os.listdir(pdir):
            if f.endswith(".md") or f.endswith(".xlsx"):
                mtimes.append(os.path.getmtime(os.path.join(pdir, f)))
    return max(mtimes) if mtimes else 0.0


def poll_once(sync_root, centre):
    processed = []
    state = load_state()

    for cicle in CICLES_ALL:
        familia = get_familia(cicle)
        key = f"{familia}_{cicle}"
        pdir = plantilles_dir(sync_root, familia, cicle)

        bootstrap = subprocess.run(
            ["make", f"PLANTILLES_ROOT={sync_root}", f"CENTRO_EDUCATIVO={centre}",
             f"generar-plantilles-pccf-{cicle.lower()}"],
            cwd=PROJECT_DIR, capture_output=True, text=True,
        )
        if bootstrap.returncode != 0:
            print(f"[pccf-poller] ERROR bootstrap {key}:\n{bootstrap.stdout[-2000:]}\n{bootstrap.stderr[-2000:]}", flush=True)
            continue

        source_mtime = latest_source_mtime(pdir)
        if source_mtime == 0.0:
            continue

        last_mtime = state.get(key, {}).get("mtime", 0.0)
        if source_mtime <= last_mtime:
            continue

        print(f"[pccf-poller] {key}: canvi detectat, regenerant report...", flush=True)
        status = compute_status(cicle, familia, pdir)
        verified = is_verified(status)

        report_dir = os.path.join(sync_root, "0_report_pccf")
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, f"{key}.txt"), "w", encoding="utf-8") as f:
            f.write(format_report(status))

        prev_verified = state.get(key, {}).get("verified")

        if verified == prev_verified:
            # Report ja regenerat i publicat: no queda cap operació que
            # puga fallar, es pot fixar l'estat ja mateix.
            state[key] = {"mtime": source_mtime, "verified": verified}
            save_state(state)
            print(f"[pccf-poller] {key}: estat verificat sense canvis ({verified}), no recompilo el PDF.", flush=True)
            processed.append(key)
            continue

        # NOTA: no es guarda l'estat fins que compilació+publicació ixen bé.
        # Si falla ací, la propera passada ho torna a intentar (encara que
        # el docent no haja tornat a editar res).
        print(f"[pccf-poller] {key}: estat verificat ha passat a {verified}, compilant...", flush=True)
        compile_result = subprocess.run(
            ["make", f"PLANTILLES_ROOT={sync_root}", f"CENTRO_EDUCATIVO={centre}",
             f"compila-pccf-{cicle.lower()}"],
            cwd=PROJECT_DIR, capture_output=True, text=True,
        )
        if compile_result.returncode != 0:
            print(f"[pccf-poller] ERROR compilant {key}:\n{compile_result.stdout[-3000:]}\n{compile_result.stderr[-3000:]}", flush=True)
            continue

        publish_result = subprocess.run(
            [sys.executable, os.path.join(PROJECT_DIR, "tools", "publish_pccf_output.py"),
             "--dest", sync_root, "--centre", centre, "--cicle", cicle],
            cwd=PROJECT_DIR, capture_output=True, text=True,
        )
        print(publish_result.stdout, flush=True)
        if publish_result.returncode != 0:
            print(f"[pccf-poller] ERROR publicant {key}: {publish_result.stderr[-2000:]}", flush=True)
            continue

        state[key] = {"mtime": source_mtime, "verified": verified}
        save_state(state)
        processed.append(key)

    return processed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Una sola passada (per a proves)")
    parser.add_argument("--sync-root", default=os.environ.get("PCCF_SYNC_ROOT", "/data/onedrive-pccf"))
    parser.add_argument("--centre", default=os.environ.get("CENTRO_EDUCATIVO", "IESEPM"))
    parser.add_argument("--interval", type=int, default=int(os.environ.get("POLLER_INTERVAL", "300")))
    args = parser.parse_args()

    while True:
        try:
            processed = poll_once(args.sync_root, args.centre)
            if not processed:
                print("[pccf-poller] cap canvi pendent.", flush=True)
        except Exception as e:
            print(f"[pccf-poller] ERROR inesperat: {e}", flush=True)
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
