#!/usr/bin/env python3
"""Plantilla RRAA_CA de la coordinació de Formació en Empresa (FE).

Llig, per a cada mòdul que dualitza (`pccf_utils.dualitza`), les columnes
REQUISIT FE (H: C = compartit, E = sols empresa) i HORES DUAL (I) de la seua
fulla a `programacions/{CICLE}/libro_{CICLE}.xlsx` i:
  - omple `templates/FE/Plantilla_RRAA_CA.docx` (la de la coordinadora), un
    document per cicle i curs (camp "curs" del JSON): per mòdul, Mòdul,
    Hores empresa i una fila per RA i tipus (RRAA | CE | Compartit | Sols
    empresa);
  - escriu `pendents_FE.txt` amb els mòduls duals que encara no tenen la
    informació completa (vore `llig_fe_modul`).
Tot a `programacions/2_FE/`. El mateix lector genera la taula FE que
`prepara_pd_compilacio.py` injecta a la PD de cada mòdul, perquè PD i
document de la coordinadora sempre coincidisquen.

Ús:
    python3 tools/genera_fe.py --root PCCF_ROOT [--cicle DAM]
"""

import argparse
import copy
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pccf_utils import (CICLES_INF, CICLES_SCO, CICLE_INFO, PROJECT_DIR, dualitza, get_curs,
                        get_familia, get_hoja_label, get_moduls_del_cicle, parse_pd_filename)

PLANTILLA = os.path.join(PROJECT_DIR, "templates", "FE", "Plantilla_RRAA_CA.docx")
DIR_FE = "2_FE"
PENDENTS = "pendents_FE.txt"

FILA_INICI = 10                 # primera fila de dades (excel_estils.FILA_CAPCALERA + 2)
COL_RA, COL_CE, COL_FE, COL_HORES_DUAL = 2, 5, 8, 9
CE_RE = re.compile(r"^\s*([a-zñ]{1,2})\)")
RA_RE = re.compile(r"^\s*(RA\s*\d+)\s*\.?\s*(.*)", re.S)
TIPUS = (("C", "Compartit"), ("E", "Sols empresa"))


def _hores(valor):
    if valor is None or valor == "":
        return 0.0
    try:
        return float(str(valor).replace(",", "."))
    except ValueError:
        return None


def fmt_hores(h):
    return str(int(h)) if float(h).is_integer() else f"{h:.1f}".replace(".", ",")


def resol_fulla(sheetnames, nombre):
    """Fulla del mòdul: sigles (get_hoja_label) o, als llibres antics, el nom."""
    for cand in (get_hoja_label(nombre), nombre, nombre[:31]):
        if cand in sheetnames:
            return cand
    return None


def llig_fe_modul(ws):
    """Llig REQUISIT FE / HORES DUAL d'una fulla de mòdul que dualitza.

    Torna {"ras": [(codi, text, {"C": [ce...], "E": [ce...]}), ...],
           "hores": float, "incidencies": [str, ...]}.
    Incidència = el mòdul no té la informació FE completa.
    """
    ras, incidencies = [], []
    actual = None
    marcats = sense_hores = hores_sense_marca = 0
    hores = 0.0
    for r in range(FILA_INICI, ws.max_row + 1):
        ra = ws.cell(row=r, column=COL_RA).value
        if isinstance(ra, str) and ra.strip().startswith("RA"):
            m = RA_RE.match(ra)
            codi = m.group(1).replace(" ", "") if m else ra.split(".")[0]
            actual = (codi, (m.group(2) if m else ra).strip(), {"C": [], "E": []})
            ras.append(actual)
        ce = ws.cell(row=r, column=COL_CE).value
        if not isinstance(ce, str) or ce.strip() in ("", "TOTS") or actual is None:
            continue
        m = CE_RE.match(ce)
        lletra = m.group(1) if m else ce.strip()[:3]
        marca = ws.cell(row=r, column=COL_FE).value
        marca = "" if marca is None else str(marca).strip().upper()
        h = _hores(ws.cell(row=r, column=COL_HORES_DUAL).value)
        if h is None:
            incidencies.append(f"{actual[0]} {lletra}): HORES DUAL no numèric "
                               f"('{ws.cell(row=r, column=COL_HORES_DUAL).value}')")
            h = 0.0
        hores += h
        if marca in ("C", "E"):
            actual[2][marca].append(lletra)
            marcats += 1
            if h <= 0:
                sense_hores += 1
        elif marca:
            incidencies.append(f"{actual[0]} {lletra}): valor '{marca}' a REQUISIT FE (cal C o E)")
        elif h > 0:
            hores_sense_marca += 1
    if not marcats and hores <= 0 and not incidencies:
        incidencies.append("sense informació FE (cap criteri amb C/E ni HORES DUAL)")
    else:
        if not marcats:
            incidencies.append("cap criteri marcat amb C/E a REQUISIT FE")
        if hores <= 0:
            incidencies.append("HORES DUAL sense omplir (total 0)")
    if sense_hores:
        incidencies.append(f"{sense_hores} criteri(s) amb C/E sense HORES DUAL")
    if hores_sense_marca:
        incidencies.append(f"{hores_sense_marca} criteri(s) amb HORES DUAL sense C/E")
    return {"ras": ras, "hores": hores, "incidencies": incidencies}


