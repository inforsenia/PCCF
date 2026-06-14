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
        return None

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


def check_placeholders(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    remaining = re.findall(r"\[###\]|\[\.\.\.\]|\[NOMDELPROFESSOR", content)
    return remaining


def build_report_lines(familia, config, parsed, expected):
    curs_academic = config["curs"]
    centre = config["centre"]
    departament = config["departament"]

    ok_files = [p for p in parsed if p["estat"] == "OK"]
    borrador_files = [p for p in parsed if p["estat"] == "BORRADOR"]

    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append(f"REPORT DE MEMÒRIES - {departament} - Curs {curs_academic}")
    report_lines.append(f"Centre: {centre}")
    report_lines.append("=" * 60)

    ok_keys = set()
    for p in ok_files:
        ok_keys.add((p["cicle"], p["curs"], p["grup"], p["modul"]))

    borrador_keys = set()
    for p in borrador_files:
        borrador_keys.add((p["cicle"], p["curs"], p["grup"], p["modul"]))

    missing = []
    complete_pending_list = []

    # Detect duplicates: same module with both OK and BORRADOR
    duplicated_keys = ok_keys & borrador_keys
    duplicates = []
    for p in parsed:
        key = (p["cicle"], p["curs"], p["grup"], p["modul"])
        if key in duplicated_keys and p["estat"] == "BORRADOR":
            duplicates.append(p)

    report_lines.append(f"\n--- Llegits {len(parsed)} fitxers a memories_md/ ---")
    report_lines.append(f"  Completats (OK): {len(ok_files)}")
    report_lines.append(f"  Pendents (BORRADOR): {len(borrador_files)}")
    if duplicates:
        report_lines.append(f"  AVÍS: {len(duplicates)} mòduls tenen fitxer OK i BORRADOR (possible còpia en lloc de renombrar)")
    report_lines.append("")

    for exp in expected:
        key = (exp["cicle"], exp["curs"], exp["grup"], exp["modul_codi"])
        if key in ok_keys:
            continue
        if key in borrador_keys and key not in duplicated_keys:
            complete_pending_list.append(exp)
        elif key not in borrador_keys:
            missing.append(exp)

    if duplicates:
        report_lines.append("MÒDULS AMB FITXER OK I BORRADOR (posible duplicat):")
        report_lines.append("-" * 40)
        for p in sorted(duplicates, key=lambda x: (x["cicle"], x["curs"], x["grup"], x["modul"])):
            label = f"{p['cicle']} {curs_display(p['curs'])}"
            if p["grup"]:
                label += f" {p['grup']}"
            label += f" - {p['modul']}"
            report_lines.append(f"  [DUPLICAT] {label}")
        report_lines.append("  (Conservau el fitxer OK i esborreu el BORRADOR)")
        report_lines.append("")

    if missing:
        report_lines.append("MÒDULS NO PRESENTS (ni OK ni BORRADOR):")
        report_lines.append("-" * 40)
        for exp in sorted(missing, key=lambda x: (x["cicle"], x["curs"], x["grup"])):
            label = f"{exp['cicle']} {curs_display(exp['curs'])}"
            if exp["grup"]:
                label += f" {exp['grup']}"
            label += f" - {exp['modul_codi']} ({exp['modul_nom']})"
            report_lines.append(f"  [FALTA] {label}")
        report_lines.append("")

    if complete_pending_list:
        report_lines.append("MÒDULS EN ESTAT BORRADOR (pendents de completar):")
        report_lines.append("-" * 40)
        for exp in sorted(complete_pending_list, key=lambda x: (x["cicle"], x["curs"], x["grup"])):
            label = f"{exp['cicle']} {curs_display(exp['curs'])}"
            if exp["grup"]:
                label += f" {exp['grup']}"
            label += f" - {exp['modul_codi']} ({exp['modul_nom']})"
            report_lines.append(f"  [BORRADOR] {label}")
        report_lines.append("")

    incomplete_ok = []
    for p in ok_files:
        filepath = os.path.join(PROJECT_DIR, "memories_md", p["filename"])
        remaining = check_placeholders(filepath)
        if remaining:
            incomplete_ok.append((p, remaining))

    if incomplete_ok:
        report_lines.append("MÒDULS OK AMB CAMPS PER OMPLIR (contenen [###] o [...]):")
        report_lines.append("-" * 40)
        for p, rem in incomplete_ok:
            label = f"{p['cicle']} {curs_display(p['curs'])}"
            if p["grup"]:
                label += f" {p['grup']}"
            label += f" - {p['modul']}"
            report_lines.append(f"  [INCOMPLET] {label} ({len(rem)} marcadors restants)")
        report_lines.append("")

    report_lines.append("=" * 60)
    report_lines.append("FI DEL REPORT")
    report_lines.append("=" * 60)

    return report_lines, ok_files, borrador_files, missing, incomplete_ok
