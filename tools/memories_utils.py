#!/usr/bin/env python3

"""
Funcions compartides per a la gestió de memòries (report i compilació).
"""

import os
import re
import json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

CICLES_CONEGUTS = sorted(["SMX", "DAM", "CEIABD", "FPBIIO", "APD", "EI", "IS"], key=len, reverse=True)
ANNEX_PREFIX = "AA_ACTIVITATS_EXTRAESCOLARS"
CURSOS_ESOBAT = sorted(["ESO", "BAT"], key=len, reverse=True)


def is_annex_file(filename):
    """Check if filename is an annex file (extraescolars)."""
    return "AA_ACTIVITATS_EXTRAESCOLARS" in filename and filename.endswith(".md")


def get_output_parent(base_dir):
    """Derive output dir name from base_dir.
    "memoriaFP" → "memories_FP", "memoriaESOBAT" → "memories_ESOBAT"
    """
    suffix = base_dir.replace("memoria", "", 1)
    return f"memories_{suffix}"


def get_report_dir(base_dir="memoriaFP", is_esobat=False, timestamp=None):
    """Return the report dir path: PDFS/0_YYYYMMDD_hhmm_report_memories_{ESOBAT|FP}/
    If timestamp is None, falls back to env REPORT_TIMESTAMP, then to datetime.now().
    """
    if timestamp is None:
        timestamp = os.environ.get('REPORT_TIMESTAMP')
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    tipus = "ESOBAT" if is_esobat else "FP"
    report_dir = os.path.join(PROJECT_DIR, "PDFS", f"0_{timestamp}_report_memories_{tipus}")
    return report_dir

def normalitza_fitxers(memories_dir):
    """
    Normalitza noms de fitxer abans de parsejar:
    - Renombra _ok.md  → _OK.md  (automàtic)
    - Detecta _BORR.md → es reporta com a BORR_TRUNCAT
    - Detecta fitxers sense sufix → es reporten com a SENSE_SUFIX
    - Ignora *safeBackup*

    Retorna (renamed, issues) on:
      renamed = llista de (nom_antic, nom_nou)
      issues  = llista de (nom_fitxer, tipus)
    """
    renamed = []
    issues = []
    if not os.path.isdir(memories_dir):
        return renamed, issues

    for fname in sorted(os.listdir(memories_dir)):
        if not fname.endswith(".md"):
            continue
        if "safeBackup" in fname:
            continue

        # _ok.md → _OK.md
        if fname.endswith("_ok.md"):
            new_name = fname[:-6] + "_OK.md"
            os.rename(
                os.path.join(memories_dir, fname),
                os.path.join(memories_dir, new_name)
            )
            renamed.append((fname, new_name))
            continue

        # _BORR.md (truncat, pero no _BORRADOR.md)
        if re.search(r'_BORR\.md$', fname) and not fname.endswith("_BORRADOR.md"):
            issues.append((fname, "BORR_TRUNCAT"))
            continue

        # Sense sufix (ni OK ni BORRADOR)
        if not re.search(r'_(OK|ok|Ok|BORRADOR|borrador|BORR|borr)\.md$', fname):
            issues.append((fname, "SENSE_SUFIX"))

    return renamed, issues


def parse_filename(filename):
    if not filename.endswith(".md"):
        return None
    base = filename[:-3]
    parts = base.split("_")
    if len(parts) < 4:
        return None

    estat = parts[-1]
    if estat not in ("BORRADOR", "OK"):
        return None

    modul = parts[-2]

    rest = "_".join(parts[:-2])
    # rest = {curs_academic}_{curs}{cicle}{grup}
    # curs_academic = first 5 chars (XX_XX)
    if len(rest) < 6 or rest[2] != "_":
        return None
    curs_academic = rest[:5]
    after_academic = rest[6:]

    # after_academic = {curs}{cicle}[{grup}]
    curs = ""
    cicle = ""
    grup = ""

    for cicle_candidat in CICLES_CONEGUTS:
        idx = after_academic.find(cicle_candidat)
        if idx == -1:
            continue
        curs = after_academic[:idx]
        rest_after_cicle = after_academic[idx + len(cicle_candidat):]
        if rest_after_cicle.startswith("_"):
            grup = rest_after_cicle[1:]
        else:
            grup = rest_after_cicle
        cicle = cicle_candidat
        break

    if not cicle:
        return parse_filename_esobat(filename)

    return {
        "curs_academic": curs_academic,
        "curs": curs,
        "cicle": cicle,
        "grup": grup if grup else "",
        "modul": modul,
        "estat": estat,
        "filename": filename,
    }


