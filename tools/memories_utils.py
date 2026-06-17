#!/usr/bin/env python3

"""
Funcions compartides per a la gestió de memòries (report i compilació).
"""

import os
import re
import json

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
    return f"{curs}r"


def parse_filename_esobat(filename):
    """Parse ESO/BAT filename: {curs_acad}_{curs}{etapa}{grup}_{materia}_{estat}.md
    
    Example: 25_26_1ESOA_ANGLES_BORRADOR.md → curs=1, etapa=ESO, grup=A, materia=ANGLES
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
    # rest = {curs_academic}_{curs}{etapa}{grup}
    if len(rest) < 6 or rest[2] != "_":
        return None
    curs_academic = rest[:5]
    after_academic = rest[6:]

    curs = ""
    etapa = ""
    grup = ""

    for etapa_candidat in CURSOS_ESOBAT:
        idx = after_academic.find(etapa_candidat)
        if idx == -1:
            continue
        curs = after_academic[:idx]
        rest_after_etapa = after_academic[idx + len(etapa_candidat):]
        if rest_after_etapa.startswith("_"):
            grup = rest_after_etapa[1:]
        else:
            grup = rest_after_etapa
        etapa = etapa_candidat
        break

    if not etapa:
        return None

    return {
        "curs_academic": curs_academic,
        "curs": curs,
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
        for materia in curs_data["materies"]:
            for grup in curs_data.get("grups", [""]):
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
    return remaining


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
            # Combine curs + etapa to match curs_codi format (e.g. "1"+"ESO" → "1ESO")
            return (p.get("curs", "") + p.get("etapa", ""), p.get("grup", ""), p.get("materia"))
        return (p["cicle"], p["curs"], p.get("grup", ""), p["modul"])

    def exp_label(e):
        if is_esobat:
            return f"{e.get('etapa','')} {e.get('curs_codi','')} {e.get('grup','')} - {e['materia_codi']} ({e['materia_nom']})".strip()
        label = f"{e['cicle']} {curs_display(e.get('curs',''))}"
        if e.get("grup"):
            label += f" {e['grup']}"
        label += f" - {e['modul_codi']} ({e['modul_nom']})"
        return label

    def parsed_label(p):
        if is_esobat:
            return f"{p.get('etapa','')} {p.get('curs','')} {p.get('grup','')} - {p.get('materia','')}".strip()
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

    report_lines.append(f"\n--- Llegits {len(parsed)} fitxers a {output_parent}/{familia}/ ---")
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
        report_lines.append("  (Conservau el fitxer OK i esborreu el BORRADOR)")
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
        if remaining:
            incomplete_ok.append((p, remaining))

    if incomplete_ok:
        report_lines.append("MÒDULS OK AMB CAMPS PER OMPLIR (contenen [###] o [...]):")
        report_lines.append("-" * 40)
        for p, rem in incomplete_ok:
            report_lines.append(f"  [INCOMPLET] {parsed_label(p)} ({len(rem)} marcadors restants)")
        report_lines.append("")

    # Annex d'activitats extraescolars
    annex_status, annex_files = get_annex_status(familia, output_parent)
    if annex_status:
        report_lines.append("ANNEX ACTIVITATS EXTRAESCOLARS:")
        report_lines.append("-" * 40)
        for f in annex_files:
            label = "OK" if f.endswith("_OK.md") else "BORRADOR"
            report_lines.append(f"  [{label}] {f}")
        report_lines.append("")

    report_lines.append("=" * 60)
    report_lines.append("FI DEL REPORT")
    report_lines.append("=" * 60)

    return report_lines, ok_files, borrador_files, missing, incomplete_ok
