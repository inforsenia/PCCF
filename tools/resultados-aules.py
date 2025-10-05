#!/usr/bin/env python3

import sys
import json
import os
import shutil
from box import Box
# Importamos Jinja2
import jinja2

# Cargar el JSON desde un archivo

# Origenes
if sys.argv[1] == "DAW":
    with open('./boe/rd-daw.json', 'r', encoding='utf-8') as f:
        data1 = json.load(f)

if sys.argv[1] == "DAM":
    with open('./boe/rd-dam.json', 'r', encoding='utf-8') as f:
        data1 = json.load(f)

if sys.argv[1] == "ASIR":
    with open('./boe/rd-asir.json', 'r', encoding='utf-8') as f:
        data1 = json.load(f)


if sys.argv[1] == "SMX":
    with open('./boe/rd-smx.json', 'r', encoding='utf-8') as f:
        data1 = json.load(f)

# Destinos
codigo = sys.argv[2]

# Convertir el diccionario a un objeto Box
data_box1 = Box(data1)


modulo_orig = data_box1.ModulosProfesionales[codigo]

print("outcome_name;outcome_shortname;outcome_description;scale_name;scale_items;scale_description")

for ra in modulo_orig.ResultadosAprendizaje:

    listaCriterios=modulo_orig.ResultadosAprendizaje[ra].CriteriosEvaluacion
    for ce in listaCriterios:
        print(ra+"."+ce+";"+ra+"."+ce+";\""+listaCriterios[ce]+"\";Deficiente/Regular/Excelente;Deficiente,Regular,Excelente;")





