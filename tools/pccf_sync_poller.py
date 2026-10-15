#!/usr/bin/env python3

"""
Sondeja les carpetes sincronitzades OneDrive i, per a cada cicle, regenera
el report sempre que detecta un canvi (PCCF o PD). Compila automàticament
el PCCF PDF (pccf/src*/) i, de manera incremental, les Programacions: només
els mòduls que han canviat i porten PD_BUILD_DEBOUNCE segons quiets
(compila_pd_pendents), sense correus. COMPILAR_ARA les compila totes i envia
el PDF al cap de departament i a la coordinació de FE.
Tampoc genera les plantilles de PD ni els Excel: es fa a mà una vegada per
curs amb `make PCCF_ROOT=... genera-totes-plantilles`.

Estructura esperada dins de sync-root:
  pccf/
    src*, src_{FAMILIA}*, src_{FAMILIA}_{CICLO}*  → PCCF framework MDs
    0_report/   → reports del framework PCCF
    1_esborrany/ → PCCF_{CENTRO}_{CICLO}.pdf (auto)
  programacions/
    {CICLO}/                → PD_*.md + libro_{CICLO}.xlsx (+ COMPILAR_ARA)
    OPTATIVES/              → PD de les optatives + libro_optatives.xlsx
    0_report/PerCicle/      → reports de les PD per cicle
    0_report/PerDept/{DEPT}/ → report per departament (INF, SCO, ANG, FOL)
    1_esborranysPerCicle/   → Programaciones_{CENTRO}_{CICLO}.pdf (automàtic, per mòduls)
    2_esborranysPerDept/    → Programaciones_{CENTRO}_{DEPT}.pdf (en compilar un cicle)
    3_esborranyModuls/{DEPT}/ → un PDF per mòdul (en compilar un cicle)
    4_plaFormatiuFE/        → plantilla RRAA_CA + pendents_FE.txt (auto)

Ús:
    python3 tools/pccf_sync_poller.py --once             # una sola passada
    python3 tools/pccf_sync_poller.py --once --cicle APD # només un cicle
    python3 tools/pccf_sync_poller.py                    # bucle continu
"""

import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pccf_utils import (CICLES_INF, CICLES_SCO, DEPARTAMENTS, dir_moduls, dualitza, get_familia, get_moduls_del_cicle, get_optatives,
                        get_optatives_del_cicle, OPTATIVES_DIRNAME,
                        OPTATIVES_LIBRO, check_excel_coherence, find_optativa_pd, hores_per_fulla,
                        DIR_ESBORRANY_CICLE, DIR_ESBORRANY_DEPT, departaments_del_cicle,
                        dir_report_cicle, dir_report_dept)
from report_pccf import (compute_pd_status, compute_pccf_status, format_pd_report, format_pccf_report,
                         find_placeholders, escriu_reports_dept, format_dept_report, modul_verificat,
                         estat_moduls_cicle, _issues_fulla)
from memories_utils import get_teacher_emails
from mailer import smtp_configured, send_report_email, get_department_email
import genera_fe
import pd_build

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

# Últim estat FE (empremta de genera_fe.empremta) ja notificat a la
# coordinació de Formació en Empresa. Mateix criteri: fora de la carpeta
# sincronitzada, i si l'enviament falla no es guarda (es reintenta).
FE_STATE_PATH = os.path.join(PROJECT_DIR, "temp", "pccf_fe_notify_state.json")
# Destinatari a department_emails.json: {"FE": {"coordinacio": "adreça"}}
FE_EMAIL_TIPUS, FE_EMAIL_CLAU = "FE", "coordinacio"

# Caps de departament (INF, SCO, ANG, FOL) per a les PD: les mateixes adreces
# que les memòries, department_emails.json → {"FP": {"INF": "adreça", ...}}.
DEPT_EMAIL_TIPUS = "FP"
# Última empremta de l'estat de cada departament ja notificada al seu cap
# ({dept: empremta}). Mateix criteri que FE: si l'enviament falla, no es guarda.
DEPT_STATE_PATH = os.path.join(PROJECT_DIR, "temp", "pccf_dept_notify_state.json")
# Compilació incremental de les PD: {"CICLE/CODI": empremta} dels mòduls ja
# compilats (pd_build.empremtes). Un mòdul es torna a compilar quan la seua
# empremta canvia i les seues fonts porten PD_BUILD_DEBOUNCE segons sense canvis.
PD_BUILD_STATE_PATH = os.path.join(PROJECT_DIR, "temp", "pd_build_state.json")
PD_BUILD_DEBOUNCE = int(os.environ.get("PD_BUILD_DEBOUNCE", "600"))
# Versió de la PD ja enviada a cada docent: {clau_enviament: empremta de
# contingut}. Un mòdul sense registre (primer desplegament o mòdul nou) pren
# l'estat actual com a punt de partida sense enviar res.
PD_SENT_STATE_PATH = os.path.join(PROJECT_DIR, "temp", "pd_sent_state.json")


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


