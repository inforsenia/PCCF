#!/usr/bin/env python3
"""PDF de Programacions per departament, a
`programacions/2_esborranysPerDept/Programaciones_{CENTRE}_{DEPT}.pdf`.

No torna a renderitzar cap markdown: ajunta, amb portada i índex, els PDF de
mòdul que `compila_pd_moduls.py` ha deixat a `3_esborranyModuls/{DEPT}/`,
ordenats per cicle (CICLES_INF + CICLES_SCO) i per nom de fitxer (el mateix
ordre que el PDF del cicle). Així sempre recull l'última versió compilada de
cada cicle i és ràpid. La marca d'aigua ESBORRANY ja la porta cada PDF de
mòdul.

Ús:
    compila_pd_dept.py --prog-dir PROG_DIR --centre CENTRE [--dept INF ...]
                       [--stage STAGE] -- [opcions pandoc...]
Amb --stage, només els departaments dels mòduls de STAGE/.moduls.json (els
que acaba de compilar un cicle); sense --dept ni --stage, tots.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compila_pd_moduls import FONS_DEPT
from pccf_utils import (CICLES_INF, CICLES_SCO, DEPARTAMENTS, DIR_ESBORRANY_DEPT, PROJECT_DIR,
                        dir_moduls, get_moduls_del_cicle, get_optatives, nom_departament)

PDF_RE = re.compile(r"^PD_([A-Z]+)_(\d+|[A-Z][A-Z0-9]*)_.*\.pdf$")
LATEX_ESPECIALS = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "$": r"\$", "{": r"\{", "}": r"\}"}


def tex(text):
    return "".join(LATEX_ESPECIALS.get(c, c) for c in text)


def get_curs():
    path = os.environ.get("CURS_ACTUAL_FILE", os.path.join(PROJECT_DIR, "curs_actual.json"))
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)["curs"]
    except (OSError, KeyError, ValueError):
        return ""


def nom_centre(dept, codi_centre):
    """Nom del centre de memoriaFP/memories_{DEPT}.json, o el codi (CENTRO_EDUCATIVO)."""
    try:
        with open(os.path.join(PROJECT_DIR, "memoriaFP", f"memories_{dept}.json"), encoding="utf-8") as f:
            return json.load(f)["centre"]
    except (OSError, KeyError, ValueError):
        return codi_centre


def nom_modul(cicle, codi):
    modul = get_moduls_del_cicle(cicle).get(codi) or get_optatives().get(codi)
    return modul["nombre"] if modul else codi


def pdfs_dept(prog_dir, dept):
    """[(cicle, codi, path)] dels PDF de mòdul del departament, en ordre."""
    ordre = {c: i for i, c in enumerate(CICLES_INF + CICLES_SCO)}
    pdfs = []
    for path in glob.glob(os.path.join(dir_moduls(prog_dir, dept), "PD_*.pdf")):
        m = PDF_RE.match(os.path.basename(path))
        if m and m.group(1) in ordre:
            pdfs.append((m.group(1), m.group(2), path))
    return sorted(pdfs, key=lambda p: (ordre[p[0]], os.path.basename(p[2])))


def markdown_dept(dept, pdfs, centre):
    from genera_fe import nom_cicle
    nom = nom_departament(dept)
    curs = get_curs()
    fons = os.path.join(PROJECT_DIR, "rsrc", "backgrounds", FONS_DEPT.get(dept, f"pccf_EPM_{dept}.pdf"))
    yaml = [
        "---",
        f'title: "Programacions Didàctiques - {nom}"',
        f'subtitle: "Curs {curs}"' if curs else None,
        f'author: "{nom_centre(dept, centre)}"',
        "lang: ca-ES",
        "titlepage: true",
        'titlepage-text-color: "3c4d64"',
        'titlepage-rule-color: "360049"',
        "titlepage-rule-height: 0",
        f'titlepage-background: "{fons}"' if os.path.exists(fons) else None,
        "---",
    ]
    cos = ["", "\\newpage", "", "\\tableofcontents", "", "\\newpage", ""]
    cicle_actual = None
    for cicle, codi, path in pdfs:
        toc = []
        if cicle != cicle_actual:
            cicle_actual = cicle
            toc.append(f"1,section,1,{{{tex(nom_cicle(cicle))}}},cicle-{cicle}")
        toc.append(f"1,subsection,2,{{{tex(nom_modul(cicle, codi))}}},modul-{cicle}-{codi}")
        cos.append(f"\\includepdf[pages=-,fitpaper=true,addtotoc={{{','.join(toc)}}}]{{{path}}}")
        cos.append("")
    return "\n".join(l for l in yaml if l is not None) + "\n" + "\n".join(cos)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prog-dir", required=True)
    parser.add_argument("--centre", required=True)
    parser.add_argument("--dept", action="append", choices=DEPARTAMENTS)
    parser.add_argument("--stage", help="Només els departaments de STAGE/.moduls.json")
    # Les opcions de pandoc van després de `--` i es passen tal qual.
    argv = sys.argv[1:]
    pandoc_opts = argv[argv.index("--") + 1:] if "--" in argv else []
    args = parser.parse_args(argv[:argv.index("--")] if "--" in argv else argv)
    args.prog_dir = os.path.abspath(args.prog_dir)

    depts = args.dept or []
    if args.stage:
        with open(os.path.join(args.stage, ".moduls.json"), encoding="utf-8") as f:
            depts += [m["departament"] for m in json.load(f)]
    depts = [d for d in DEPARTAMENTS if d in depts] if depts else DEPARTAMENTS

    desti_dir = os.path.join(args.prog_dir, DIR_ESBORRANY_DEPT)
    os.makedirs(desti_dir, exist_ok=True)
    tmp = os.path.join(PROJECT_DIR, "temp", "compila_pd_dept")
    os.makedirs(tmp, exist_ok=True)
    for dept in depts:
        pdfs = pdfs_dept(args.prog_dir, dept)
        if not pdfs:
            print(f" * [PD] {dept}: cap PDF de mòdul a {dir_moduls(args.prog_dir, dept)}, no es genera")
            continue
        md = os.path.join(tmp, f"PD_{dept}.md")
        with open(md, "w", encoding="utf-8") as f:
            f.write(markdown_dept(dept, pdfs, args.centre))
        desti = os.path.join(desti_dir, f"Programaciones_{args.centre}_{dept}.pdf")
        r = subprocess.run(["pandoc", *pandoc_opts, "-o", desti, md], cwd=tmp, capture_output=True, text=True)
        if r.returncode != 0:
            print(f" * [PD] ERROR compilant el PDF del departament {dept}:\n{r.stderr[-1500:]}")
        else:
            print(f" * [PD] {DIR_ESBORRANY_DEPT}/{os.path.basename(desti)} ({len(pdfs)} mòduls)")


if __name__ == "__main__":
    main()
