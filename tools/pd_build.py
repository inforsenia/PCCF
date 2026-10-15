#!/usr/bin/env python3
"""Què cal tornar a compilar de les Programacions d'un cicle (compilació
incremental del poller, `pccf_sync_poller.compila_pd_pendents`).

`empremtes(cicle, prog_dir)` torna, per a cada mòdul amb PD (els del cicle i
les seues optatives), una empremta de tot el que fa canviar el seu PDF i el
mtime més recent d'eixes fonts:
  - el .md de la PD (del cicle o de programacions/OPTATIVES/);
  - els valors de la seua fulla de l'Excel (libro_{CICLE}.xlsx o
    libro_optatives.xlsx): editar la fulla d'un altre mòdul no el canvia;
  - la portada del cicle (PD_000_{CICLE}_*.md) i el mòdul al JSON;
  - la «versió de render» (`VERSIO_FITXERS`): la plantilla LaTeX i els
    scripts que preparen i compilen la PD. Si un desplegament els canvia,
    es recompila tot una vegada.

A més torna `contingut`, l'empremta només del que escriu el docent (el .md i
la seua fulla; per als mòduls del cicle, també la portada i el JSON), sense la
versió de render: és la que decidix si s'envia la nova versió al docent, així
que un canvi de plantilla recompila però no envia correus. Les optatives no hi
compten la portada, perquè són el mateix document en tots els seus cicles i
el docent només ha de rebre'l una vegada (`clau_enviament`).
"""

import glob
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genera_fe import resol_fulla
from pccf_utils import (OPTATIVES_DIRNAME, OPTATIVES_LIBRO, PROJECT_DIR, find_optativa_pd, get_familia,
                        get_moduls_del_cicle, get_optatives_del_cicle, parse_pd_filename)

VERSIO_FITXERS = [
    "rsrc/templates/eisvogel.latex",
    "tools/prepara_pd_compilacio.py",
    "tools/compila_pd_moduls.py",
    "tools/excel-to-pdfs.py",
    "tools/excel_estils.py",
    "tools/genera_fe.py",
]


def _sha(*parts):
    h = hashlib.sha1()
    for p in parts:
        h.update(p if isinstance(p, bytes) else str(p).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def _llig(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return b""


def _mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


def versio_render():
    return _sha(*(_llig(os.path.join(PROJECT_DIR, f)) for f in VERSIO_FITXERS))


def _fulles(excel):
    """{nom de fulla: empremta dels seus valors} (buit si no hi ha Excel)."""
    if not os.path.exists(excel):
        return {}
    import openpyxl
    try:
        wb = openpyxl.load_workbook(excel, read_only=True, data_only=True)
    except Exception:
        return {}
    try:
        return {ws.title: _sha(*(repr(r) for r in ws.iter_rows(values_only=True))) for ws in wb.worksheets}
    finally:
        wb.close()


def empremtes(cicle, prog_dir):
    """{codi: {"empremta", "contingut", "mtime", "mds", "optativa"}} dels mòduls
    amb PD del cicle (vore el docstring del mòdul)."""
    cicle = cicle.upper()
    familia = get_familia(cicle)
    pd_dir = os.path.join(prog_dir, cicle)
    opt_dir = os.path.join(prog_dir, OPTATIVES_DIRNAME)
    portades = sorted(glob.glob(os.path.join(pd_dir, f"PD_000_{cicle}_*.md")))
    portada = portades[0] if portades else ""
    comu = _sha(versio_render(), _llig(portada))

    # codi -> (fitxers .md, mòdul del JSON, Excel)
    fonts = {}
    json_moduls = get_moduls_del_cicle(cicle, familia)
    excel_cicle = os.path.join(pd_dir, f"libro_{cicle}.xlsx")
    try:
        noms = sorted(os.listdir(pd_dir))
    except OSError:
        noms = []
    for fname in noms:
        p = parse_pd_filename(fname)
        if p:
            fonts.setdefault(p["codi"], ([], json_moduls.get(p["codi"]), excel_cicle))[0].append(os.path.join(pd_dir, fname))
    excel_opt = os.path.join(opt_dir, OPTATIVES_LIBRO)
    for codi, modul in get_optatives_del_cicle(cicle, familia):
        fname = find_optativa_pd(opt_dir, codi)
        if fname:
            fonts[str(codi)] = ([os.path.join(opt_dir, fname)], modul, excel_opt)
    optatives = {str(c) for c, _ in get_optatives_del_cicle(cicle, familia)}

    fulles = {excel: _fulles(excel) for excel in {f[2] for f in fonts.values()}}
    res = {}
    for codi, (mds, modul, excel) in fonts.items():
        fulla = resol_fulla(list(fulles[excel]), modul["nombre"]) if modul else None
        docent = _sha(*(os.path.basename(m).encode() + _llig(m) for m in sorted(mds)),
                      fulles[excel].get(fulla, ""))
        modul_json = json.dumps(modul, sort_keys=True, ensure_ascii=False)
        optativa = codi in optatives
        res[codi] = {
            "empremta": _sha(comu, modul_json, docent),
            "contingut": docent if optativa else _sha(_llig(portada), modul_json, docent),
            "mtime": max([_mtime(m) for m in mds] + [_mtime(excel), _mtime(portada)]),
            "mds": sorted(mds),
            "optativa": optativa,
        }
    return res


def clau_enviament(cicle, codi, info):
    """Clau de l'estat d'enviaments: una per optativa (no per cicle)."""
    return f"{OPTATIVES_DIRNAME}/{codi}" if info["optativa"] else f"{cicle}/{codi}"
