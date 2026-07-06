#!/usr/bin/env python3

"""
Sondeja les carpetes de departament ja sincronitzades (OneDrive) i, si
algun fitxer .md és més recent que l'últim report publicat, executa sol
compila-memories + publish_memories_output.py -- sense cap acció manual
ni fitxer disparador. Qualsevol canvi (edició d'un docent, fitxer nou)
regenera automàticament el report + PDF d'eixe departament.

Ús:
    python3 tools/local_sync_poller.py --once      # una sola passada
    python3 tools/local_sync_poller.py             # bucle continu
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memories_utils import PROJECT_DIR, check_placeholders, check_stats_consistency, get_teacher_email
from mailer import smtp_configured, send_report_email

# Estat intern del poller (últim mtime de cada .md ja avaluat per a
# notificació al docent). MAI dins la carpeta sincronitzada: és bookkeeping
# del poller, no contingut per als docents. Es perd sense risc si
# s'esborra (pitjor cas: es reavalua/reenvia un avís de més).
TEACHER_STATE_PATH = os.path.join(PROJECT_DIR, "temp", "memories_teacher_notify_state.json")

DEPARTMENTS = {
    "memoriaESOBAT": {
        "tipus": "ESOBAT",
        "sync_subpath": "General/Memòries ESO-BAT",
        "families": [
            "ANGLES", "BIOLOGIA_GEOLOGIA", "DIBUIX", "ECONOMIA",
            "EDUCACIO_FISICA", "FILOSOFIA", "FISICA_QUIMICA", "FRANCES",
            "GEOGRAFIA_HISTORIA", "INFORMATICA", "LLATI",
            "LLENGUA_CASTELLANA", "LLENGUA_VALENCIANA", "MATEMATIQUES",
            "MUSICA", "RELIGIO", "TECNOLOGIA",
        ],
    },
    "memoriaFP": {
        "tipus": "FP",
        "sync_subpath": "General/Memòries FP",
        "families": ["ANG", "FOL", "INF", "SCO"],
    },
}


def latest_source_mtime(dept_dir):
    mtimes = [
        os.path.getmtime(os.path.join(dept_dir, f))
        for f in os.listdir(dept_dir)
        if f.endswith(".md")
    ]
    return max(mtimes) if mtimes else 0.0


def latest_report_mtime(dept_root, tipus, familia):
    report_dir = os.path.join(dept_root, f"0_report_memories_{tipus}")
    matches = glob.glob(os.path.join(report_dir, f"{familia}_*.txt"))
    if not matches:
        return 0.0
    return max(os.path.getmtime(m) for m in matches)


def load_teacher_state():
    if not os.path.exists(TEACHER_STATE_PATH):
        return {}
    try:
        with open(TEACHER_STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_teacher_state(state):
    os.makedirs(os.path.dirname(TEACHER_STATE_PATH), exist_ok=True)
    with open(TEACHER_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f)


def format_deficiencies(remaining, stats_issues):
    parts = []
    custom_markers = {"[ZERO_STATS]", "[CHECKBOX_FORMAT]"}
    ph_count = len([r for r in remaining if r not in custom_markers])
    if ph_count:
        parts.append(f"{ph_count} marcadors pendents ([###]/[...] sense substituir)")
    if "[ZERO_STATS]" in remaining:
        parts.append("estadístiques amb 0 aprovats i 0 suspensos")
    if "[CHECKBOX_FORMAT]" in remaining:
        parts.append("caselles marcades amb format incorrecte (useu [x] sense espais)")
    parts.extend(stats_issues)
    return parts


def notify_teachers(base_dir, familia, tipus, dept_dir, is_esobat):
    """Avisa cada docent per correu de les deficiències de la seua pròpia
    memòria (no del report sencer del departament), si el seu fitxer .md
    conté una línia "correu-e: adreça" (vore memories_utils.get_teacher_email).

    No invasiu: sense SMTP configurat no fa absolutament res (ni tan sols
    llig l'estat). Un fitxer sense el camp "correu-e" o sense deficiències
    detectades tampoc genera cap enviament. Cada versió (mtime) d'un
    fitxer es processa com a màxim una vegada -- si l'enviament falla
    (SMTP caigut), l'estat no es guarda i es reintenta a la propera passada.
    """
    if not smtp_configured():
        return

    state = load_teacher_state()

    for fname in sorted(os.listdir(dept_dir)):
        if not fname.endswith(".md") or "safeBackup" in fname:
            continue
        filepath = os.path.join(dept_dir, fname)
        state_key = f"{base_dir}/{familia}/{fname}"
        mtime_before = os.path.getmtime(filepath)
        if mtime_before <= state.get(state_key, 0.0):
            continue

        to_addr = get_teacher_email(filepath)
        if not to_addr:
            state[state_key] = mtime_before
            save_teacher_state(state)
            continue

        # check_placeholders() pot reescriure el fitxer (auto-fix de
        # claudàtors) -- es captura el mtime final després de cridar-lo.
        remaining = check_placeholders(filepath)
        stats_issues = check_stats_consistency(filepath, is_esobat)
        deficiencies = format_deficiencies(remaining, stats_issues)
        mtime_final = os.path.getmtime(filepath)

        if not deficiencies:
            state[state_key] = mtime_final
            save_teacher_state(state)
            continue

        subject = f"[Memòries {tipus}] Incidències pendents - {fname}"
        body = (
            f"S'han detectat les següents incidències a la vostra memòria "
            f"({fname}, departament {familia}):\n\n"
            + "\n".join(f"- {d}" for d in deficiencies)
            + "\n\nReviseu i corregiu-les directament al fitxer.\n"
        )
        if send_report_email(to_addr, subject, body):
            print(f"    correu enviat al docent ({to_addr}) per {fname}", flush=True)
            state[state_key] = mtime_final
            save_teacher_state(state)


def poll_once(sync_root, centre):
    processed = []
    for base_dir, info in DEPARTMENTS.items():
        tipus = info["tipus"]
        dept_root = os.path.join(sync_root, info["sync_subpath"])
        if not os.path.isdir(dept_root):
            continue
        for familia in info["families"]:
            dept_dir = os.path.join(dept_root, familia)
            if not os.path.isdir(dept_dir):
                continue

            notify_teachers(base_dir, familia, tipus, dept_dir, tipus == "ESOBAT")

            source_mtime = latest_source_mtime(dept_dir)
            if source_mtime == 0.0:
                continue
            last_mtime = latest_report_mtime(dept_root, tipus, familia)
            if source_mtime <= last_mtime:
                continue

            print(f"[poller] {base_dir}/{familia}: canvi detectat, compilant...", flush=True)
            compile_result = subprocess.run(
                ["make", f"CENTRO_EDUCATIVO={centre}", f"BASE_DIR={base_dir}",
                 f"FAMILIA={familia}", "compila-memories"],
                cwd=PROJECT_DIR, capture_output=True, text=True,
            )
            if compile_result.returncode != 0:
                print(f"[poller] ERROR compilant {base_dir}/{familia}:\n{compile_result.stdout[-3000:]}\n{compile_result.stderr[-3000:]}", flush=True)
                continue

            publish_result = subprocess.run(
                [sys.executable, os.path.join(PROJECT_DIR, "tools", "publish_memories_output.py"),
                 "--base-dir", base_dir, "--dest", dept_root, "--centre", centre,
                 "--familia", familia],
                cwd=PROJECT_DIR, capture_output=True, text=True,
            )
            print(publish_result.stdout, flush=True)
            if publish_result.returncode != 0:
                print(f"[poller] ERROR publicant {base_dir}/{familia}: {publish_result.stderr[-2000:]}", flush=True)
                continue

            processed.append(f"{base_dir}/{familia}")
    return processed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Una sola passada (per a proves)")
    parser.add_argument("--sync-root", default=os.environ.get("MEMORIES_SYNC_ROOT", "/data/onedrive-memories"))
    parser.add_argument("--centre", default=os.environ.get("CENTRO_EDUCATIVO", "IESEPM"))
    parser.add_argument("--interval", type=int, default=int(os.environ.get("POLLER_INTERVAL", "300")))
    args = parser.parse_args()

    while True:
        try:
            processed = poll_once(args.sync_root, args.centre)
            if not processed:
                print("[poller] cap canvi pendent.", flush=True)
        except Exception as e:
            print(f"[poller] ERROR inesperat: {e}", flush=True)
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