def incidencies_excel_cicle(cicle, prog_root, status):
    """{fitxer de PD: [incidències de la seua fulla de l'Excel i de FE]} dels
    mòduls del cicle (les mateixes del report, `estat_moduls_cicle`)."""
    per_codi = {m["codi"]: [i.strip() for i in m["excel"]] + [f"FE: {i}" for i in m["fe"]]
                for m in estat_moduls_cicle(cicle, prog_root, status)}
    return {p["filename"]: per_codi.get(p["codi"], []) for p in status["borrador"] + status["ok"]}


def incidencies_excel_optatives(opt_dir):
    """{fitxer de PD d'optativa: [incidències de la seua fulla de libro_optatives.xlsx]}."""
    opts = get_optatives()
    issues = check_excel_coherence(os.path.join(opt_dir, OPTATIVES_LIBRO), hores_per_fulla(opts.values()))
    res = {}
    for codi, modul in opts.items():
        fname = find_optativa_pd(opt_dir, codi)
        if fname:
            res[fname] = _issues_fulla(issues, modul["nombre"])
    return res


def _empremta(incidencies):
    return hashlib.sha1("\n".join(sorted(incidencies)).encode("utf-8")).hexdigest() if incidencies else ""


def notify_pd_teachers(cicle, familia, pd_dir, excel_per_fitxer=None):
    """Avisa cada docent per correu de les deficiències de la seua pròpia
    PD (no del report sencer del cicle), si el seu fitxer .md conté una
    línia "correu-e: adreça[, adreça...]" a la secció ### DOCENT (vore
    memories_utils.get_teacher_emails). Compten com a deficiència els
    placeholders [###]/[...] pendents, l'estat _BORRADOR i les incidències
    de la fulla del mòdul a l'Excel i de FE (`excel_per_fitxer`, {fitxer:
    [incidències]}, les mateixes del report).

    No invasiu: sense SMTP configurat no fa absolutament res. Es torna a
    avisar quan canvia el .md (mtime) o les incidències de l'Excel
    (empremta), i només si n'hi ha alguna -- si l'enviament falla, l'estat
    no es guarda i es reintenta a la propera passada. Estat per fitxer:
    {"mtime": ..., "excel": empremta}; els estats antics (només el mtime,
    sense empremta) es tracten com a Excel sense incidències, per a no tornar
    a avisar de les marques de la PD en desplegar.
    """
    if not smtp_configured():
        return

    state = load_pd_teacher_state()
    excel_per_fitxer = excel_per_fitxer or {}

    for fname in sorted(os.listdir(pd_dir)):
        if not fname.endswith(".md") or "_000_" in fname:
            continue
        filepath = os.path.join(pd_dir, fname)
        state_key = f"{familia}/{cicle}/{fname}"
        mtime = os.path.getmtime(filepath)
        excel = excel_per_fitxer.get(fname, [])
        empremta = _empremta(excel)
        anterior = state.get(state_key, {})
        if not isinstance(anterior, dict):
            anterior = {"mtime": anterior, "excel": ""}
        if mtime <= anterior.get("mtime", 0.0) and empremta == anterior.get("excel", ""):
            continue
        nou_estat = {"mtime": mtime, "excel": empremta}

        # Diversos docents (separats per comes): un sol correu a tots.
        to_addr = ", ".join(get_teacher_emails(filepath))
        if not to_addr:
            state[state_key] = nou_estat
            save_pd_teacher_state(state)
            continue

        deficiencies = []
        places = find_placeholders(filepath)
        if places:
            deficiencies.append(f"{len(places)} marques pendents ([###]/[...] sense substituir):\n"
                                + "\n".join(f"    L{ln}: {text}" for ln, text in places))
        # Pel sufix (no parse_pd_filename): val també per a les PD
        # d'optatives, que no porten el cicle al nom.
        if fname.endswith("_BORRADOR.md"):
            deficiencies.append("el fitxer segueix en estat BORRADOR (falta renombrar a _OK.md)")

        if not deficiencies and not excel:
            state[state_key] = nou_estat
            save_pd_teacher_state(state)
            continue

        llibre = OPTATIVES_LIBRO if cicle == OPTATIVES_DIRNAME else f"libro_{cicle}.xlsx"
        subject = f"[PCCF {cicle}] Incidències pendents a la teua PD - {fname}"
        body = f"S'han detectat les següents incidències a la teua Programació Didàctica ({fname}, cicle {cicle}):\n"
        if deficiencies:
            body += "\nAl fitxer de la PD:\n" + "\n".join(f"- {d}" for d in deficiencies) + "\n"
        if excel:
            body += (f"\nA la fulla del mòdul de l'Excel ({llibre}):\n"
                     + "\n".join(f"- {d}" for d in excel) + "\n")
        body += "\nRevisa-ho i corregix-ho directament als fitxers.\n"
        if send_report_email(to_addr, subject, body):
            print(f"[pccf-poller] correu enviat als docents ({to_addr}) per {fname}", flush=True)
            state[state_key] = nou_estat
            save_pd_teacher_state(state)


