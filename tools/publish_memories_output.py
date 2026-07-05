#!/usr/bin/env python3

"""
Copia el report i els PDFs compilats (ja generats a PDFS/) cap a la carpeta
compartida sincronitzada, mantenint només l'última versió per departament:

  0_report_memories_{FP|ESOBAT}/{FAMILIA}_{timestamp}.txt
  1_esborrany_memories_{FP|ESOBAT}/Memories_{FP|ESOBAT}_{FAMILIA}_{CENTRE}_{CURS}_{timestamp}.pdf

En publicar un departament, s'esborra qualsevol fitxer anterior d'eixe mateix
departament (timestamp diferent) ja present a la carpeta de destinació.
"""

import argparse
import glob
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memories_utils import get_report_dir, PROJECT_DIR


def latest_timestamp(tipus):
    candidats = sorted(
        glob.glob(os.path.join(PROJECT_DIR, "PDFS", f"0_*_report_memories_{tipus}"))
    )
    if not candidats:
        return None
    nom = os.path.basename(candidats[-1])
    # nom = "0_{timestamp}_report_memories_{tipus}"
    return nom[len("0_"):-len(f"_report_memories_{tipus}")]


def matches_familia(filename, familia):
    """Comprova si 'familia' apareix com a seqüència de tokens dins el nom de fitxer."""
    tokens = filename.replace(".", "_").split("_")
    familia_tokens = familia.split("_")
    n = len(familia_tokens)
    return any(tokens[i:i + n] == familia_tokens for i in range(len(tokens) - n + 1))


def publish_one(dest_dir, familia, src_path, new_name):
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, new_name)
    shutil.copy2(src_path, dest_path)
    for existing in os.listdir(dest_dir):
        if existing == new_name:
            continue
        if matches_familia(existing, familia):
            os.remove(os.path.join(dest_dir, existing))
            print(f"    esborrat anterior: {existing}")
    print(f"    publicat: {new_name}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-dir", default="memoriaESOBAT", choices=["memoriaFP", "memoriaESOBAT"])
    p.add_argument("--dest", required=True, help="Carpeta sincronitzada arrel (ex: '.../General/Memòries ESO-BAT')")
    p.add_argument("--timestamp", default=None, help="Per defecte: l'últim report generat a PDFS/")
    p.add_argument("--centre", default="IESEPM")
    p.add_argument("--familia", default=None, help="Nomes publicar este departament (per defecte: tots els presents al report)")
    args = p.parse_args()

    is_esobat = args.base_dir == "memoriaESOBAT"
    tipus = "ESOBAT" if is_esobat else "FP"

    timestamp = args.timestamp or latest_timestamp(tipus)
    if timestamp is None:
        sys.exit(f"No s'ha trobat cap carpeta de report per a {tipus} dins PDFS/")

    report_src_dir = get_report_dir(args.base_dir, is_esobat, timestamp)
    if not os.path.isdir(report_src_dir):
        sys.exit(f"No existeix {report_src_dir}")

    families = [args.familia] if args.familia else sorted(
        os.path.splitext(f)[0] for f in os.listdir(report_src_dir) if f.endswith(".txt")
    )

    report_dest_dir = os.path.join(args.dest, f"0_report_memories_{tipus}")
    esborrany_dest_dir = os.path.join(args.dest, f"1_esborrany_memories_{tipus}")
    prefix = args.base_dir.replace("memoria", "Memories_")

    for familia in families:
        print(f"- {familia}")
        report_src = os.path.join(report_src_dir, f"{familia}.txt")
        if os.path.isfile(report_src):
            publish_one(report_dest_dir, familia, report_src, f"{familia}_{timestamp}.txt")
        else:
            print(f"    AVÍS: no existeix {report_src}")

        pdf_src = os.path.join(PROJECT_DIR, "PDFS", f"{prefix}_{familia}_{args.centre}_25_26.pdf")
        if os.path.isfile(pdf_src):
            pdf_new_name = f"{prefix}_{familia}_{args.centre}_25_26_{timestamp}.pdf"
            publish_one(esborrany_dest_dir, familia, pdf_src, pdf_new_name)
        else:
            print(f"    AVÍS: no existeix PDF {pdf_src}")


if __name__ == "__main__":
    main()
