#!/usr/bin/env python3
"""Prepara la còpia de muntatge (STAGE) de les PDs abans de compilar el PDF
de Programacions (`compila-pd-pccf-%`). Mai toca els fitxers dels docents.

Per a cada PD de mòdul copiada a STAGE:
  1. Marca el títol de nivel superior (`# ...`, i per tant l'índex) amb
     ✎ si està en BORRADOR i amb ✗ si té incidències pendents (placeholders
     `[###]`/`[...]` o Excel incoherent per a la seua fulla) -- mateix criteri
     visual que ✏️/❌ a memòries, però amb pifont perquè el PD compila amb
     xelatex (el paquet emoji requereix LuaTeX).
  2. Elimina els blocs de cita (`> ...`): a les plantilles de PD només
     s'usen per a instruccions al docent, que no han d'eixir al PDF (mateix
     regex que memòries, `memories_utils.py`).
  3. Als mòduls que dualitzen, afig a la subsecció «Formació en empresa (RA
     dualitzats)» la taula RA | CE | Compartit | Sols empresa i les hores en
     empresa, llegides de REQUISIT FE / HORES DUAL de l'Excel amb el mateix
     lector que la plantilla RRAA_CA de la coordinació (`genera_fe.py`). Si
     la informació FE és incompleta, hi posa un avís i marca ✗ el títol.
  4. Afig al final el Quadre Resum de la fulla del mòdul a l'Excel
     (`libro_{CICLE}.xlsx` de PD_DIR, el que editen els docents), exportat a
     PDF amb LibreOffice i inclòs amb \\includepdf. El títol
     `## Esquema general de ...` de la plantilla es trau del markdown i
     s'afig a l'índex amb `addtotoc` del mateix \\includepdf: si no, quedava
     sol en una pàgina en blanc abans del Quadre Resum (apaïsat).

A més, escriu STAGE/.draft si el report no està verificat
(`is_pd_verified`), perquè el Makefile active la marca d'aigua ESBORRANY.
"""

import argparse
import importlib.util
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pccf_utils import parse_pd_filename, get_optatives_del_cicle, dualitza
from genera_fe import llig_fe_modul, resol_fulla, taula_markdown
from report_pccf import compute_pd_status, is_pd_verified, find_placeholders

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MARCA_BORRADOR = r"\texorpdfstring{\ \ding{46}}{}"
MARCA_INCIDENCIES = r"\texorpdfstring{\ \textcolor{red}{\ding{55}}}{}"
# Inclou la columna J (CONTINGUTS, i OBJECTIUS/COMPETENCIES a dalt), per si
# el docent concreta els continguts a l'Excel. En els mòduls que no
# dualitzen, CONTINGUTS és la H i exportar_rango_a_pdf retalla el rang.
QUADRE_RESUM_RANG = "B1:J200"
HEADER_TEX = "\\usepackage{pifont}\n"
BLOCKQUOTE_RE = re.compile(r'(?:^|\n)[ \t]*>.*(?:\n[ \t]*>.*)*')


def load_excel_exporter():
    """excel-to-pdfs.py té guionet al nom: no es pot importar amb `import`."""
    path = os.path.join(PROJECT_DIR, "tools", "excel-to-pdfs.py")
    spec = importlib.util.spec_from_file_location("excel_to_pdfs", path)
    src = open(path, encoding="utf-8").read()
    # Només volem la funció, no el codi de nivell de mòdul (llig sys.argv).
    src = src.split("\nruta_excel = sys.argv[1]")[0]
    mod = importlib.util.module_from_spec(spec)
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod.exportar_rango_a_pdf


def marca_titol(path, marca):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines[i] = line.rstrip() + marca
            break
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


ESQUEMA_RE = re.compile(r'^## (Esquema general de .*?)\s*$', re.MULTILINE)
LATEX_ESPECIALS = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "$": r"\$"}


def extrau_titol_esquema(path):
    """Lleva la línia `## Esquema general de ...` i en torna el text (o None)."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    m = ESQUEMA_RE.search(content)
    if not m:
        return None
    with open(path, "w", encoding="utf-8") as f:
        f.write(content[:m.start()] + content[m.end():])
    return "".join(LATEX_ESPECIALS.get(c, c) for c in m.group(1))


FE_TITOL_RE = re.compile(r'^###\s+Formació en empresa.*$', re.MULTILINE)


def afig_taula_fe(path, info):
    """Insereix la taula FE després del primer paràgraf de la subsecció.
    Torna False si la PD no té la subsecció (o ja no la té el docent)."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    m = FE_TITOL_RE.search(content)
    if not m:
        return False
    # Final del primer paràgraf (text fix de la plantilla) després del títol
    resta = content[m.end():]
    inici = len(resta) - len(resta.lstrip("\n"))
    fi = resta.find("\n\n", inici)
    fi = len(resta) if fi == -1 else fi
    if info["incidencies"]:
        bloc = ("**Informació de formació en empresa pendent a l'Excel:** "
                + "; ".join(info["incidencies"]) + ".\n")
    else:
        bloc = taula_markdown(info)
    pos = m.end() + fi
    with open(path, "w", encoding="utf-8") as f:
        f.write(content[:pos] + "\n\n" + bloc + content[pos:])
    return True


