#!/usr/bin/env python3

"""
Publica els PDFs ja compilats (PCCF + Programaciones) d'un cicle cap a la
carpeta sincronitzada amb OneDrive, dins una carpeta fixa "1_esborrany_pccf/"
(mateix patró que tools/publish_memories_output.py). A diferència de
memòries, els noms de fitxer de PCCF ja són fixos (sense timestamp), així
que no cal esborrar cap versió anterior amb un altre nom: shutil.copy2 ja
sobreescriu la publicació anterior del mateix cicle.
"""

import argparse
import os
import shutil
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def publish(dest, centre, cicle):
    pdf_dir = os.path.join(PROJECT_DIR, "PDFS")
    dest_dir = os.path.join(dest, "1_esborrany_pccf")
    os.makedirs(dest_dir, exist_ok=True)

    published = []
    for prefix in ("PCCF", "Programaciones"):
        filename = f"{prefix}_{centre}_{cicle}.pdf"
        src = os.path.join(pdf_dir, filename)
        if not os.path.exists(src):
            print(f"[publish-pccf] AVÍS: no trobat {src}, s'omet.")
            continue
        dst = os.path.join(dest_dir, filename)
        shutil.copy2(src, dst)
        published.append(dst)

    return published


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", required=True, help="Arrel de la carpeta sincronitzada amb OneDrive")
    parser.add_argument("--centre", required=True)
    parser.add_argument("--cicle", required=True)
    args = parser.parse_args()

    published = publish(args.dest, args.centre, args.cicle.upper())
    if not published:
        print("[publish-pccf] Cap fitxer publicat.")
        sys.exit(1)
    for p in published:
        print(f"[publish-pccf] Publicat: {p}")


if __name__ == "__main__":
    main()