def actualitza_fe(sync_root, cicles):
    """Regenera programacions/4_plaFormatiuFE (plantilla RRAA_CA dels `cicles` i
    pendents_FE.txt de tots) i avisa la coordinació de FE si ha canviat."""
    try:
        estats, text, total, _ = genera_fe.genera(sync_root, cicles)
    except Exception as e:
        print(f"[pccf-poller] ERROR generant la plantilla RRAA_CA (FE): {e}", flush=True)
        return
    notify_fe_coordinator(sync_root, estats, text, total)


def notify_fe_coordinator(sync_root, estats, text, total):
    """Correu a la coordinació de FE amb els mòduls duals pendents i els
    docx de 4_plaFormatiuFE, només quan l'estat FE canvia. No invasiu: sense SMTP o
    sense adreça a department_emails.json no fa res."""
    if not smtp_configured():
        return
    to_addr = get_department_email(FE_EMAIL_TIPUS, FE_EMAIL_CLAU)
    if not to_addr:
        return
    empremta = genera_fe.empremta(estats)
    try:
        with open(FE_STATE_PATH, encoding="utf-8") as f:
            if json.load(f).get("empremta") == empremta:
                return
    except (OSError, json.JSONDecodeError):
        pass
    desti = os.path.join(sync_root, "programacions", genera_fe.DIR_FE)
    adjunts = [os.path.join(desti, f) for f in sorted(os.listdir(desti)) if f.endswith(".docx")]
    adjunts.append(os.path.join(desti, genera_fe.PENDENTS))
    subject = (f"[FE] Plantilla RRAA_CA: {total} mòduls duals pendents" if total
               else "[FE] Plantilla RRAA_CA: tots els mòduls duals complets")
    body = (
        "S'ha actualitzat la plantilla RRAA_CA a partir dels Excel de les "
        f"Programacions (carpeta programacions/{genera_fe.DIR_FE}, adjunta també a este correu).\n\n"
        + text
    )
    if send_report_email(to_addr, subject, body, adjunts):
        print(f"[pccf-poller] correu FE enviat a la coordinació ({to_addr}): {total} pendents", flush=True)
        os.makedirs(os.path.dirname(FE_STATE_PATH), exist_ok=True)
        with open(FE_STATE_PATH, "w", encoding="utf-8") as f:
            json.dump({"empremta": empremta}, f)


