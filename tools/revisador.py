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
if sys.argv[2] == "DAM":
    with open('./boe/rd-dam.json', 'r', encoding='utf-8') as h:
        data2 = json.load(h)

if sys.argv[2] == "DAW":
    with open('./boe/rd-daw.json', 'r', encoding='utf-8') as h:
        data2 = json.load(h)

if sys.argv[2] == "ASIR":
    with open('./boe/rd-asir.json', 'r', encoding='utf-8') as h:
        data2 = json.load(h)

# Convertir el diccionario a un objeto Box
data_box1 = Box(data1)


if len(sys.argv) != 2 and sys.argv[2] == "--contextoSocio":


    print("|Competencias Profesionales | %  |")
    print("|---------------------------|----|")
    numc=len(data_box1.CompetenciasProfesionales)
    propc=100/numc
    for cprof in data_box1.CompetenciasProfesionales:
        print(" | "+data_box1.CompetenciasProfesionalesPersonalesSociales[cprof]+"|"+str(round(propc,2))+"%  |")
    

    print("")
    print("|Competencias Sociales | %  |")
    print("|----------------------|----|")
    numc=len(data_box1.CompetenciasSociales)
    propc=100/numc
    for csoci in data_box1.CompetenciasSociales:
        print(" | "+data_box1.CompetenciasProfesionalesPersonalesSociales[csoci]+"|"+str(round(propc,2))+"%  |")
        

    for comp_orig in data_box1.CompetenciasProfesionalesPersonalesSociales:
        text_comp_orig = data_box1.CompetenciasProfesionalesPersonalesSociales[comp_orig]
        #print("Contexto : "+text_comp_orig)

    sys.exit(0)

if len(sys.argv) != 2 and sys.argv[2] == "--imagenCompetencias":
    sys.exit(0)

data_box2 = Box(data2)

if len(sys.argv) != 3 and sys.argv[3] == "--competencias":

    for comp_orig in data_box1.CompetenciasProfesionalesPersonalesSociales:
        text_comp_orig = data_box1.CompetenciasProfesionalesPersonalesSociales[comp_orig]
        for comp_dest in data_box2.CompetenciasProfesionalesPersonalesSociales:
            text_comp_dest = data_box2.CompetenciasProfesionalesPersonalesSociales[comp_dest]
            if text_comp_orig == text_comp_dest:
                print("Competencia Comun : "+text_comp_dest)
    sys.exit(0)

if len(sys.argv) != 3 and sys.argv[3] == "--UnidadesCompetenciaAcreditadas":

    for cod_orig in data_box1.ModulosProfesionales:
        modulo_orig = data_box1.ModulosProfesionales[cod_orig]
        print(" * ["+modulo_orig.nombre+"]")
        try:
            print("convalidaciones :"+str(modulo_orig.UnidadesCompetenciaAcreditadas))
        except AttributeError as e:
            print(" No tiene "+str(e))
    sys.exit(0)

if len(sys.argv) != 3 and sys.argv[3] == "--competencias-modulos":

    for cod_orig in data_box1.ModulosProfesionales:

        modulo_orig = data_box1.ModulosProfesionales[cod_orig]
        print(" * ["+modulo_orig.nombre+"]")
        try:
            print("Objetivos Generales :"+str(modulo_orig.ObjetivosGenerales))

            for obj in modulo_orig.ObjetivosGenerales:
                print(" - "+data_box1.CompetenciasProfesionalesPersonalesSociales[obj])

            print("")
            print("Competencias Titulo :"+str(modulo_orig.CompetenciasTitulo))

            for comp in modulo_orig.CompetenciasTitulo:
                print(" - "+data_box1.ObjetivosGenerales[comp])

        except AttributeError as e:
            print(" No tiene "+str(e))

        print("\n\n")

    sys.exit(0)


for cod_orig in data_box1.ModulosProfesionales:

    modulo_orig = data_box1.ModulosProfesionales[cod_orig]

    for cod_dest in data_box2.ModulosProfesionales:

        modulo_dest = data_box2.ModulosProfesionales[cod_dest]

        if modulo_dest.nombre == modulo_orig.nombre:

            print("Modulo comun["+cod_dest+"]: "+modulo_dest.nombre)

            if modulo_orig.horas == modulo_dest.horas :
                print(" - Horas OK :"+modulo_orig.horas+" -- "+modulo_dest.horas)
            else:
                print(" - Horas MAL :"+modulo_orig.horas+" -- "+modulo_dest.horas)

            print(" * CompetenciasTitulo")
            try:
                print(str(modulo_orig.CompetenciasTitulo))
                print(str(modulo_dest.CompetenciasTitulo))
            except Exception as e:
                print(str(e))

            print("\n\n")