def get_grup_label(grup):
    if not grup:
        return "Grup únic"
    return f"Grup {grup}"


def curs_display(curs):
    if not curs:
        return ""
    ordinals = {"1": "1r", "2": "2n", "3": "3r", "4": "4t"}
    if curs in ordinals:
        return ordinals[curs]
    return f"{curs}è"


CURSOS_ESPECIALS = sorted(["PDC", "APLI"], key=len, reverse=True)


def parse_filename_esobat(filename):
    """Parse ESO/BAT filename: {curs_acad}_{curs_codi}{grup}_{materia}_{estat}.md
    
    Examples:
      25_26_1ESOA_ANGLES_BORRADOR.md → curs_codi=1ESO, grup=A, materia=ANGLES
      25_26_3ESO_PDC_ANGLES3PDC_BORRADOR.md → curs_codi=3ESO, grup=PDC, materia=ANGLES3PDC
      25_26_3PDC_PDC_ANGLES3PDC_BORRADOR.md → curs_codi=3PDC, grup=PDC, materia=ANGLES3PDC
      25_26_4BATA_ANGLESII_BORRADOR.md → curs_codi=4BAT, grup=A, materia=ANGLESII
    """
    if not filename.endswith(".md"):
        return None
    base = filename[:-3]
    parts = base.split("_")
    if len(parts) < 4:
        return None

    estat = parts[-1]
    if estat not in ("BORRADOR", "OK"):
        return None

    materia = parts[-2]

    rest = "_".join(parts[:-2])
    # rest = {curs_academic}_{curs_codi}{grup}
    if len(rest) < 6 or rest[2] != "_":
        return None
    curs_academic = rest[:5]
    after_academic = rest[6:]

    curs_codi = ""
    curs = ""
    etapa = ""
    grup = ""

    # Try ESO/BAT first (exact match)
    for etapa_candidat in CURSOS_ESOBAT:
        idx = after_academic.find(etapa_candidat)
        if idx == -1:
            continue
        # Extract curs_codi: everything up to end of etapa_candidat
        curs_codi = after_academic[:idx + len(etapa_candidat)]
        curs = after_academic[:idx]
        rest_after = after_academic[idx + len(etapa_candidat):]
        if rest_after.startswith("_"):
            grup = rest_after[1:]
        else:
            grup = rest_after
        etapa = etapa_candidat
        break

    # Try PDC/APLI if ESO/BAT not found
    if not etapa:
        for especial in CURSOS_ESPECIALS:
            idx = after_academic.find(especial)
            if idx == -1:
                continue
            curs_codi = after_academic[:idx + len(especial)]
            curs = after_academic[:idx]
            rest_after = after_academic[idx + len(especial):]
            if rest_after.startswith("_"):
                grup = rest_after[1:]
            else:
                grup = rest_after
            etapa = "ESO"
            break

    if not etapa:
        return None

    return {
        "curs_academic": curs_academic,
        "curs": curs,
        "curs_codi": curs_codi,
        "etapa": etapa,
        "grup": grup if grup else "",
        "materia": materia,
        "estat": estat,
        "filename": filename,
        "tipus": "ESOBAT",
    }


