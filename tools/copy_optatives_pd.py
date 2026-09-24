#!/usr/bin/env python3
"""Copia a la còpia de muntatge (STAGE) de compila-pd-pccf-{CICLE} les PD de
les optatives que pertanyen al cicle (optatives.json, camp "grups"), des de
programacions/OPTATIVES/.

Es renomenen a PD_{CICLE}_{CODI}_..., perquè:
  - s'ordenen després dels mòduls del cicle (codis numèrics) al PDF;
  - prepara_pd_compilacio.py les reconega (PD_FILE_RE) i els pose les
    marques ✎/✗ i el Quadre Resum de libro_optatives.xlsx.

Ús: copy_optatives_pd.py CICLE FAMILIA OPTATIVES_DIR STAGE_DIR
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pccf_utils import get_optatives_del_cicle, find_optativa_pd

if len(sys.argv) != 5:
    print(__doc__)
    sys.exit(1)

cicle, familia, opt_dir, stage = sys.argv[1].upper(), sys.argv[2].upper(), sys.argv[3], sys.argv[4]

for codi, modul in get_optatives_del_cicle(cicle, familia):
    fname = find_optativa_pd(opt_dir, codi)
    if not fname:
        print(f"  * AVÍS: falta la PD de l'optativa {codi} ({modul['nombre']}) a {opt_dir}/")
        continue
    dest = f"PD_{cicle}_{fname[len('PD_'):]}"
    shutil.copy(os.path.join(opt_dir, fname), os.path.join(stage, dest))
    print(f"  • {fname} -> {dest}")