def files_fe(info):
    """Una fila per RA i tipus: (RA, "a, b, c", tipus)."""
    for codi, text, per_tipus in info["ras"]:
        for tipus, _ in TIPUS:
            if per_tipus[tipus]:
                yield (codi, text, ", ".join(per_tipus[tipus]), tipus)


def taula_markdown(info):
    """Taula FE per a la subsecció de la PD (prepara_pd_compilacio.py)."""
    linies = [f"**Hores en empresa:** {fmt_hores(info['hores'])}", "",
              "| RA | CE | Compartit | Sols empresa |", "|:--|:--|:-:|:-:|"]
    for codi, _text, ces, tipus in files_fe(info):
        linies.append(f"| {codi} | {ces} | {'X' if tipus == 'C' else ''} | {'X' if tipus == 'E' else ''} |")
    return "\n".join(linies) + "\n"


def docent_de_la_pd(pd_dir, codi):
    """Nom del docent (`**Docent**:` de la PD) o None si no l'ha omplit."""
    if not os.path.isdir(pd_dir):
        return None
    for fname in os.listdir(pd_dir):
        parsed = parse_pd_filename(fname)
        if not parsed or parsed["codi"] != codi:
            continue
        with open(os.path.join(pd_dir, fname), encoding="utf-8") as f:
            m = re.search(r"(?m)^\s*\**Docent\**\s*:\s*\**\s*(.+?)\s*$", f.read())
        if m and "[" not in m.group(1):
            return m.group(1).strip("* ")
    return None


def estat_cicle(cicle, root):
    """Mòduls duals del cicle amb la seua informació FE (o incidències)."""
    familia = get_familia(cicle)
    pd_dir = os.path.join(root, "programacions", cicle)
    excel = os.path.join(pd_dir, f"libro_{cicle}.xlsx")
    wb = None
    if os.path.exists(excel):
        import openpyxl
        try:
            wb = openpyxl.load_workbook(excel, data_only=True)
        except Exception as e:
            print(f" * [FE] {cicle}: error en obrir {excel}: {e}")
    moduls = []
    for codi, modul in get_moduls_del_cicle(cicle, familia).items():
        if not dualitza(modul):
            continue
        codi = str(codi)
        fulla = resol_fulla(wb.sheetnames, modul["nombre"]) if wb else None
        if fulla:
            info = llig_fe_modul(wb[fulla])
        else:
            info = {"ras": [], "hores": 0.0,
                    "incidencies": ["Excel no trobat" if wb is None else "fulla del mòdul no trobada a l'Excel"]}
        moduls.append({"codi": codi, "nom": modul["nombre"], "curs": get_curs(modul),
                       "docent": docent_de_la_pd(pd_dir, codi), **info})
    if wb:
        wb.close()
    return moduls


def nom_cicle(cicle):
    contexto = CICLE_INFO.get(cicle, {}).get("contexto", "")
    nom = contexto.split("\n")[-1] if "\n" in contexto else re.sub(r"^el ", "", contexto)
    return f"{cicle} — {nom.strip()}" if nom else cicle


# --- docx -------------------------------------------------------------------

def _text_cela(tc, text):
    """Escriu `text` al primer paràgraf de la cel·la (w:tc), conservant-ne el format."""
    from docx.oxml.ns import qn
    ps = tc.findall(qn("w:p"))
    for p in ps[1:]:
        tc.remove(p)
    p = ps[0]
    for r in p.findall(qn("w:r")):
        p.remove(r)
    if text:
        r = p.makeelement(qn("w:r"), {})
        t = r.makeelement(qn("w:t"), {qn("xml:space"): "preserve"})
        t.text = text
        r.append(t)
        p.append(r)


def _cel_les(tr):
    from docx.oxml.ns import qn
    return tr.findall(qn("w:tc"))


def _omple_taula(tbl, modul):
    from docx.oxml.ns import qn
    trs = tbl.findall(qn("w:tr"))
    fila_modul, fila_hores, prototip = trs[0], trs[1], trs[3]  # trs[2]: capçalera RRAA | CE | ...
    _text_cela(_cel_les(fila_modul)[1], f"{modul['codi']} {modul['nom']}")
    pendent = bool(modul["incidencies"])
    _text_cela(_cel_les(fila_hores)[1], "Pendent" if pendent else fmt_hores(modul["hores"]))
    for tr in trs[3:]:
        tbl.remove(tr)
    files, anterior = [], None
    for codi, text, ces, t in ([] if pendent else files_fe(modul)):
        ra = codi if codi == anterior else f"{codi}. {text}"  # el text del RA, només a la primera fila
        files.append((ra, ces, "X" if t == "C" else "", "X" if t == "E" else ""))
        anterior = codi
    if pendent:
        files = [("Informació pendent a l'Excel: " + "; ".join(modul["incidencies"]), "", "", "")]
    for valors in files:
        tr = copy.deepcopy(prototip)
        tcs = _cel_les(tr)
        for tc, valor in zip(tcs, valors):
            _text_cela(tc, valor)
        if pendent:  # l'avís ocupa tota la fila
            for tc in tcs[1:]:
                tr.remove(tc)
            tcPr = tcs[0].find(qn("w:tcPr"))
            span = tcPr.makeelement(qn("w:gridSpan"), {qn("w:val"): str(len(tcs))})
            tcW = tcPr.find(qn("w:tcW"))
            (tcW.addnext if tcW is not None else tcPr.append)(span)
        tbl.append(tr)