def _llig_dept_state():
    try:
        with open(DEPT_STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _guarda_dept_state(state):
    os.makedirs(os.path.dirname(DEPT_STATE_PATH), exist_ok=True)
    with open(DEPT_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f)


def _resum_dept(moduls):
    pendents = sum(not modul_verificat(m) for m in moduls)
    return f"{pendents} de {len(moduls)} mòduls amb incidències" if pendents else f"tots els mòduls ({len(moduls)}) complets"


def notify_dept_report(sync_root, depts, ja_avisats=()):
    """Correu al cap de cada departament amb el seu report (0_report/{DEPT}/)
    quan l'estat del departament canvia de veritat: per a cada mòdul, l'estat
    OK/BORRADOR/FALTA i si té o no marques pendents i incidències de l'Excel
    o de FE (empremta, com a FE). Omplir una marca de les moltes que en
    queden, o editar text, no avisa.
    No invasiu: sense SMTP o sense adreça a department_emails.json
    ({"FP": {DEPT: adreça}}) no fa res. Els departaments de `ja_avisats`
    reben en esta passada el correu de compilació (que ja porta el report):
    només se'n guarda l'empremta, per no enviar-los dos correus."""
    if not smtp_configured():
        return
    state = _llig_dept_state()
    prog_root = os.path.join(sync_root, "programacions")
    for dept, moduls in depts.items():
        if not moduls:
            continue
        to_addr = get_department_email(DEPT_EMAIL_TIPUS, dept)
        if not to_addr:
            continue
        # Per mòdul, només si té o no incidències de cada tipus: omplir una
        # marca o canviar unes hores no avisa; passar a OK o a complet, sí.
        empremta = genera_fe.empremta([
            [m["cicle"], m["codi"], m["estat"], bool(m["marques"]), bool(m["excel"]), bool(m["fe"])]
            for m in moduls])
        if state.get(dept) == empremta:
            continue
        if dept in ja_avisats:
            state[dept] = empremta
            _guarda_dept_state(state)
            continue
        report = os.path.join(dir_report_dept(prog_root, dept), f"report_{dept}.txt")
        subject = f"[PD {dept}] Estat de les programacions: {_resum_dept(moduls)}"
        body = (
            f"Ha canviat l'estat de les programacions didàctiques del departament {dept} "
            "(carpeta programacions/0_report, adjunt també a este correu).\n\n"
            + format_dept_report(dept, moduls)
        )
        if send_report_email(to_addr, subject, body, [report]):
            print(f"[pccf-poller] correu de report enviat al cap del departament {dept} ({to_addr})", flush=True)
            state[dept] = empremta
            _guarda_dept_state(state)


def notify_dept_heads(sync_root, centre, depts, cicles):
    """Després de compilar les Programacions de `cicles`, un sol correu per
    departament afectat amb el seu PDF (2_esborranysPerDept) i el seu report,
    encara que el disparador global n'haja compilat diversos."""
    if not smtp_configured():
        return
    prog_root = os.path.join(sync_root, "programacions")
    for dept in sorted(depts):
        to_addr = get_department_email(DEPT_EMAIL_TIPUS, dept)
        if not to_addr:
            print(f"[pccf-poller] PD del departament {dept} compilada però no hi ha email a department_emails.json (tipus '{DEPT_EMAIL_TIPUS}', clau '{dept}')", flush=True)
            continue
        pdf = os.path.join(prog_root, DIR_ESBORRANY_DEPT, f"Programaciones_{centre}_{dept}.pdf")
        report = os.path.join(dir_report_dept(prog_root, dept), f"report_{dept}.txt")
        subject = f"[PD {dept}] Programacions del departament compilades"
        body = (
            f"S'han compilat les Programacions de {', '.join(cicles)} i s'ha actualitzat el PDF "
            f"del departament {dept} (programacions/{DIR_ESBORRANY_DEPT}). Els PDF de cada mòdul "
            "són a programacions/3_esborranyModuls.\n\n"
            "Adjunts: el PDF del departament i el seu report, si s'han pogut adjuntar.\n"
        )
        if send_report_email(to_addr, subject, body, [pdf, report]):
            print(f"[pccf-poller] correu enviat al cap del departament {dept} ({to_addr}) amb el PDF", flush=True)


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
    """Compila totes les Programacions d'un cicle (COMPILAR_ARA) i envia el PDF
    al cap de departament (department_emails.json, tipus "PCCF", clau = cicle)
    i, si el cicle té mòduls que dualitzen, a la coordinació de FE. Torna True
    si s'han compilat els mòduls (encara que algun haja fallat: queda al log i
    es manté el seu PDF anterior; si no, el disparador es reintentaria sempre)."""
    print(f"[pccf-poller] {familia}_{cicle}: {motiu}, compilant Programacions...", flush=True)
    resultat_path = os.path.join(PROJECT_DIR, "temp", f"pd_build_result_{cicle}.json")
    if os.path.exists(resultat_path):
        os.remove(resultat_path)
    result = subprocess.run(
        ["make", f"PCCF_ROOT={sync_root}", f"CENTRO_EDUCATIVO={centre}",
         f"compila-pd-pccf-{cicle.lower()}"],
        cwd=PROJECT_DIR, capture_output=True, text=True,
        env={**os.environ, "PD_BUILD_RESULT": resultat_path},
    )
    resultat = _llig_json(resultat_path)
    if result.returncode != 0:
        print(f"[pccf-poller] ERROR compilant PD {familia}_{cicle}:\n{result.stdout[-2000:]}\n{result.stderr[-2000:]}", flush=True)
        if not resultat:
            return False
    envia_pd_docents(cicle, os.path.join(sync_root, "programacions"), resultat.get("ok", []))

    pdf_path = os.path.join(sync_root, "programacions", DIR_ESBORRANY_CICLE, f"Programaciones_{centre}_{cicle}.pdf")
    destinataris = [get_department_email("PCCF", cicle)]
    if any(dualitza(m) for m in get_moduls_del_cicle(cicle, familia).values()):
        destinataris.append(get_department_email(FE_EMAIL_TIPUS, FE_EMAIL_CLAU))
    to_addr = ", ".join(dict.fromkeys(d for d in destinataris if d))
    if not to_addr:
        print(f"[pccf-poller] {familia}_{cicle}: PD compilada però no hi ha email de cap de departament a department_emails.json (tipus 'PCCF', clau '{cicle}')", flush=True)
        return True

    subject = f"[PCCF {cicle}] Programacions compilades"
    body = (
        f"S'ha generat el PDF de Programacions del cicle {cicle} a petició del cap de departament "
        f"(fitxer {PD_COMPILE_TRIGGER}).\n\n"
        "L'adjunt d'este correu, si s'ha pogut adjuntar, és la darrera versió compilada.\n"
    )
    if resultat.get("ko"):
        body += (f"\nNo s'han pogut compilar els mòduls {', '.join(resultat['ko'])}: el PDF inclou la seua "
                 "versió anterior. Cal revisar el seu fitxer de PD.\n")
    if send_report_email(to_addr, subject, body, attachments=[pdf_path]):
        print(f"[pccf-poller] correu enviat ({to_addr}) per Programacions {cicle}", flush=True)
    return True


def _llig_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _guarda_json(path, dades):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dades, f, indent=1)


