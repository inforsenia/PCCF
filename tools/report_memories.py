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
from memories_utils import parse_filename, get_expected, get_expected_esobat, build_report_lines, get_output_parent


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

    pdf_dir = os.path.join(PROJECT_DIR, "PDFS")
    os.makedirs(pdf_dir, exist_ok=True)

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

    report_text = "\n".join(report_lines)
    print(report_text)

    report_prefix = base_dir.replace("memoria", "", 1)
    report_path = os.path.join(pdf_dir, f"report_memories_{report_prefix}_{familia}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\nReport guardat a: {report_path}")


if __name__ == "__main__":
    main()
