#!/usr/bin/env python3

import sys
import json
import os
import shutil
import subprocess
from box import Box
# Importamos Jinja2
import jinja2

import warnings
warnings.filterwarnings('ignore')  # Por ahora ignoro todos los warnings

# Cargar el JSON desde un archivo
if len(sys.argv) < 3:
    print(" * No se ha indicado Ciclo y Familia ")
    print(f" * Uso: {sys.argv[0]} <ciclo> <familia>")
    print(" * Ejemplo: ./json2pccf.py ASIR INF")
    sys.exit(0)

# Convertir el argumento a minúsculas
ciclo = sys.argv[1].lower()
familia = sys.argv[2].upper()
nombre_archivo = f'./boe_{familia}/rd-{ciclo}.json'

try:
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f" * No se encontró el archivo para el ciclo: {sys.argv[1]}")
    print(f" * Archivo buscado: {nombre_archivo}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f" * Error al leer el archivo JSON: {nombre_archivo}")
    sys.exit(1)

# Nos guardamos el ciclo 
s_ciclo=sys.argv[1]
dir_ciclo="./temp_"+s_ciclo+"/"

# Creamos el directorio para luego poder generar las PD de manera individual
os.makedirs(dir_ciclo,exist_ok=True)

# Convertir el diccionario a un objeto Box
data_box = Box(data)

# Generar fichero con las Competencias del Ciclo a partir de plantilla Jinja
dir_srcciclo="./src_"+familia+"_"+s_ciclo+"/"
comp_file = os.path.join(dir_srcciclo, f"PCCF_111_Competencies_{s_ciclo}.md")
if os.path.exists(comp_file):
    print(f" * PCCF: fichero de competencias ya existe: {comp_file}")
else:
    try:
        # si no existe lo generamos directamente en la carpeta PDFS
        comp_file = os.path.join("PDFS", f"PCCF_111_Competencies_{s_ciclo}.md")
        templateLoader = jinja2.FileSystemLoader(searchpath=f"./templates_{familia}/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_COMP = "PCCF_111_Competencies_Cicle.md"
        template = templateEnv.get_template(TEMPLATE_COMP)
        output_comp = template.render(
            ciclo=s_ciclo,
            competencias_profesionales=data_box.CompetenciasProfesionales,
            competencias_sociales=data_box.CompetenciasSociales,
            cpps=data_box.CompetenciasProfesionalesPersonalesSociales,
            importancia=data.get("ImportanciaCompetencias", {}),
        )
        with open(comp_file, "w", encoding="utf-8") as fc:
            fc.write(output_comp)
        print(f" * PCCF: fichero de competencias generado: {comp_file}")
    except jinja2.TemplateNotFound:
        print(f" * PCCF: plantilla {TEMPLATE_COMP} no encontrada, se omite generación de competencias")
    except Exception as e:
        print(f" * PCCF: error al generar fichero de competencias: {e}")




for codigo in data_box.ModulosProfesionales:


    modulo=data_box.ModulosProfesionales[codigo]

    modulo.CPSS=data_box.CompetenciasProfesionalesPersonalesSociales
    modulo.OG=data_box.ObjetivosGenerales

    dir_modulo = dir_ciclo+str(codigo)+"/"
    os.makedirs(dir_modulo,exist_ok=True)

    # fmod es la ruta al fichero del modulo dentro de la PD General del Ciclo
    fmod = "./temp/PD_"+str(codigo)+"_"+modulo.nombre.replace(" ","")+".md"

    # pdmod es la ruta al fichero del modulo de manera standalone
    # esto se hace para mas adelante construir los PDFS de todos los modulos
    # de manera independiente
    pdmod = dir_modulo+"PD_"+str(codigo)+"_"+modulo.nombre.replace(" ","")+".md"
    pdtit = dir_modulo+"PD_0000_"+str(codigo)+"_"+modulo.nombre.replace(" ","")+".md"
    pdplanformativo = "./temp/PCCF_222_PlanFormativo.md"

    # Esto hay que hacerlo aqui
    fmod = fmod.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
    # Creamos la ruta al fichero que sera la programacion standalone
    pdmod = pdmod.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
    

    if os.path.exists(fmod):
        print(" PD provisionado : "+modulo.nombre.replace(" ",""))

    else:
        print(" PD generado : Programacion Didactica para "+modulo.nombre.replace(" ",""))
        templateLoader = jinja2.FileSystemLoader(searchpath=f"./templates_{familia}/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "PCCF_PD_Plantilla_MODULO_"+sys.argv[1]+".md"
        template = templateEnv.get_template(TEMPLATE_FILE)
        outputText = template.render(modulo=modulo)
        fmod = "./temp/PD_"+str(codigo)+"_"+modulo.nombre.replace(" ","")+".md"
        fmodulo = open(fmod,"w")
        fmodulo.write(outputText)
        fmodulo.close()

    #print(" - Includes from PCCF para "+modulo.nombre.replace(" ",""))

    with open(fmod, "rt") as fin:
         with open("./temp/out.txt", "wt") as fout:
            for line in fin:
                if "@@@" in line:
                    pccff="".join(line.split('@')[3]).rstrip()
                    if os.path.exists("./temp/"+pccff):
                        newpages=0
                        with open("./temp/"+pccff, "rt") as fincluded:
                            for linein in fincluded:
                                ignorar=False
                                if linein.startswith('\\newpage') and newpages < 10:
                                    ignorar=True

                                if linein.startswith('# '):
                                    ignorar=True

                                if linein.startswith('#'):
                                    linein='#'+linein

                                if not ignorar :
                                    fout.write(linein)

                                newpages=newpages+1
                    else:
                        print(" File not exists, not included : ./temp/"+pccff)
                else:
                    fout.write(line)
            fout.close()
    shutil.copy("./temp/out.txt", pdmod)
    shutil.move("./temp/out.txt", fmod)

    # Creamos la PD Individual
    print("  - Generando PD Standalone para "+modulo.nombre.replace(" ",""))
    templateLoader = jinja2.FileSystemLoader(searchpath=f"./templates_{familia}/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_TITULO = "PCCF_PD_Plantilla_Portada_Modulo.md"
    template = templateEnv.get_template(TEMPLATE_TITULO)
    outputText = template.render(modulo=modulo)
    ftitulo = open(pdtit,"w")
    ftitulo.write(outputText)
    ftitulo.close()
    
    # Creamos el PDF desde el excel
    #print(" * [ PCCF ] : Si existe el libro rellenado en la ruta, usarlo ")
    ruta_al_libro=f"excels_{familia}/"+s_ciclo+"_libro.xlsx"
    
    if os.path.exists(ruta_al_libro):
        print(" * [ PCCF ] - Excel provisto ")
    else:
        print(" * [ PCCF ] - Excel por defecto ")
        ruta_al_libro="PDFS/"+s_ciclo+"_libro_autogenerado.xlsx"
        
    #print(" Obtenemos el PDF desde el Excel ")
    subprocess.run("./tools/excel-to-pdfs.py "+ruta_al_libro+" \""+modulo.nombre+"\"",shell=True,check=True)
    subprocess.run("./tools/excel-to-plan-formativo.py "+ruta_al_libro+" \""+modulo.nombre+"\" "+pdplanformativo+" ",shell=True,check=True)
    shutil.copy("/tmp/cuadro-resumen.pdf",dir_modulo+"PD_9999_CuadroResumen.pdf")
    
sys.exit(0)