def marca_compilats(cicle, prog_root, codis=None):
    """Guarda l'empremta actual dels mòduls `codis` (tots si és None) com a compilats."""
    try:
        fps = pd_build.empremtes(cicle, prog_root)
    except Exception as e:
        print(f"[pccf-poller] {cicle}: no s'han pogut calcular les empremtes de les PD: {e}", flush=True)
        return
    state = _llig_json(PD_BUILD_STATE_PATH)
    for k in [k for k in state if k.startswith(f"{cicle}/") and k.split("/", 1)[1] not in fps]:
        del state[k]
    for codi, v in fps.items():
        if codis is None or codi in codis:
            state[f"{cicle}/{codi}"] = v["empremta"]
    _guarda_json(PD_BUILD_STATE_PATH, state)


def compila_pd_pendents(cicle, familia, sync_root, centre):
    """Compilació automàtica i sense correus: torna a compilar només els
    mòduls del cicle que han canviat (pd_build.empremtes) i que porten
    PD_BUILD_DEBOUNCE segons sense canvis; després es munten el PDF del cicle
    i els dels departaments. Si s'ha esborrat la PD d'algun mòdul, només es
    torna a muntar. Torna True si ha compilat o muntat alguna cosa.

    Un mòdul que no compila es dona per fet igualment (l'error queda al log
    i el seu PDF anterior es manté): no es reintenta a cada passada, sinó
    quan canvie de nou o amb COMPILAR_ARA."""
    prog_root = os.path.join(sync_root, "programacions")
    try:
        fps = pd_build.empremtes(cicle, prog_root)
    except Exception as e:
        print(f"[pccf-poller] {familia}_{cicle}: no s'han pogut calcular les empremtes de les PD: {e}", flush=True)
        return False
    state = _llig_json(PD_BUILD_STATE_PATH)
    ara = time.time()
    canviats = [c for c, v in fps.items() if state.get(f"{cicle}/{c}") != v["empremta"]]
    pendents = sorted(c for c in canviats if ara - fps[c]["mtime"] >= PD_BUILD_DEBOUNCE)
    esborrats = [k for k in state if k.startswith(f"{cicle}/") and k.split("/", 1)[1] not in fps]
    if len(pendents) < len(canviats):
        print(f"[pccf-poller] {familia}_{cicle}: {len(canviats) - len(pendents)} PD amb canvis recents, "
              f"es compilaran quan porten {PD_BUILD_DEBOUNCE // 60 or 1} min sense canvis", flush=True)
    if not pendents and not esborrats:
        return False

    if pendents:
        print(f"[pccf-poller] {familia}_{cicle}: compilant les PD de {', '.join(pendents)}...", flush=True)
        resultat_path = os.path.join(PROJECT_DIR, "temp", f"pd_build_result_{cicle}.json")
        if os.path.exists(resultat_path):
            os.remove(resultat_path)
        r = subprocess.run(
            ["make", f"PCCF_ROOT={sync_root}", f"CENTRO_EDUCATIVO={centre}",
             f"compila-pd-pccf-{cicle.lower()}", f"MODULS={' '.join(pendents)}"],
            cwd=PROJECT_DIR, capture_output=True, text=True,
            env={**os.environ, "PD_BUILD_RESULT": resultat_path},
        )
        resultat = _llig_json(resultat_path)
        if not resultat:
            # Ha fallat abans de compilar cap mòdul (muntatge, preparació...): es reintenta
            print(f"[pccf-poller] ERROR compilant les PD de {familia}_{cicle}:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}", flush=True)
            return False
        if resultat.get("ko") or r.returncode != 0:
            print(f"[pccf-poller] {familia}_{cicle}: errors compilant {', '.join(resultat.get('ko', [])) or 'el cicle o els departaments'}:\n"
                  f"{r.stdout[-2000:]}\n{r.stderr[-2000:]}", flush=True)
        for codi in pendents:
            state[f"{cicle}/{codi}"] = fps[codi]["empremta"]
        print(f"[pccf-poller] {familia}_{cicle}: PD compilades: {', '.join(resultat.get('ok', [])) or 'cap'}", flush=True)
        envia_pd_docents(cicle, prog_root, resultat.get("ok", []), fps)
    else:
        print(f"[pccf-poller] {familia}_{cicle}: PD esborrades ({', '.join(k.split('/', 1)[1] for k in esborrats)}), es torna a muntar el cicle", flush=True)
        r = subprocess.run(
            ["make", f"PCCF_ROOT={sync_root}", f"CENTRO_EDUCATIVO={centre}", f"munta-pd-pccf-{cicle.lower()}"],
            cwd=PROJECT_DIR, capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"[pccf-poller] ERROR muntant les PD de {familia}_{cicle}:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}", flush=True)
            return False
    for k in esborrats:
        del state[k]
    _guarda_json(PD_BUILD_STATE_PATH, state)
    return True


