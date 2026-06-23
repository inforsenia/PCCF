#!/usr/bin/env python3

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pccf_utils import parse_pd_filename, check_excel_coherence, get_familia

PLACEHOLDER_RE = re.compile(r'\[#+#\]|\[\.\.\.\]')


def find_placeholders(filepath):
    places = []
    with open(filepath, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            stripped = line.strip()
            if not PLACEHOLDER_RE.search(stripped):
                continue
            if stripped.startswith('>') and '`[###]`' in stripped:
                continue
            places.append((i, stripped[:120]))
    return places


def report(cicle, familia, plantilles_dir):
    cicle = cicle.upper()
    familia = familia.upper()
    lines = []
    lines.append(f"=== Report PCCF: {cicle} (Família {familia}) ===")
    lines.append(f"Directori: {plantilles_dir}/\n")

    if not os.path.isdir(plantilles_dir):
        lines.append(f"ERROR: Directori no trobat: {plantilles_dir}")
        return "\n".join(lines)

    # 1. PD status summary
    pd_files = sorted([f for f in os.listdir(plantilles_dir) if f.endswith('.md') and f.startswith('PD_')])
    borrador = []
    ok = []
    for f in pd_files:
        parsed = parse_pd_filename(f)
        if parsed:
            if parsed['estat'] == 'BORRADOR':
                borrador.append(parsed)
            elif parsed['estat'] == 'OK':
                ok.append(parsed)

    lines.append(f"PDs en BORRADOR: {len(borrador)}")
    for p in borrador:
        lines.append(f"  - {p['nom']} ({p['codi']})")
    lines.append(f"PDs en OK: {len(ok)}")
    for p in ok:
        lines.append(f"  - {p['nom']} ({p['codi']})")
    lines.append("")

    # 2. Placeholder check
    all_md = sorted([f for f in os.listdir(plantilles_dir) if f.endswith('.md') and not f.startswith('out.')])
    total_places = 0
    files_with_places = 0
    for f in all_md:
        fp = os.path.join(plantilles_dir, f)
        places = find_placeholders(fp)
        if places:
            files_with_places += 1
            total_places += len(places)
            lines.append(f"  {f} ({len(places)} marques pendents):")
            for ln, ct in places[:10]:
                lines.append(f"    L{ln}: {ct}")
            if len(places) > 10:
                lines.append(f"    ... i {len(places) - 10} marques més")
            lines.append("")

    if total_places == 0:
        lines.append("  [###]: Cap marca pendent.\n")
    else:
        lines.append(f"  [###]: {total_places} marques en {files_with_places} fitxers.\n")

    # 3. Excel coherence
    excel_path = os.path.join(plantilles_dir, f"libro_{cicle}.xlsx")
    lines.append(f"Excel: {excel_path}")
    excel_issues = check_excel_coherence(excel_path)
    if excel_issues:
        for e in excel_issues:
            lines.append(f"  {e}")
    else:
        lines.append("  Correcte (RA suma 100% o Excel no trobat/sense dades).")
    lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Ús: python3 tools/report_pccf.py <CICLO> [plantilles_dir]")
        print("  Si no es dona plantilles_dir, es dedueix: plantilles_{FAMILIA}_{CICLO}/")
        sys.exit(1)

    cicle = sys.argv[1].upper()
    familia = get_familia(cicle) or "INF"
    if len(sys.argv) > 2:
        plantilles_dir = sys.argv[2]
    else:
        plantilles_dir = f"plantilles_{familia}_{cicle}"

    report_text = report(cicle, familia, plantilles_dir)
    print(report_text)

    pdf_dir = "PDFS"
    os.makedirs(pdf_dir, exist_ok=True)
    report_path = os.path.join(pdf_dir, f"report_pccf_{familia}_{cicle}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"Report guardat a: {report_path}")


if __name__ == "__main__":
    main()
