#!/usr/bin/env python3
"""PDF de Programacions d'un cicle, a
`programacions/1_esborranysPerCicle/Programaciones_{CENTRE}_{CICLE}.pdf`.

Com `compila_pd_dept.py`, no torna a renderitzar cap markdown: munta la
portada del cicle (`PD_000_{CICLE}_Portada.md` de PD_DIR), l'índex i els PDF de
mòdul que `compila_pd_moduls.py` ha deixat a `3_esborranyModuls/{DEPT}/`, en
l'ordre dels fitxers (`PD_{CICLE}_{CODI}_...`: els mòduls del cicle i després
les optatives). Així, quan canvia un mòdul només es compila eixe mòdul i el
cicle es torna a muntar en uns segons.

- Cada entrada de l'índex porta les marques ✎ (BORRADOR) i ✗ (marques
  pendents o incidències de l'Excel o de FE) del mòdul, com abans.
- La marca d'aigua ESBORRANY de cada mòdul ja la porta el seu PDF; si el
  cicle no està verificat (`is_pd_verified`), la portada també la porta.
- Abans de muntar, esborra els PDF de mòdul d'este cicle que ja no tenen PD
  (mòdul esborrat o optativa que ja no és del cicle).

Ús:
    compila_pd_cicle.py CICLE --prog-dir PROG_DIR --centre CENTRE -- [opcions pandoc...]
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compila_pd_dept import MACRO_ROTACIO, includepdf, nom_modul, tex
from pccf_utils import (DEPARTAMENTS, DIR_ESBORRANY_CICLE, DIR_MODULS, PROJECT_DIR, dir_moduls,
                        get_familia)
from prepara_pd_compilacio import MARCA_BORRADOR, MARCA_INCIDENCIES
from report_pccf import compute_pd_status, estat_moduls_cicle, is_pd_verified

# La portada porta la marca si el cicle no està verificat; la resta de pàgines
# són PDF de mòdul, que ja porten la seua (si en tenen).
CAPCALERA_ESBORRANY = (
    "\\usepackage[firstpageonly]{draftwatermark}\n\\SetWatermarkText{ESBORRANY}\n"
    "\\SetWatermarkScale{1}\n\\SetWatermarkColor[gray]{0.85}\n"
)


def pdfs_cicle(prog_dir, cicle):
    """{codi: path} dels PDF de mòdul del cicle, de totes les carpetes de departament."""
    pdfs = {}
    for dept in DEPARTAMENTS:
        for path in glob.glob(os.path.join(dir_moduls(prog_dir, dept), f"PD_{cicle}_*.pdf")):
            m = re.match(rf"^PD_{cicle}_(\d+|[A-Z][A-Z0-9]*)_", os.path.basename(path))
            if m:
                pdfs[m.group(1)] = path
    return pdfs


def portada_cicle(pd_dir, cicle):
    """Portada del cicle amb els fons amb camí absolut i sense `page-background`:
    les pàgines de mòdul ja porten el seu fons."""
    portades = sorted(glob.glob(os.path.join(pd_dir, f"PD_000_{cicle}_*.md")))
    if not portades:
        return None
    with open(portades[0], encoding="utf-8") as f:
        text = f.read().replace("../rsrc/backgrounds/", os.path.join(PROJECT_DIR, "rsrc", "backgrounds") + "/")
    return "\n".join(l for l in text.split("\n") if not l.startswith("page-background"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cicle")
    parser.add_argument("--prog-dir", required=True)
    parser.add_argument("--centre", required=True)
    # Les opcions de pandoc van després de `--` i es passen tal qual.
    argv = sys.argv[1:]
    pandoc_opts = argv[argv.index("--") + 1:] if "--" in argv else []
    args = parser.parse_args(argv[:argv.index("--")] if "--" in argv else argv)
    args.prog_dir = os.path.abspath(args.prog_dir)
    cicle = args.cicle.upper()
    familia = get_familia(cicle)
    pd_dir = os.path.join(args.prog_dir, cicle)

    status = compute_pd_status(cicle, familia, pd_dir)
    # Mòduls amb PD: els fitxers que hi ha (encara que el codi no siga el del
    # JSON, p. ex. un PD_DAM_PI_... antic) i les optatives del cicle amb PD.
    estat = {m["codi"]: m for m in estat_moduls_cicle(cicle, args.prog_dir, status)}
    llocs = dict(status["placeholders"])
    moduls = {}
    for p in status["borrador"] + status["ok"]:
        moduls[p["codi"]] = estat.get(p["codi"]) or {
            "estat": p["estat"], "marques": len(llocs.get(p["filename"], [])), "excel": [], "fe": []}
    for o in status.get("optatives", []):
        if o["fitxer"]:
            moduls[o["codi"]] = estat[o["codi"]]

    pdfs = pdfs_cicle(args.prog_dir, cicle)
    for codi in sorted(set(pdfs) - set(moduls)):
        os.remove(pdfs.pop(codi))
        print(f" * [PD] {cicle} {codi}: ja no té PD, s'esborra el seu PDF de {DIR_MODULS}")
    if not pdfs:
        print(f" * [PD] {cicle}: cap PDF de mòdul a {DIR_MODULS}, no es munta el PDF del cicle")
        return

    portada = portada_cicle(pd_dir, cicle)
    if portada is None:
        print(f" * [PD] {cicle}: no hi ha portada (PD_000_{cicle}_*.md), no es munta el PDF del cicle")
        sys.exit(1)

    cos = ["", "\\newpage", ""]
    for codi, path in sorted(pdfs.items(), key=lambda p: os.path.basename(p[1])):
        m = moduls[codi]
        marca = MARCA_BORRADOR if m["estat"] == "BORRADOR" else ""
        if m["marques"] or m["excel"] or m["fe"]:
            marca += MARCA_INCIDENCIES
        cos.extend(includepdf(path, [f"1,section,1,{{{tex(nom_modul(cicle, codi))}{marca}}},modul-{codi}"]))
        cos.append("")

    tmp = os.path.join(PROJECT_DIR, "temp", f"compila_pd_cicle_{cicle}")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    md = os.path.join(tmp, f"PD_{cicle}.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(portada.rstrip("\n") + "\n" + "\n".join(cos))
    capcalera = os.path.join(tmp, "capcalera.tex")
    verificat = is_pd_verified(status)
    with open(capcalera, "w", encoding="utf-8") as f:
        f.write("\\usepackage{pifont}\n" + MACRO_ROTACIO + ("" if verificat else CAPCALERA_ESBORRANY))

    desti_dir = os.path.join(args.prog_dir, DIR_ESBORRANY_CICLE)
    os.makedirs(desti_dir, exist_ok=True)
    desti = os.path.join(desti_dir, f"Programaciones_{args.centre}_{cicle}.pdf")
    nou = os.path.join(tmp, "cicle.pdf")
    r = subprocess.run(["pandoc", *pandoc_opts, "--include-in-header", capcalera, "-o", nou, md],
                       cwd=tmp, capture_output=True, text=True)
    if r.returncode != 0:
        print(f" * [PD] ERROR muntant el PDF del cicle {cicle}:\n{r.stderr[-1500:]}")
        sys.exit(1)
    shutil.move(nou, desti)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f" * [PD] {DIR_ESBORRANY_CICLE}/{os.path.basename(desti)} ({len(pdfs)} mòduls"
          + ("" if verificat else ", ESBORRANY") + ")")


if __name__ == "__main__":
    main()