def envia_pd_docents(cicle, prog_root, codis, fps=None):
    """Envia a cada docent el PDF nou del seu mòdul (3_esborranyModuls), per a
    cada mòdul de `codis` compilat correctament, però només si el seu
    contingut (pd_build: el .md i la seua fulla de l'Excel) ha canviat des de
    l'última versió enviada. Els destinataris són els del camp correu-e de la
    PD. Sense SMTP no fa res; si l'enviament falla, es reintenta la propera
    vegada que es compile."""
    if not codis or not smtp_configured():
        return
    if fps is None:
        try:
            fps = pd_build.empremtes(cicle, prog_root)
        except Exception as e:
            print(f"[pccf-poller] {cicle}: no s'han pogut calcular les empremtes de les PD: {e}", flush=True)
            return
    enviats = _llig_json(PD_SENT_STATE_PATH)
    for codi in codis:
        info = fps.get(codi)
        if not info:
            continue
        clau = pd_build.clau_enviament(cicle, codi, info)
        if enviats.get(clau) == info["contingut"]:
            continue
        if clau not in enviats:
            enviats[clau] = info["contingut"]
            continue
        to_addr = ", ".join(dict.fromkeys(e for md in info["mds"] for e in get_teacher_emails(md)))
        pdfs = [p for dept in DEPARTAMENTS
                for p in glob.glob(os.path.join(dir_moduls(prog_root, dept), f"PD_{cicle}_{codi}_*.pdf"))]
        if not to_addr or not pdfs:
            enviats[clau] = info["contingut"]
            continue
        nom = os.path.basename(pdfs[0])
        subject = f"[PD {cicle}] Nova versió de la teua programació - {nom}"
        body = (
            f"S'ha generat una nova versió de la teua Programació Didàctica ({nom}), "
            "perquè ha canviat el fitxer de la PD o la fulla del mòdul a l'Excel. "
            "La tens adjunta i també a OneDrive, a programacions/3_esborranyModuls.\n\n"
            "Si el títol porta ✎ (encara en BORRADOR) o ✗ (marques pendents o incidències a "
            "l'Excel), el PDF porta la marca d'aigua ESBORRANY; el detall de què falta t'arriba "
            "en el correu d'incidències.\n"
        )
        if send_report_email(to_addr, subject, body, attachments=[pdfs[0]]):
            print(f"[pccf-poller] nova versió de {nom} enviada als docents ({to_addr})", flush=True)
            enviats[clau] = info["contingut"]
    _guarda_json(PD_SENT_STATE_PATH, enviats)


