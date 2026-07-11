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


def compute_status(cicle, familia, plantilles_dir):
    """Recull l'estat brut d'un cicle: PDs BORRADOR/OK, placeholders pendents
    i coherència de l'Excel. Base compartida pel report de text i per
    decidir si el cicle es pot considerar verificat (is_verified)."""
    cicle = cicle.upper()
    familia = familia.upper()

    status = {
        "cicle": cicle,
        "familia": familia,
        "plantilles_dir": plantilles_dir,
        "dir_found": os.path.isdir(plantilles_dir),
        "borrador": [],
        "ok": [],
        "placeholders": [],
        "total_places": 0,
        "excel_path": os.path.join(plantilles_dir, f"libro_{cicle}.xlsx"),
        "excel_issues": [],
    }
    if not status["dir_found"]:
        return status

    pd_files = sorted([f for f in os.listdir(plantilles_dir) if f.endswith('.md') and f.startswith('PD_')])
    for f in pd_files:
        parsed = parse_pd_filename(f)
        if parsed:
            if parsed['estat'] == 'BORRADOR':
                status["borrador"].append(parsed)
            elif parsed['estat'] == 'OK':
                status["ok"].append(parsed)

    all_md = sorted([f for f in os.listdir(plantilles_dir) if f.endswith('.md') and not f.startswith('out.')])
    for f in all_md:
        fp = os.path.join(plantilles_dir, f)
        places = find_placeholders(fp)
        if places:
            status["placeholders"].append((f, places))
            status["total_places"] += len(places)

    status["excel_issues"] = check_excel_coherence(status["excel_path"])
    return status


def is_verified(status):
    """Un cicle es considera verificat (sense marca d'aigua ESBORRANY) quan
    no queda cap PD en BORRADOR, cap placeholder [###]/[...] pendent, i
    l'Excel de pesos RA és coherent."""
    if not status["dir_found"]:
        return False
    if status["borrador"]:
        return False
    if status["total_places"] > 0:
        return False
    if status["excel_issues"]:
        return False
    return True


def format_report(status):
    lines = []
    lines.append(f"=== Report PCCF: {status['cicle']} (Família {status['familia']}) ===")
    lines.append(f"Directori: {status['plantilles_dir']}/\n")

    if not status["dir_found"]:
        lines.append(f"ERROR: Directori no trobat: {status['plantilles_dir']}")
        return "\n".join(lines)

    # 1. PD status summary
    lines.append(f"PDs en BORRADOR: {len(status['borrador'])}")
    for p in status["borrador"]:
        lines.append(f"  - {p['nom']} ({p['codi']})")
    lines.append(f"PDs en OK: {len(status['ok'])}")
    for p in status["ok"]:
        lines.append(f"  - {p['nom']} ({p['codi']})")
    lines.append("")

    # 2. Placeholder check
    for f, places in status["placeholders"]:
        lines.append(f"  {f} ({len(places)} marques pendents):")
        for ln, ct in places[:10]:
            lines.append(f"    L{ln}: {ct}")
        if len(places) > 10:
            lines.append(f"    ... i {len(places) - 10} marques més")
        lines.append("")

    if status["total_places"] == 0:
        lines.append("  [###]: Cap marca pendent.\n")
    else:
        lines.append(f"  [###]: {status['total_places']} marques en {len(status['placeholders'])} fitxers.\n")

    # 3. Excel coherence
    lines.append(f"Excel: {status['excel_path']}")
    if status["excel_issues"]:
        for e in status["excel_issues"]:
            lines.append(f"  {e}")
    else:
        lines.append("  Correcte (RA suma 100% o Excel no trobat/sense dades).")
    lines.append("")

    lines.append(f"Verificat (sense marca d'esborrany): {'SI' if is_verified(status) else 'NO'}")

    return "\n".join(lines)


def report(cicle, familia, plantilles_dir):
    return format_report(compute_status(cicle, familia, plantilles_dir))


def main():
    if len(sys.argv) < 2:
        print("Ús: python3 tools/report_pccf.py <CICLO> [pd_dir] [pccf_root]")
        print("  pccf_root: directori arrel que conté 0_report_pccf/ (per defecte '.')")
        sys.exit(1)

    cicle = sys.argv[1].upper()
    familia = get_familia(cicle) or "INF"
    if len(sys.argv) > 2:
        pd_dir = sys.argv[2]
    else:
        pd_dir = f"programacions/{cicle}"

    pccf_root = sys.argv[3] if len(sys.argv) > 3 else "."

    report_text = report(cicle, familia, pd_dir)
    print(report_text)

    report_dir = os.path.join(pccf_root, "0_report_pccf")
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{familia}_{cicle}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"Report guardat a: {report_path}")


if __name__ == "__main__":
    main()
