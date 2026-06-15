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
from memories_utils import parse_filename, get_expected, build_report_lines


def main():
    familia = sys.argv[1].upper() if len(sys.argv) > 1 else "INF"
    centre_educatiu = sys.argv[2] if len(sys.argv) > 2 else "SENIA"

    config_path = os.path.join(PROJECT_DIR, "memoria", f"memories_{familia}.json")
    if not os.path.exists(config_path):
        print(f"Error: no es troba {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    memories_dir = os.path.join(PROJECT_DIR, f"memories_{familia}")
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

    expected = get_expected(config)

    report_lines, _, _, _, _ = build_report_lines(familia, config, parsed, expected)

    report_text = "\n".join(report_lines)
    print(report_text)

    report_path = os.path.join(pdf_dir, f"report_memories_{familia}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\nReport guardat a: {report_path}")


if __name__ == "__main__":
    main()