def elimina_instruccions(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(BLOCKQUOTE_RE.sub("", content))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ciclo")
    parser.add_argument("familia")
    parser.add_argument("--pd-dir", required=True)
    parser.add_argument("--stage", required=True)
    args = parser.parse_args()
    cicle = args.ciclo.upper()
    familia = args.familia.upper()

    with open(os.path.join(PROJECT_DIR, f"boe_{familia}", f"rd-{cicle.lower()}.json"), encoding="utf-8") as f:
        json_moduls = json.load(f)["ModulosProfesionales"]
    moduls = {str(k): v["nombre"] for k, v in json_moduls.items()}
    duals = {str(k) for k, v in json_moduls.items() if dualitza(v)}

    status = compute_pd_status(cicle, familia, args.pd_dir)
    draft_path = os.path.join(args.stage, ".draft")
    if is_pd_verified(status):
        if os.path.exists(draft_path):
            os.remove(draft_path)
    else:
        open(draft_path, "w").close()
        print(" * [PD] Report no verificat: s'aplica la marca d'aigua ESBORRANY")

    with open(os.path.join(args.stage, "pd_header.tex"), "w", encoding="utf-8") as f:
        f.write(HEADER_TEX)

    # Cada llibre Excel: (camí, fulles, incidències). Els mòduls del cicle
    # usen libro_{CICLE}.xlsx; les optatives (copiades a STAGE per
    # copy_optatives_pd.py com a PD_{CICLE}_{CODI}_...) libro_optatives.xlsx.
    def llig_llibre(excel, issues):
        if not os.path.exists(excel):
            print(f" * [PD] Excel no trobat ({excel}): sense Quadres Resum")
            return (excel, [], issues)
        import openpyxl
        wb = openpyxl.load_workbook(excel, read_only=True)
        sheetnames = wb.sheetnames
        wb.close()
        return (excel, sheetnames, issues)

    llibre_cicle = llig_llibre(status["excel_path"], status["excel_issues"])
    llibres = {codi: llibre_cicle for codi in moduls}
    optatives = get_optatives_del_cicle(cicle, familia)
    if optatives:
        llibre_opt = llig_llibre(status["opt_excel_path"], status["opt_excel_issues"])
        for codi, modul in optatives:
            moduls[codi] = modul["nombre"]
            llibres[codi] = llibre_opt
    exportar = load_excel_exporter() if any(l[1] for l in llibres.values()) else None

    # Informació FE (REQUISIT FE / HORES DUAL) dels mòduls que dualitzen
    wb_fe = None
    if duals and llibre_cicle[1]:
        import openpyxl
        wb_fe = openpyxl.load_workbook(llibre_cicle[0], data_only=True)

    for fname in sorted(os.listdir(args.stage)):
        parsed = parse_pd_filename(fname)
        if not parsed:
            continue
        path = os.path.join(args.stage, fname)
        codi = parsed["codi"]
        nombre = moduls.get(codi)
        excel, sheetnames, excel_issues = llibres.get(codi, (None, [], []))
        fulla = resol_fulla(sheetnames, nombre) if nombre else None

        excel_ko = bool(fulla) and any(f"Fulla '{fulla}'" in e for e in excel_issues)
        if codi in duals:
            if wb_fe is not None and fulla:
                info = llig_fe_modul(wb_fe[fulla])
            else:
                info = {"ras": [], "hores": 0.0, "incidencies": ["fulla del mòdul no trobada a l'Excel"]}
            if afig_taula_fe(path, info):
                excel_ko = excel_ko or bool(info["incidencies"])
                print(f" * [PD] {codi}: taula FE afegida" + (" (pendent)" if info["incidencies"] else ""))
        marca = ""
        if parsed["estat"] == "BORRADOR":
            marca += MARCA_BORRADOR
        if find_placeholders(path) or excel_ko:
            marca += MARCA_INCIDENCIES
        if marca:
            marca_titol(path, marca)
        elimina_instruccions(path)

        if not (exportar and fulla):
            if exportar and nombre:
                print(f" * [PD] {codi}: fulla '{nombre}' no trobada a l'Excel, sense Quadre Resum")
            continue
        tmp_pdf = "/tmp/cuadro-resumen.pdf"
        if os.path.exists(tmp_pdf):
            os.remove(tmp_pdf)
        cwd = os.getcwd()
        os.chdir(PROJECT_DIR)  # exportar_rango_a_pdf usa ./temp/ relatiu
        try:
            exportar(excel, fulla, QUADRE_RESUM_RANG, tmp_pdf)
        finally:
            os.chdir(cwd)
        if not os.path.exists(tmp_pdf):
            print(f" * [PD] {codi}: no s'ha pogut exportar el Quadre Resum")
            continue
        pdf_name = f"PD_9999_{codi}_CuadroResumen.pdf"
        shutil.move(tmp_pdf, os.path.join(args.stage, pdf_name))
        titol = extrau_titol_esquema(path)
        toc = f",addtotoc={{1,subsection,2,{{{titol}}},esquema-{codi}}}" if titol else ""
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n\n\\includepdf[pages=-,landscape=true{toc}]{{./{pdf_name}}}\n")
        print(f" * [PD] {codi}: Quadre Resum afegit")


if __name__ == "__main__":
    main()
