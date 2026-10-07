#!/usr/bin/env python3
"""Un PDF per mòdul de la PD d'un cicle, a
`programacions/3_esborranyModuls/{DEPT}/PD_{CICLE}_{CODI}_{SIGLES}.pdf`.

Treballa sobre la còpia de muntatge (STAGE) que ja ha preparat
`prepara_pd_compilacio.py` per al PDF del cicle (marques, sense instruccions,
llista de docents, taula FE i Quadre Resum), amb la llista de mòduls de
`STAGE/.moduls.json`. Cada mòdul porta una portada pròpia, derivada de la del
cicle (`PD_000_*`) amb el títol del mòdul i el seu departament, i la marca
d'aigua ESBORRANY si el mòdul té ✎/✗.

Abans d'escriure, esborra els PDF d'este cicle de totes les carpetes de
departament, perquè un mòdul eliminat o que canvia de departament no hi quede.
Si un mòdul no compila, s'avisa i es continua amb la resta.

Ús (des del Makefile, amb les mateixes opcions de pandoc que el PDF del cicle):
    compila_pd_moduls.py CICLE --stage STAGE --prog-dir PROG_DIR -- [opcions pandoc...]
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pccf_utils import DEPARTAMENTS, DIR_MODULS, PROJECT_DIR, dir_moduls, nom_departament

FONS_DEPT = {"ANG": "pccf_EPM_ANGLES.pdf"}


def nom_pdf(cicle, modul):
    sigles = re.sub(r"[^\w-]", "", modul["sigles"]) or modul["codi"]
    return f"PD_{cicle}_{modul['codi']}_{sigles}.pdf"


def _yaml(valor):
    return '"' + valor.replace("\\", "\\\\").replace('"', '\\"') + '"'


def portada_modul(portada_cicle, modul):
    """Front matter de la portada del cicle amb el títol del mòdul i el
    departament com a autor; sense l'abstract (que parla del cicle)."""
    with open(portada_cicle, encoding="utf-8") as f:
        linies = f.read().split("\n")
    out, dins_abstract = [], False
    for l in linies:
        if dins_abstract:
            if l.startswith((" ", "\t")):
                continue
            dins_abstract = False
        if l.startswith("title:"):
            l = f"title: {_yaml('Programació Didàctica - ' + modul['nom'])}"
        elif l.startswith("author:"):
            l = f"author: {_yaml(nom_departament(modul['departament']))}"
        elif l.startswith("titlepage-background:"):
            # Fons del departament del mòdul (ANG, FOL...), si n'hi ha
            fons = FONS_DEPT.get(modul["departament"], f"pccf_EPM_{modul['departament']}.pdf")
            if os.path.exists(os.path.join(PROJECT_DIR, "rsrc", "backgrounds", fons)):
                l = re.sub(r"pccf_EPM_\w+\.pdf", fons, l)
        elif l.startswith("abstract:"):
            dins_abstract = True
            continue
        out.append(l)
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cicle")
    parser.add_argument("--stage", required=True)
    parser.add_argument("--prog-dir", required=True)
    # Les opcions de pandoc van després de `--` i es passen tal qual.
    argv = sys.argv[1:]
    pandoc_opts = argv[argv.index("--") + 1:] if "--" in argv else []
    args = parser.parse_args(argv[:argv.index("--")] if "--" in argv else argv)
    args.prog_dir = os.path.abspath(args.prog_dir)
    cicle = args.cicle.upper()

    with open(os.path.join(args.stage, ".moduls.json"), encoding="utf-8") as f:
        moduls = json.load(f)
    portades = sorted(glob.glob(os.path.join(args.stage, "PD_000_*.md")))

    for dept in DEPARTAMENTS:
        for vell in glob.glob(os.path.join(dir_moduls(args.prog_dir, dept), f"PD_{cicle}_*.pdf")):
            os.remove(vell)

    errors = 0
    for modul in moduls:
        desti_dir = dir_moduls(args.prog_dir, modul["departament"])
        os.makedirs(desti_dir, exist_ok=True)
        desti = os.path.join(desti_dir, nom_pdf(cicle, modul))
        fitxers = []
        if portades:
            portada = f"_portada_{modul['codi']}.md"
            with open(os.path.join(args.stage, portada), "w", encoding="utf-8") as f:
                f.write(portada_modul(portades[0], modul))
            fitxers.append(portada)
        fitxers.append(modul["fitxer"])
        cmd = ["pandoc", *pandoc_opts, "--include-in-header", "pd_header.tex"]
        if modul["draft"]:
            cmd += ["-V", "draft=true"]
        cmd += ["-o", desti, *fitxers]
        r = subprocess.run(cmd, cwd=args.stage, capture_output=True, text=True)
        rel = os.path.relpath(desti, args.prog_dir)
        if r.returncode != 0:
            errors += 1
            print(f" * [PD] ERROR compilant {rel}:\n{r.stderr[-1500:]}")
        else:
            print(f" * [PD] {rel}" + (" (ESBORRANY)" if modul["draft"] else ""))
    print(f" * [PD] {DIR_MODULS}: {len(moduls) - errors} de {len(moduls)} mòduls de {cicle} compilats")


if __name__ == "__main__":
    main()