def genera_docx(cicle, curs, moduls, desti):
    import docx
    from docx.oxml.ns import qn
    doc = docx.Document(PLANTILLA)
    for p in doc.paragraphs[:3]:
        if p.text.strip().startswith("CICLE:"):
            p.text = f"CICLE: {nom_cicle(cicle)}"
        elif p.text.strip().startswith("CURS:"):
            p.text = f"CURS: {f'{curs}r' if curs == 1 else f'{curs}n' if curs else '(sense indicar al JSON)'}"
    body = doc.element.body
    prototip = copy.deepcopy(doc.tables[0]._tbl)
    # Fora les taules d'exemple i els paràgrafs buits que les separen
    primera = doc.tables[0]._tbl
    for el in list(body)[list(body).index(primera):]:
        if el.tag != qn("w:sectPr"):
            body.remove(el)
    sect = body.find(qn("w:sectPr"))
    for modul in moduls:
        tbl = copy.deepcopy(prototip)
        _omple_taula(tbl, modul)
        buit = copy.deepcopy(doc.paragraphs[-1]._p) if doc.paragraphs else None
        if sect is not None:
            sect.addprevious(tbl)
            if buit is not None:
                for r in buit.findall(qn("w:r")):
                    buit.remove(r)
                sect.addprevious(buit)
        else:
            body.append(tbl)
    cp = doc.core_properties
    cp.author = cp.last_modified_by = ""
    cp.title = f"RRAA_CA {cicle}"
    doc.save(desti)


def nom_docx(cicle, curs):
    return f"RRAA_CA_{cicle}_{f'{curs}r' if curs == 1 else f'{curs}n' if curs else 'sense_curs'}.docx"


def text_pendents(estats):
    linies = ["Mòduls que dualitzen amb la informació de Formació en Empresa pendent",
              "(columnes REQUISIT FE (C/E) i HORES DUAL del libro_{CICLE}.xlsx)", ""]
    total = 0
    for cicle, moduls in estats.items():
        pendents = [m for m in moduls if m["incidencies"]]
        sense_curs = [m for m in moduls if not m["curs"]]
        if not pendents and not sense_curs:
            linies.append(f"{cicle}: complet ({len(moduls)} mòduls duals)")
            continue
        linies.append(f"{cicle}: {len(pendents)} de {len(moduls)} mòduls duals pendents")
        for m in pendents:
            total += 1
            docent = f" [{m['docent']}]" if m["docent"] else ""
            linies.append(f"  - {m['codi']} {m['nom']}{docent}")
            linies.extend(f"      · {i}" for i in m["incidencies"])
        for m in sense_curs:
            linies.append(f"  ! {m['codi']} {m['nom']}: sense \"curs\" al JSON")
    linies.insert(2, f"Total pendents: {total}")
    return "\n".join(linies) + "\n", total


def empremta(estats):
    """Hash estable del contingut (sense dates): el poller només avisa si canvia."""
    return hashlib.sha256(json.dumps(estats, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def genera(root, cicles=None):
    """Genera a {root}/programacions/2_FE els docx de `cicles` (per defecte,
    tots) i pendents_FE.txt, que sempre cobreix tots els cicles.

    Torna (estats, text_pendents, total_pendents, fitxers_docx)."""
    desti = os.path.join(root, "programacions", DIR_FE)
    os.makedirs(desti, exist_ok=True)
    estats, fitxers = {}, []
    for cicle in CICLES_INF + CICLES_SCO:
        if not os.path.isdir(os.path.join(root, "programacions", cicle)):
            continue
        moduls = estat_cicle(cicle, root)
        if moduls:
            estats[cicle] = moduls
    for cicle, moduls in estats.items():
        if cicles and cicle not in cicles:
            continue
        for curs in sorted({m["curs"] for m in moduls}, key=lambda c: c or 9):
            path = os.path.join(desti, nom_docx(cicle, curs))
            genera_docx(cicle, curs, [m for m in moduls if m["curs"] == curs], path)
            fitxers.append(path)
            print(f" * [FE] {os.path.relpath(path, root)}")
    text, total = text_pendents(estats)
    with open(os.path.join(desti, PENDENTS), "w", encoding="utf-8") as f:
        f.write(text)
    print(f" * [FE] {DIR_FE}/{PENDENTS}: {total} mòduls pendents")
    return estats, text, total, fitxers


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", default=".", help="PCCF_ROOT (conté programacions/)")
    parser.add_argument("--cicle", help="Només este cicle (per defecte, tots)")
    args = parser.parse_args()
    genera(args.root, [args.cicle.upper()] if args.cicle else None)


if __name__ == "__main__":
    main()
