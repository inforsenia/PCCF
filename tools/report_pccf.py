#!/usr/bin/env python3

import argparse
import os
import re
import sys

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


def compute_pd_status(cicle, familia, pd_dir):
    status = {
        "cicle": cicle,
        "familia": familia,
        "pd_dir": pd_dir,
        "dir_found": os.path.isdir(pd_dir),
        "borrador": [],
        "ok": [],
        "placeholders": [],
        "total_places": 0,
        "excel_path": os.path.join(pd_dir, f"libro_{cicle}.xlsx"),
        "excel_issues": [],
    }
    if not status["dir_found"]:
        return status

    pd_files = sorted([f for f in os.listdir(pd_dir) if f.endswith('.md') and f.startswith('PD_')])
    for f in pd_files:
        parsed = parse_pd_filename(f)
        if parsed:
            if parsed['estat'] == 'BORRADOR':
                status["borrador"].append(parsed)
            elif parsed['estat'] == 'OK':
                status["ok"].append(parsed)

    all_md = sorted([f for f in os.listdir(pd_dir) if f.endswith('.md') and not f.startswith('out.')])
    for f in all_md:
        fp = os.path.join(pd_dir, f)
        places = find_placeholders(fp)
        if places:
            status["placeholders"].append((f, places))
            status["total_places"] += len(places)

    status["excel_issues"] = check_excel_coherence(status["excel_path"])
    return status


def compute_pccf_status(cicle, familia, pccf_dir):
    status = {
        "cicle": cicle,
        "familia": familia,
        "pccf_dir": pccf_dir,
        "dir_found": os.path.isdir(pccf_dir),
        "missing_src_dirs": [],
        "pccf_count": 0,
        "placeholders": [],
        "total_places": 0,
    }
    if not status["dir_found"]:
        return status

    for d in [f"src", f"src_{familia}", f"src_{familia}_{cicle}"]:
        dd = os.path.join(pccf_dir, d)
        if not os.path.isdir(dd):
            status["missing_src_dirs"].append(d)

    for root, _dirs, files in os.walk(pccf_dir):
        for f in sorted(files):
            if f.startswith("PCCF_") and f.endswith(".md"):
                status["pccf_count"] += 1
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, pccf_dir)
                places = find_placeholders(fp)
                if places:
                    status["placeholders"].append((rel, places))
                    status["total_places"] += len(places)

    return status


def is_pd_verified(status):
    if not status["dir_found"]:
        return False
    if status["borrador"]:
        return False
    if status["total_places"] > 0:
        return False
    if status["excel_issues"]:
        return False
    return True


def is_pccf_verified(status):
    if not status["dir_found"]:
        return False
    if status["total_places"] > 0:
        return False
    return True


def format_pd_report(status):
    lines = []
    lines.append(f"=== Report Programacions Didàctiques: {status['cicle']} (Família {status['familia']}) ===")
    lines.append(f"Directori: {status['pd_dir']}/\n")

    if not status["dir_found"]:
        lines.append(f"ERROR: Directori no trobat: {status['pd_dir']}")
        return "\n".join(lines)

    lines.append(f"PDs en BORRADOR: {len(status['borrador'])}")
    for p in status["borrador"]:
        lines.append(f"  - {p['nom']} ({p['codi']})")
    lines.append(f"PDs en OK: {len(status['ok'])}")
    for p in status["ok"]:
        lines.append(f"  - {p['nom']} ({p['codi']})")
    lines.append("")

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

    lines.append(f"Excel: {status['excel_path']}")
    if status["excel_issues"]:
        for e in status["excel_issues"]:
            lines.append(f"  {e}")
    else:
        lines.append("  Correcte (RA suma 100% o Excel no trobat/sense dades).")
    lines.append("")

    lines.append(f"Verificat (sense marca d'esborrany): {'SI' if is_pd_verified(status) else 'NO'}")

    return "\n".join(lines)


def format_pccf_report(status):
    lines = []
    lines.append(f"=== Report Framework PCCF: {status['cicle']} (Família {status['familia']}) ===")
    lines.append(f"Directori: {status['pccf_dir']}/\n")

    if not status["dir_found"]:
        lines.append(f"ERROR: Directori no trobat: {status['pccf_dir']}")
        return "\n".join(lines)

    lines.append(f"Directoris src esperats:")
    for d in [f"src", f"src_{status['familia']}", f"src_{status['familia']}_{status['cicle']}"]:
        dd = os.path.join(status['pccf_dir'], d)
        present = "✓" if os.path.isdir(dd) else "✗"
        lines.append(f"  {present} {d}/")

    lines.append(f"\nFitxers PCCF_*.md trobats: {status['pccf_count']}")

    for f, places in status["placeholders"]:
        lines.append(f"  {f} ({len(places)} marques pendents):")
        for ln, ct in places[:10]:
            lines.append(f"    L{ln}: {ct}")
        if len(places) > 10:
            lines.append(f"    ... i {len(places) - 10} marques més")
        lines.append("")

    if status["total_places"] == 0:
        lines.append("  [###]: Cap marca pendent en fitxers PCCF.\n")
    else:
        lines.append(f"  [###]: {status['total_places']} marques en {len(status['placeholders'])} fitxers.\n")

    lines.append(f"Verificat (sense marca d'esborrany): {'SI' if is_pccf_verified(status) else 'NO'}")

    return "\n".join(lines)


def report_pd(cicle, familia, pd_dir):
    return format_pd_report(compute_pd_status(cicle, familia, pd_dir))


def report_pccf(cicle, familia, pccf_dir):
    return format_pccf_report(compute_pccf_status(cicle, familia, pccf_dir))


def main():
    parser = argparse.ArgumentParser(description="Genera report de PCCF o Programacions")
    parser.add_argument("cicle", help="Cicle (ex: APD)")
    parser.add_argument("--type", choices=["pd", "pccf"], default="pd",
                        help="Tipus de report: pd (PD + Excel, dins programacions/) o pccf (framework, dins pccf/)")
    parser.add_argument("--pd-dir", help="Directori de les PD (ex: programacions/APD)")
    parser.add_argument("--pccf-dir", default=os.environ.get("PCCF_ROOT", ".") + "/pccf",
                        help="Directori del framework PCCF (conté src*/)")
    parser.add_argument("--centre", default="SENIA")
    args = parser.parse_args()

    cicle = args.cicle.upper()
    familia = get_familia(cicle) or "INF"

    if args.type == "pd":
        pd_dir = args.pd_dir or f"programacions/{cicle}"
        status = compute_pd_status(cicle, familia, pd_dir)
        report_text = format_pd_report(status)
        report_dir = os.path.join(pd_dir, "0_report")
    else:
        pccf_dir = args.pccf_dir
        status = compute_pccf_status(cicle, familia, pccf_dir)
        report_text = format_pccf_report(status)
        report_dir = os.path.join(pccf_dir, "0_report")

    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{familia}_{cicle}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(report_text)
    print(f"Report guardat a: {report_path}")


if __name__ == "__main__":
    main()
