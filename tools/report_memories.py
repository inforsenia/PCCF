#!/usr/bin/env python3

"""
Genera un report de l'estat de les memòries sense compilar el PDF.

Ús: python3 tools/report_memories.py [família] [centre_educatiu]

Per defecte: família = INF, centre_educatiu = SENIA
"""

import sys
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

sys.path.insert(0, SCRIPT_DIR)
from memories_utils import parse_filename, get_expected, get_expected_esobat, build_report_lines, get_output_parent, normalitza_fitxers, get_report_dir


def main():
    familia = "INF"
    centre_educatiu = "SENIA"
    base_dir = "memoriaFP"

    args = sys.argv[1:]
    if "--base-dir" in args:
        idx = args.index("--base-dir")
        if idx + 1 < len(args):
            base_dir = args[idx + 1]
            args = args[:idx] + args[idx+2:]

    if len(args) > 0:
        familia = args[0].upper()
    if len(args) > 1:
        centre_educatiu = args[1]

    config_path = os.path.join(PROJECT_DIR, base_dir, f"memories_{familia}.json")
    if not os.path.exists(config_path):
        print(f"Error: no es troba {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    output_parent = get_output_parent(base_dir)
    memories_dir = os.path.join(PROJECT_DIR, output_parent, familia)
    if not os.path.exists(memories_dir):
        print(f"Error: no es troba el directori {memories_dir}")
        sys.exit(1)

    # Normalitzar noms abans de parsejar
    renamed, issues = normalitza_fitxers(memories_dir)
    for old_n, new_n in renamed:
        print(f"  Renombrat: {old_n} → {new_n}")

    all_files = sorted(os.listdir(memories_dir))
    parsed = []
    for f in all_files:
        info = parse_filename(f)
        if info:
            parsed.append(info)

    if "cicles" in config:
        expected = get_expected(config)
    else:
        expected = get_expected_esobat(config)

    report_lines, _, _, _, _ = build_report_lines(familia, config, parsed, expected, output_parent)

    # Afegir secció de noms incorrectes al report
    if issues:
        report_lines.insert(1, "")
        report_lines.insert(1, f"  AVÍS: {len(issues)} fitxers amb nom incorrecte (revisau més avall)")
        report_lines.append("")
        report_lines.append("FITXERS AMB NOMS INCORRECTES (cal revisió del docent):")
        report_lines.append("-" * 40)
        for fname, tipus in issues:
            if tipus == "BORR_TRUNCAT":
                report_lines.append(f"  [BORR_TRUNCAT] {fname} — El nom hauria d'acabar en _BORRADOR.md")
            elif tipus == "SENSE_SUFIX":
                report_lines.append(f"  [SENSE_SUFIX] {fname} — Afegiu _OK o _BORRADOR al nom del fitxer")
        report_lines.append("")

    report_text = "\n".join(report_lines)
    print(report_text)

    report_dir = get_report_dir(base_dir)
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{familia}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\nReport guardat a: {report_path}")


if __name__ == "__main__":
    main()