def check_pd_compile_trigger(cicle, familia, pdir, sync_root, centre, forcat=False):
    """Compila el PDF de Programacions si el cap de departament ha deixat el
    fitxer disparador `PD_COMPILE_TRIGGER` (buit) dins de programacions/{CICLE}/,
    o si `forcat` (disparador global a l'arrel de programacions/).

    Independent de si hi ha hagut cap canvi de PD en esta passada -- cal
    comprovar-ho sempre. Si la compilació falla, el disparador del cicle NO
    s'esborra (es reintenta a la propera passada, mateix criteri que
    notify_pd_teachers). Torna None si no hi havia res a compilar, True si
    ha compilat i False si s'ha intentat i ha fallat.
    """
    triggers = find_pd_triggers(pdir)
    if not triggers and not forcat:
        return None

    motiu = "disparador global" if forcat and not triggers else f"disparador {PD_COMPILE_TRIGGER} detectat"
    if not compile_pd(cicle, familia, pdir, sync_root, centre, motiu):
        return False
    marca_compilats(cicle, os.path.join(sync_root, "programacions"))

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
    compilats = []  # cicles amb les Programacions compilades en esta passada
    cicles_fe = []  # cicles amb canvis de PD/Excel: es regenera la plantilla RRAA_CA
    estats_pd = {}  # compute_pd_status ja calculats, per al report de departament

    # PD d'optatives (compartides entre cicles): avís al docent una sola
    # vegada per passada (l'estat per fitxer evita repetir-los).
    opt_dir = os.path.join(prog_root, OPTATIVES_DIRNAME)
    if os.path.isdir(opt_dir):
        notify_pd_teachers(OPTATIVES_DIRNAME, "OPT", opt_dir, incidencies_excel_optatives(opt_dir))

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
        if te_pd:
            compilat = check_pd_compile_trigger(cicle, familia, pdir, sync_root, centre, forcat=bool(global_triggers))
            if compilat is False:
                fallats.append((cicle, pdir))
            elif compilat:
                compilats.append(cicle)
            elif compila_pd_pendents(cicle, familia, sync_root, centre):
                processed.append(f"{key} (PD)")

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
            estats_pd[cicle] = status
            report_dir = dir_report_cicle(prog_root)
            os.makedirs(report_dir, exist_ok=True)
            with open(os.path.join(report_dir, f"{key}.txt"), "w", encoding="utf-8") as f:
                f.write(format_pd_report(status))
            notify_pd_teachers(cicle, familia, pdir, incidencies_excel_cicle(cicle, prog_root, status))
            cicles_fe.append(cicle)

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

    depts_compilats = set().union(*(departaments_del_cicle(c) for c in compilats))
    if cicles_fe:
        actualitza_fe(sync_root, cicles_fe)
        # Report per departament (de tots els cicles) i avís al cap si l'estat
        # del seu departament ha canviat.
        try:
            notify_dept_report(sync_root, escriu_reports_dept(prog_root, estats_pd), depts_compilats)
        except Exception as e:
            print(f"[pccf-poller] ERROR generant els reports de departament: {e}", flush=True)

    if compilats:
        notify_dept_heads(sync_root, centre, depts_compilats, compilats)

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