def get_expected(config):
    expected = []
    for cicle_codi, cicle_data in config["cicles"].items():
        for curs, curs_data in cicle_data["cursos"].items():
            for modul in curs_data["moduls"]:
                for grup in curs_data.get("grups", [""]):
                    expected.append({
                        "cicle": cicle_codi,
                        "curs": curs,
                        "grup": grup,
                        "modul_codi": modul["codi"],
                        "modul_nom": modul["nom"],
                    })
    return expected


def get_expected_esobat(config):
    expected = []
    for curs_codi, curs_data in config["cursos"].items():
        grups_curs = curs_data.get("grups", [""])
        for materia in curs_data["materies"]:
            grups = materia.get("grups", grups_curs)
            for grup in grups:
                expected.append({
                    "curs_codi": curs_codi,
                    "curs_nom": curs_data["nom"],
                    "etapa": curs_data["etapa"],
                    "grup": grup,
                    "materia_codi": materia["codi"],
                    "materia_nom": materia["nom"],
                })
    return expected


def check_placeholders(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    # Ignore blockquote lines (> ...), they are stripped at compile time
    content = re.sub(r'(?:^|\n)[ \t]*>.*(?:\n[ \t]*>.*)*', '', content)
    remaining = re.findall(r"\[###\]|\[\.\.\.\]|\[NOMDELPROFESSOR", content)

    # Check for zero stats (aprovats i suspensos ambdós a 0)
    aprov_zero = re.search(r'^\|\s*Aprovats(?:\s*/\s*[^|]*)?\s*\|\s*0\s*\|$', content, re.MULTILINE)
    susp_zero = re.search(r'^\|\s*Suspensos(?:\s*/\s*[^|]*)?\s*\|\s*0\s*\|$', content, re.MULTILINE)
    if aprov_zero and susp_zero:
        remaining.append("[ZERO_STATS]")

    # Detect non-standard checkbox fills: [ x ], [x ], [ x ], etc.
    # Valid formats: [x] or [X] (with or without uppercase, no extra spaces)
    all_filled = re.findall(r"\[\s*[xX]\s*\]", content)
    non_standard = [m for m in all_filled if len(m) > 3]
    if non_standard:
        remaining.append("[CHECKBOX_FORMAT]")

    return remaining


STATS_PATTERNS_ESOBAT = {
    "inici": re.compile(r'^\|\s*Nº d\'alumnes a inici de curs\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
    "final": re.compile(r'^\|\s*Nº d\'alumnes a final de curs\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
    "avaluats": re.compile(r'^\|\s*Alumnat avaluat\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
    "aprovats": re.compile(r'^\|\s*Aprovats(?:\s*/\s*[^|]*)?\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
    "suspensos": re.compile(r'^\|\s*Suspensos(?:\s*/\s*[^|]*)?\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
    "absents": re.compile(r'^\|\s*No avaluable\s*/\s*absentisme\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
}

STATS_PATTERNS_FP = {
    "inici": re.compile(r'^\|\s*Nº d\'alumnes a inici de curs\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
    "final": re.compile(r'^\|\s*Nº d\'alumnes a final de curs\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
    "aprovats": re.compile(r'^\|\s*Aprovats\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
    "suspensos": re.compile(r'^\|\s*Suspensos\s*\|\s*(\d+|\[###\])\s*\|$', re.MULTILINE),
}


def check_stats_consistency(filepath, is_esobat):
    issues = []
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'(?:^|\n)[ \t]*>.*(?:\n[ \t]*>.*)*', '', content)

    patterns = STATS_PATTERNS_ESOBAT if is_esobat else STATS_PATTERNS_FP
    stats = {}
    for key, pat in patterns.items():
        m = pat.search(content)
        if m and m.group(1).isdigit():
            stats[key] = int(m.group(1))

    if not stats:
        return issues

    if is_esobat:
        if "avaluats" in stats and "aprovats" in stats and "suspensos" in stats:
            if stats["aprovats"] + stats["suspensos"] > stats["avaluats"]:
                issues.append("aprovats + suspensos > alumnat avaluat")
        if "final" in stats and "aprovats" in stats and "suspensos" in stats:
            total_class = stats["aprovats"] + stats["suspensos"]
            if "absents" in stats:
                total_class += stats["absents"]
            if total_class > stats["final"]:
                issues.append("total alumnes (aprovats + suspensos + absents) > final de curs")
        if "avaluats" in stats and "final" in stats:
            if stats["avaluats"] > stats["final"]:
                issues.append("alumnat avaluat > alumnes a final de curs")
        if "inici" in stats and "final" in stats:
            if stats["final"] > stats["inici"]:
                issues.append("final de curs > inici de curs (possibles incorporacions)")
    else:
        if "final" in stats and "aprovats" in stats and "suspensos" in stats:
            if stats["aprovats"] + stats["suspensos"] > stats["final"]:
                issues.append("aprovats + suspensos > alumnes a final de curs")
        if "inici" in stats and "final" in stats:
            if stats["final"] > stats["inici"]:
                issues.append("final de curs > inici de curs (possibles incorporacions)")

    return issues


def get_annex_status(familia, output_parent="memories_FP"):
    """Check if annex file exists and its status for a given family."""
    annex_dir = os.path.join(PROJECT_DIR, output_parent, familia)
    if not os.path.isdir(annex_dir):
        return None, []
    annex_files = [f for f in os.listdir(annex_dir) if is_annex_file(f)]
    if not annex_files:
        return None, []
    status = "OK" if any(f.endswith("_OK.md") for f in annex_files) else "BORRADOR"
    return status, sorted(annex_files)


def build_report_lines(familia, config, parsed, expected, output_parent="memories_FP"):
    curs_academic = config["curs"]
    centre = config["centre"]
    departament = config["departament"]
    is_esobat = "cursos" in config

    def exp_key(e):
        if is_esobat:
            return (e.get("curs_codi"), e.get("grup", ""), e.get("materia_codi"))
        return (e["cicle"], e["curs"], e.get("grup", ""), e["modul_codi"])

    def parsed_key(p):
        if is_esobat:
            return (p.get("curs_codi", p.get("curs", "") + p.get("etapa", "")), p.get("grup", ""), p.get("materia"))
        return (p["cicle"], p["curs"], p.get("grup", ""), p["modul"])

    def exp_label(e):
        if is_esobat:
            return f"{e.get('curs_codi','')} {e.get('grup','')} - {e['materia_codi']} ({e['materia_nom']})".strip()
        label = f"{e['cicle']} {curs_display(e.get('curs',''))}"
        if e.get("grup"):
            label += f" {e['grup']}"
        label += f" - {e['modul_codi']} ({e['modul_nom']})"
        return label

    def parsed_label(p):
        if is_esobat:
            return f"{p.get('curs_codi','')} {p.get('grup','')} - {p.get('materia','')}".strip()
        label = f"{p['cicle']} {curs_display(p.get('curs',''))}"
        if p.get("grup"):
            label += f" {p['grup']}"
        label += f" - {p.get('modul','')}"
        return label

    ok_files = [p for p in parsed if p["estat"] == "OK"]
    borrador_files = [p for p in parsed if p["estat"] == "BORRADOR"]

    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append(f"REPORT DE MEMÒRIES - {departament} - Curs {curs_academic}")
    report_lines.append(f"Centre: {centre}")
    report_lines.append("=" * 60)

    ok_keys = {parsed_key(p) for p in ok_files}
    borrador_keys = {parsed_key(p) for p in borrador_files}

    missing = []
    complete_pending_list = []

    # Detect duplicates: same module with both OK and BORRADOR
    duplicated_keys = ok_keys & borrador_keys
    duplicates = []
    for p in parsed:
        key = parsed_key(p)
        if key in duplicated_keys and p["estat"] == "BORRADOR":
            duplicates.append(p)

    report_lines.append(f"\n--- Llegits {len(parsed)} fitxers a {output_parent}_{familia} ---")
    report_lines.append(f"  Completats (OK): {len(ok_files)}")
    report_lines.append(f"  Pendents (BORRADOR): {len(borrador_files)}")
    if duplicates:
        report_lines.append(f"  AVÍS: {len(duplicates)} mòduls tenen fitxer OK i BORRADOR (possible còpia en lloc de renombrar)")
    report_lines.append("")

    for exp in expected:
        key = exp_key(exp)
        if key in ok_keys:
            continue
        if key in borrador_keys and key not in duplicated_keys:
            complete_pending_list.append(exp)
        elif key not in borrador_keys:
            missing.append(exp)

    if duplicates:
        report_lines.append("MÒDULS AMB FITXER OK I BORRADOR (posible duplicat):")
        report_lines.append("-" * 40)
        for p in sorted(duplicates, key=parsed_key):
            report_lines.append(f"  [DUPLICAT] {parsed_label(p)}")
        report_lines.append("  Reviseu els dos fitxers, conserveu el correcte amb sufix _OK i esborreu l'altre")
        report_lines.append("")

    if missing:
        report_lines.append("MÒDULS NO PRESENTS (ni OK ni BORRADOR):")
        report_lines.append("-" * 40)
        for exp in sorted(missing, key=exp_key):
            report_lines.append(f"  [FALTA] {exp_label(exp)}")
        report_lines.append("")

    if complete_pending_list:
        report_lines.append("MÒDULS EN ESTAT BORRADOR (pendents de completar):")
        report_lines.append("-" * 40)
        for exp in sorted(complete_pending_list, key=exp_key):
            report_lines.append(f"  [BORRADOR] {exp_label(exp)}")
        report_lines.append("")

    incomplete_ok = []
    for p in ok_files:
        filepath = os.path.join(PROJECT_DIR, output_parent, familia, p["filename"])
        remaining = check_placeholders(filepath)
        stats_issues = check_stats_consistency(filepath, is_esobat)
        if remaining or stats_issues:
            incomplete_ok.append((p, remaining, stats_issues))

    if incomplete_ok:
        report_lines.append("MÒDULS OK AMB CAMPS PER OMPLIR o INCONGRUÈNCIES:")
        report_lines.append("-" * 40)
        custom_markers = {"[ZERO_STATS]", "[CHECKBOX_FORMAT]"}
        for p, rem, stats_issues in incomplete_ok:
            parts = []
            ph_count = len([r for r in rem if r not in custom_markers])
            if ph_count:
                parts.append(f"{ph_count} marcadors pendents")
            if "[ZERO_STATS]" in rem:
                parts.append("estadístiques amb 0 aprovats i 0 suspensos")
            if "[CHECKBOX_FORMAT]" in rem:
                parts.append("caselles marcades amb format incorrecte (useu [x] sense espais)")
            parts.extend(stats_issues)
            msg = " — ".join(parts) if parts else f"{len(rem)} marcadors restants"
            report_lines.append(f"  [INCOMPLET] {parsed_label(p)} — {msg}")
        report_lines.append("")

    # Annex d'activitats extraescolars
    annex_status, annex_files = get_annex_status(familia, output_parent)
    report_lines.append("ANNEX ACTIVITATS EXTRAESCOLARS:")
    report_lines.append("-" * 40)
    if annex_status:
        for f in annex_files:
            label = "OK" if f.endswith("_OK.md") else "BORRADOR"
            report_lines.append(f"  [{label}] {f}")
    else:
        report_lines.append("  No present / No s'ha generat")
    if is_esobat:
        report_lines.append("  (ESO/BAT: no s'inclou en la compilació del PDF)")
    report_lines.append("")

    report_lines.append("=" * 60)
    report_lines.append("FI DEL REPORT")
    report_lines.append("=" * 60)

    return report_lines, ok_files, borrador_files, missing, incomplete_ok
