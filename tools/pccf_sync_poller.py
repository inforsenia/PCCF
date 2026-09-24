#!/usr/bin/env python3

"""
Sondeja les carpetes sincronitzades OneDrive i, per a cada cicle, regenera
el report sempre que detecta un canvi (PCCF o PD). Compila automàticament
el PCCF PDF (pccf/src*/) pero NO les Programaciones (programacions/) --
això es fa manualment pel cap de departament (compila-pd-pccf-{cicle}).
Tampoc genera les plantilles de PD ni els Excel: es fa a mà una vegada per
curs amb `make PCCF_ROOT=... genera-totes-plantilles`.

Estructura esperada dins de sync-root:
  pccf/
    src*, src_{FAMILIA}*, src_{FAMILIA}_{CICLO}*  → PCCF framework MDs
    0_report/   → reports del framework PCCF
    1_esborrany/ → PCCF_{CENTRO}_{CICLO}.pdf (auto)
  programacions/{CICLO}/
    PD_*.md + libro_{CICLO}.xlsx
    0_report/   → reports de les PD
    1_esborrany/ → Programaciones_{CENTRO}_{CICLO}.pdf (manual)

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
from pccf_utils import CICLES_INF, CICLES_SCO, get_familia, get_optatives_del_cicle, OPTATIVES_DIRNAME
from report_pccf import compute_pd_status, compute_pccf_status, format_pd_report, format_pccf_report, find_placeholders
from memories_utils import get_teacher_email
from mailer import smtp_configured, send_report_email, get_department_email

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CICLES_ALL = CICLES_INF + CICLES_SCO

# Fitxer disparador que el cap de departament crea (buit) dins de
# programacions/{CICLE}/ des de la seua carpeta sincronitzada OneDrive, per a
# demanar la compilació del PDF de Programacions sense accés al contenidor.
# Deliberadament manual (a diferència del PCCF, que s'autocompila): el moment
# de compilar el decideix el cap, no cada edició d'una PD.
PD_COMPILE_TRIGGER = "COMPILAR_ARA"
# Des d'OneDrive/Windows costa crear un fitxer sense extensió: s'accepten
# també .md i .txt, sense distingir majúscules.
PD_COMPILE_TRIGGER_EXTS = ("", ".md", ".txt")
# El mateix disparador a l'arrel de programacions/ (al costat de les carpetes
# de cicle) compila les Programacions de TOTS els cicles.

STATE_PATH = os.path.join(PROJECT_DIR, "temp", "pccf_poller_state.json")

# Estat intern del poller (últim mtime de cada PD ja avaluat per a
# notificació al docent). MAI dins la carpeta sincronitzada: és bookkeeping
# del poller, no contingut per als docents.
PD_TEACHER_STATE_PATH = os.path.join(PROJECT_DIR, "temp", "pccf_pd_teacher_notify_state.json")


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


def dir_mtime(base, subpath):
    d = os.path.join(base, subpath)
    if not os.path.isdir(d):
        return 0.0
    mtimes = []
    for root, _dirs, files in os.walk(d):
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


def load_pd_teacher_state():
    if not os.path.exists(PD_TEACHER_STATE_PATH):
        return {}
    try:
        with open(PD_TEACHER_STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_pd_teacher_state(state):
    os.makedirs(os.path.dirname(PD_TEACHER_STATE_PATH), exist_ok=True)
    with open(PD_TEACHER_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f)


def notify_pd_teachers(cicle, familia, pd_dir):
    """Avisa cada docent per correu de les deficiències de la seua pròpia
    PD (no del report sencer del cicle), si el seu fitxer .md conté una
    línia "correu-e: adreça" a la secció ### DOCENT (vore
    memories_utils.get_teacher_email). En esta v1 nomes compten com a
    deficiència els placeholders [###]/[...] pendents i l'estat _BORRADOR
    -- la coherència de l'Excel es queda fora (nomes al report agregat).

    No invasiu: sense SMTP configurat no fa absolutament res. Cada versió
    (mtime) d'un fitxer es processa com a màxim una vegada -- si
    l'enviament falla, l'estat no es guarda i es reintenta a la propera
    passada.
    """
    if not smtp_configured():
        return

    state = load_pd_teacher_state()

    for fname in sorted(os.listdir(pd_dir)):
        if not fname.endswith(".md") or "_000_" in fname:
            continue
        filepath = os.path.join(pd_dir, fname)
        state_key = f"{familia}/{cicle}/{fname}"
        mtime = os.path.getmtime(filepath)
        if mtime <= state.get(state_key, 0.0):
            continue

        to_addr = get_teacher_email(filepath)
        if not to_addr:
            state[state_key] = mtime
            save_pd_teacher_state(state)
            continue

        deficiencies = []
        places = find_placeholders(filepath)
        if places:
            deficiencies.append(f"{len(places)} marques pendents ([###]/[...] sense substituir)")
        # Pel sufix (no parse_pd_filename): val també per a les PD
        # d'optatives, que no porten el cicle al nom.
        if fname.endswith("_BORRADOR.md"):
            deficiencies.append("el fitxer segueix en estat BORRADOR (falta renombrar a _OK.md)")

        if not deficiencies:
            state[state_key] = mtime
            save_pd_teacher_state(state)
            continue

        subject = f"[PCCF {cicle}] Incidències pendents a la teua PD - {fname}"
        body = (
            f"S'han detectat les següents incidències a la teua Programació "
            f"Didàctica ({fname}, cicle {cicle}):\n\n"
            + "\n".join(f"- {d}" for d in deficiencies)
            + "\n\nRevisa i completa-la directament al fitxer.\n"
        )
        if send_report_email(to_addr, subject, body):
            print(f"[pccf-poller] correu enviat al docent ({to_addr}) per {fname}", flush=True)
            state[state_key] = mtime
            save_pd_teacher_state(state)


def has_pd_files(pdir):
    try:
        return any(f.startswith("PD_") and f.endswith(".md") for f in os.listdir(pdir))
    except OSError:
        return False


def find_pd_triggers(directori):
    """Fitxers disparador `PD_COMPILE_TRIGGER` (amb extensions acceptades)
    presents a `directori`, o llista buida."""
    valids = {(PD_COMPILE_TRIGGER + ext).upper() for ext in PD_COMPILE_TRIGGER_EXTS}
    try:
        return [os.path.join(directori, f) for f in os.listdir(directori)
                if f.upper() in valids and os.path.isfile(os.path.join(directori, f))]
    except OSError:
        return []


def compile_pd(cicle, familia, pdir, sync_root, centre, motiu):
    """Compila el PDF de Programacions d'un cicle i avisa per correu el cap
    de departament (department_emails.json, tipus "PCCF", clau = cicle).
    Torna True si la compilació ha anat bé."""
    print(f"[pccf-poller] {familia}_{cicle}: {motiu}, compilant Programacions...", flush=True)
    result = subprocess.run(
        ["make", f"PCCF_ROOT={sync_root}", f"CENTRO_EDUCATIVO={centre}",
         f"compila-pd-pccf-{cicle.lower()}"],
        cwd=PROJECT_DIR, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"[pccf-poller] ERROR compilant PD {familia}_{cicle}:\n{result.stdout[-2000:]}\n{result.stderr[-2000:]}", flush=True)
        return False

    pdf_path = os.path.join(pdir, "1_esborrany", f"Programaciones_{centre}_{cicle}.pdf")
    to_addr = get_department_email("PCCF", cicle)
    if not to_addr:
        print(f"[pccf-poller] {familia}_{cicle}: PD compilada però no hi ha email de cap de departament a department_emails.json (tipus 'PCCF', clau '{cicle}')", flush=True)
        return True

    subject = f"[PCCF {cicle}] Programacions compilades"
    body = (
        f"S'ha generat el PDF de Programacions del cicle {cicle} a petició teua "
        f"(fitxer {PD_COMPILE_TRIGGER}).\n\n"
        "L'adjunt d'este correu, si s'ha pogut adjuntar, és la darrera versió compilada.\n"
    )
    if send_report_email(to_addr, subject, body, attachments=[pdf_path]):
        print(f"[pccf-poller] correu enviat al cap de departament ({to_addr}) per Programacions {cicle}", flush=True)
    return True


def check_pd_compile_trigger(cicle, familia, pdir, sync_root, centre, forcat=False):
    """Compila el PDF de Programacions si el cap de departament ha deixat el
    fitxer disparador `PD_COMPILE_TRIGGER` (buit) dins de programacions/{CICLE}/,
    o si `forcat` (disparador global a l'arrel de programacions/).

    Independent de si hi ha hagut cap canvi de PD en esta passada -- cal
    comprovar-ho sempre. Si la compilació falla, el disparador del cicle NO
    s'esborra (es reintenta a la propera passada, mateix criteri que
    notify_pd_teachers). Torna False només si s'ha intentat i ha fallat.
    """
    triggers = find_pd_triggers(pdir)
    if not triggers and not forcat:
        return True

    motiu = "disparador global" if forcat and not triggers else f"disparador {PD_COMPILE_TRIGGER} detectat"
    if not compile_pd(cicle, familia, pdir, sync_root, centre, motiu):
        return False

    for trigger_path in triggers:
        try:
            os.remove(trigger_path)
        except OSError:
            pass
    return True


def poll_once(sync_root, centre, cicle=None):
    processed = []
    state = load_state()

    cicles_a_processar = [cicle] if cicle else CICLES_ALL

    # Disparador global (programacions/COMPILAR_ARA): compila tots els cicles.
    # Només quan es processen tots (no amb --cicle).
    prog_root = os.path.join(sync_root, "programacions")
    global_triggers = [] if cicle else find_pd_triggers(prog_root)
    if global_triggers:
        print(f"[pccf-poller] disparador global {PD_COMPILE_TRIGGER} detectat a programacions/: compilant tots els cicles", flush=True)
    fallats = []

    # PD d'optatives (compartides entre cicles): avís al docent una sola
    # vegada per passada (l'estat per fitxer evita repetir-los).
    opt_dir = os.path.join(prog_root, OPTATIVES_DIRNAME)
    if os.path.isdir(opt_dir):
        notify_pd_teachers(OPTATIVES_DIRNAME, "OPT", opt_dir)

    for cicle in cicles_a_processar:
        familia = get_familia(cicle)
        key = f"{familia}_{cicle}"

        pdir = os.path.join(sync_root, "programacions", cicle)
        pccf_dir = os.path.join(sync_root, "pccf")

        # Les plantilles de PD i els Excel NO es generen ací: es fa a mà una
        # vegada per curs (o quan canvien les plantilles) amb
        # `make PCCF_ROOT=... genera-totes-plantilles`. Regenerar-les a cada
        # passada tornava a crear en silenci les PD que un docent esborrava i,
        # amb OneDrive a mitjan sincronitzar, podia generar BORRADORs en
        # conflicte amb els dels docents.
        # programacions/{CICLE}/ pot existir buida: el que compta és que hi haja PD.
        te_pd = has_pd_files(pdir)
        if not te_pd and global_triggers:
            print(f"[pccf-poller] {key}: no hi ha PD a programacions/{cicle}/ (cal genera-totes-plantilles), no es compilen les seues Programacions", flush=True)

        # Independent de si hi ha canvis de PD/PCCF esta passada -- el cap de
        # departament pot demanar compilar encara que res haja canviat.
        if te_pd and not check_pd_compile_trigger(cicle, familia, pdir, sync_root, centre, forcat=bool(global_triggers)):
            fallats.append((cicle, pdir))

        pd_mtime = latest_source_mtime(pdir)
        # Les optatives del cicle formen part de les seues Programacions i del
        # seu report: un canvi a programacions/OPTATIVES/ també el regenera.
        if get_optatives_del_cicle(cicle, familia):
            pd_mtime = max(pd_mtime, latest_source_mtime(opt_dir))
        mtime_src = dir_mtime(pccf_dir, "src")
        mtime_familia = dir_mtime(pccf_dir, f"src_{familia}")
        mtime_cicle = dir_mtime(pccf_dir, f"src_{familia}_{cicle}")

        if pd_mtime == 0.0 and mtime_src == 0.0 and mtime_familia == 0.0 and mtime_cicle == 0.0:
            continue

        last_pd_mtime = state.get(key, {}).get("mtime_pd", 0.0)
        last_src = state.get(key, {}).get("mtime_src", 0.0)
        last_familia = state.get(key, {}).get("mtime_familia", 0.0)
        last_cicle = state.get(key, {}).get("mtime_cicle", 0.0)

        pd_canviat = pd_mtime > last_pd_mtime
        pccf_canviat = mtime_src > last_src or mtime_familia > last_familia or mtime_cicle > last_cicle
        if not pd_canviat and not pccf_canviat:
            continue

        what = []
        if pccf_canviat:
            what.append("PCCF")
        if pd_canviat:
            what.append("PD")
        print(f"[pccf-poller] {key}: canvi {'+'.join(what)} detectat", flush=True)

        # --- Regenerar reports ---
        if pd_canviat and te_pd:
            status = compute_pd_status(cicle, familia, pdir)
            report_dir = os.path.join(pdir, "0_report")
            os.makedirs(report_dir, exist_ok=True)
            with open(os.path.join(report_dir, f"{key}.txt"), "w", encoding="utf-8") as f:
                f.write(format_pd_report(status))
            notify_pd_teachers(cicle, familia, pdir)

        if pccf_canviat:
            status = compute_pccf_status(cicle, familia, pccf_dir)
            report_dir = os.path.join(pccf_dir, "0_report")
            os.makedirs(report_dir, exist_ok=True)
            with open(os.path.join(report_dir, f"{key}.txt"), "w", encoding="utf-8") as f:
                f.write(format_pccf_report(status))

        # --- Compilar PCCF només si els PCCF han canviat ---
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

        state[key] = {"mtime_src": mtime_src, "mtime_familia": mtime_familia, "mtime_cicle": mtime_cicle, "mtime_pd": pd_mtime}
        save_state(state)
        processed.append(key)

    if global_triggers:
        # El global s'esborra sempre; si algun cicle ha fallat, es deixa el
        # disparador dins de la seua carpeta perquè només es reintente eixe
        # cicle (i no tots) a la propera passada.
        for cicle_ko, pdir_ko in fallats:
            if not find_pd_triggers(pdir_ko) and os.path.isdir(pdir_ko):
                open(os.path.join(pdir_ko, PD_COMPILE_TRIGGER), "w").close()
                print(f"[pccf-poller] {cicle_ko}: compilació fallada, es deixa {PD_COMPILE_TRIGGER} a la seua carpeta per a reintentar", flush=True)
        for trigger_path in global_triggers:
            try:
                os.remove(trigger_path)
            except OSError:
                pass

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
