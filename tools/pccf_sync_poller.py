#!/usr/bin/env python3

"""
Sondeja les carpetes sincronitzades OneDrive i, per a cada cicle, regenera
el report sempre que detecta un canvi (PCCF o PD). Compila automàticament
el PCCF PDF (pccf/src*/) pero NO les Programaciones (programacions/) --
això es fa manualment pel cap de departament (compila-pd-pccf-{cicle}).

Estructura esperada dins de sync-root:
  pccf/                    → PCCF framework (src*, src_{FAMILIA}*, src_{FAMILIA}_{CICLO}*)
  programacions/{CICLO}/  → PD_*.md + libro_{CICLO}.xlsx
  0_report_pccf/           → reports (auto)
  1_esborrany_pccf/        → PDFs (PCCF auto, PD manual)

Ús:
    python3 tools/pccf_sync_poller.py --once             # una sola passada
    python3 tools/pccf_sync_poller.py --once --cicle APD # només un cicle
    python3 tools/pccf_sync_poller.py                    # bucle continu
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


def pccf_tree_mtime(pccf_dir):
    """Últim mtime de qualsevol .md dins de pccf/src* recursivament."""
    mtimes = []
    if os.path.isdir(pccf_dir):
        for root, _dirs, files in os.walk(pccf_dir):
            for f in files:
                if f.endswith(".md"):
                    mtimes.append(os.path.getmtime(os.path.join(root, f)))
    return max(mtimes) if mtimes else 0.0


def latest_source_mtime(pdir):
    mtimes = []
    if os.path.isdir(pdir):
        for f in os.listdir(pdir):
            if f.endswith(".md") or f.endswith(".xlsx"):
                mtimes.append(os.path.getmtime(os.path.join(pdir, f)))
    return max(mtimes) if mtimes else 0.0


def poll_once(sync_root, centre, cicle=None):
    processed = []
    state = load_state()

    cicles_a_processar = [cicle] if cicle else CICLES_ALL
    for cicle in cicles_a_processar:
        familia = get_familia(cicle)
        key = f"{familia}_{cicle}"

        # Directoris dins del sync_root (OneDrive)
        pdir = os.path.join(sync_root, "programacions", cicle)
        pccf_dir = os.path.join(sync_root, "pccf")

        # Bootstrap (idempotent)
        bootstrap = subprocess.run(
            ["make", f"PCCF_ROOT={sync_root}", f"CENTRO_EDUCATIVO={centre}",
             f"generar-plantilles-pccf-{cicle.lower()}"],
            cwd=PROJECT_DIR, capture_output=True, text=True,
        )
        if bootstrap.returncode != 0:
            print(f"[pccf-poller] ERROR bootstrap {key}:\n{bootstrap.stdout[-2000:]}\n{bootstrap.stderr[-2000:]}", flush=True)
            continue

        # Comprovar mtimes per separat
        pd_mtime = latest_source_mtime(pdir)
        pccf_mtime = pccf_tree_mtime(pccf_dir)

        if pd_mtime == 0.0 and pccf_mtime == 0.0:
            continue

        last_pd_mtime = state.get(key, {}).get("mtime_pd", 0.0)
        last_pccf_mtime = state.get(key, {}).get("mtime_pccf", 0.0)

        pd_canviat = pd_mtime > last_pd_mtime
        pccf_canviat = pccf_mtime > last_pccf_mtime
        if not pd_canviat and not pccf_canviat:
            continue

        print(f"[pccf-poller] {key}: canvi {'PCCF' if pccf_canviat else ''}{' i ' if pd_canviat and pccf_canviat else ''}{'PD' if pd_canviat else ''} detectat, regenerant report...", flush=True)

        # Sempre regenerar report (tant si canvia PCCF com PD)
        status = compute_status(cicle, familia, pdir)
        verified = is_verified(status)
        report_dir = os.path.join(sync_root, "0_report_pccf")
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, f"{key}.txt"), "w", encoding="utf-8") as f:
            f.write(format_report(status))

        # Compilar PCCF només si els PCCF han canviat (sempre, no només si canvia verified)
        if pccf_canviat:
            print(f"[pccf-poller] {key}: compilant PCCF (pccf/src* ha canviat)...", flush=True)
            compile_result = subprocess.run(
                ["make", f"PCCF_ROOT={sync_root}", f"CENTRO_EDUCATIVO={centre}",
                 f"compila-pccf-{cicle.lower()}"],
                cwd=PROJECT_DIR, capture_output=True, text=True,
            )
            if compile_result.returncode != 0:
                print(f"[pccf-poller] ERROR compilant PCCF {key}:\n{compile_result.stdout[-3000:]}\n{compile_result.stderr[-3000:]}", flush=True)
                continue
            print(f"[pccf-poller] {key}: PCCF compilat correctament.", flush=True)

        # No compilar PD automàticament (manual: compila-pd-pccf-{cicle})

        state[key] = {"mtime_pccf": pccf_mtime, "mtime_pd": pd_mtime, "verified": verified}
        save_state(state)
        processed.append(key)

    return processed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Una sola passada (per a proves)")
    parser.add_argument("--sync-root", default=os.environ.get("PCCF_SYNC_ROOT", "/data/onedrive-pccf"),
                        help="Arrel de la carpeta sincronitzada (conté pccf/, programacions/, ...)")
    parser.add_argument("--cicle", help="Limitar a un sol cicle (ex: APD)")
    parser.add_argument("--centre", default=os.environ.get("CENTRO_EDUCATIVO", "IESEPM"))
    parser.add_argument("--interval", type=int, default=int(os.environ.get("POLLER_INTERVAL", "300")))
    args = parser.parse_args()

    if args.cicle and args.cicle.upper() not in CICLES_ALL:
        print(f"ERROR: cicle desconegut '{args.cicle}'. Valors vàlids: {', '.join(CICLES_ALL)}", file=sys.stderr)
        sys.exit(1)
    if args.cicle:
        args.cicle = args.cicle.upper()

    while True:
        try:
            processed = poll_once(args.sync_root, args.centre, args.cicle)
            if not processed:
                print("[pccf-poller] cap canvi pendent.", flush=True)
        except Exception as e:
            print(f"[pccf-poller] ERROR inesperat: {e}", flush=True)
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
