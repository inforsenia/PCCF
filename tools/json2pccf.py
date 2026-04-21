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


def get_template_loader_and_env(familia, template_name):
    """
    Busca el template primero en templates (genérico del centro) y si no lo encuentra,
    busca en templates_{familia}.
    Retorna el templateLoader, templateEnv y el path usado.
    """
    # Primero intentar con el genérico del centro
    searchpath_generico = "./templates/"
    if os.path.exists(searchpath_generico):
        try:
            templateLoader = jinja2.FileSystemLoader(searchpath=searchpath_generico)
            templateEnv = jinja2.Environment(loader=templateLoader)
            # Verificar si el template existe
            templateEnv.get_template(template_name)
            return templateLoader, templateEnv, searchpath_generico
        except jinja2.TemplateNotFound:
            pass  # Si no encuentra el template, continúa con el específico de familia
    
    # Si no encuentra en genérico, buscar en familia específica
    searchpath_familia = f"./templates_{familia}/"
    if os.path.exists(searchpath_familia):
        templateLoader = jinja2.FileSystemLoader(searchpath=searchpath_familia)
        templateEnv = jinja2.Environment(loader=templateLoader)
        return templateLoader, templateEnv, searchpath_familia
    
    # Si no encuentra en ningún sitio, crear con genérico para que falle con mensaje claro
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath_generico)
    templateEnv = jinja2.Environment(loader=templateLoader)
    return templateLoader, templateEnv, searchpath_generico


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
comp_file = os.path.join(dir_srcciclo, f"PCCF_033_{s_ciclo}_ImportanciaCompetencies.md")
# if os.path.exists(comp_file):
#     print(f" * PCCF: fichero de competencias ya existe: {comp_file}")
# else:
try:
    # tanto si no existe como si existe lo generamos directamente en la carpeta del ciclo
    print(f" * PCCF: fichero de competencias : {comp_file}")
    comp_file = os.path.join(dir_srcciclo, f"PCCF_033_{s_ciclo}_ImportanciaCompetencies.md")
    TEMPLATE_COMP = "PCCF_033_Cicle_ImportanciaCompetencies.md"
    templateLoader, templateEnv, used_path = get_template_loader_and_env(familia, TEMPLATE_COMP)
    print(f" * PCCF: usando plantillas desde: {used_path}")
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

# Generar fichero con la Contribución de Módulos del Ciclo a partir de plantilla Jinja
contrib_file = os.path.join(dir_srcciclo, f"PCCF_030_{s_ciclo}_ContribucioModuls.md")
try:
    # tanto si no existe como si existe lo generamos directamente en la carpeta del ciclo
    print(f" * PCCF: fichero de contribución de módulos : {contrib_file}")
    TEMPLATE_CONTRIB = "PCCF_030_Cicle_ContribucioModuls.md"
    templateLoader, templateEnv, used_path = get_template_loader_and_env(familia, TEMPLATE_CONTRIB)
    print(f" * PCCF: usando plantillas desde: {used_path}")
    template = templateEnv.get_template(TEMPLATE_CONTRIB)
    output_contrib = template.render(
        ciclo=s_ciclo,
        competencias_profesionales=data_box.CompetenciasProfesionales,
        competencias_sociales=data_box.CompetenciasSociales,
        cpps=data_box.CompetenciasProfesionalesPersonalesSociales,
        modulos=data_box.ModulosProfesionales,
    )
    with open(contrib_file, "w", encoding="utf-8") as fc:
        fc.write(output_contrib)
    print(f" * PCCF: fichero de contribución de módulos generado: {contrib_file}")
except jinja2.TemplateNotFound:
    print(f" * PCCF: plantilla {TEMPLATE_CONTRIB} no encontrada, se omite generación de contribución de módulos")
except Exception as e:
    print(f" * PCCF: error al generar fichero de contribución de módulos: {e}")




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
    pdmod = dir_modulo+"PD_"+s_ciclo+"_"+str(codigo)+"_"+modulo.nombre.replace(" ","")+".md"
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
        TEMPLATE_FILE = "PCCF_PD_Plantilla_MODULO_"+sys.argv[1]+".md"
        templateLoader, templateEnv, used_path = get_template_loader_and_env(familia, TEMPLATE_FILE)
        print(f" * PD: usando plantillas desde: {used_path}")
        template = templateEnv.get_template(TEMPLATE_FILE)
        outputText = template.render(modulo=modulo)
        fmod = "./temp/PD_"+s_ciclo+"_"+str(codigo)+"_"+modulo.nombre.replace(" ","")+".md"
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
    TEMPLATE_TITULO = "PCCF_PD_Plantilla_Portada_Modulo.md"
    templateLoader, templateEnv, used_path = get_template_loader_and_env(familia, TEMPLATE_TITULO)
    print(f" * PD Standalone: usando plantillas desde: {used_path}")
    template = templateEnv.get_template(TEMPLATE_TITULO)
    outputText = template.render(modulo=modulo)
    ftitulo = open(pdtit,"w")
    ftitulo.write(outputText)
    ftitulo.close()
    
    # Creamos el PDF desde el excel
    #print(" * [ PCCF ] : Si existe el libro rellenado en la ruta, usarlo ")
    ruta_al_libro=f"excels_{familia}/libro_"+s_ciclo+".xlsx"
    
    if os.path.exists(ruta_al_libro):
        print(" * [ PCCF ] - Excel provisto ")
    else:
        print(" * [ PCCF ] - Excel por defecto ")
        ruta_al_libro="PDFS/libro_autogenerado_"+s_ciclo+".xlsx"
        
    #print(" Obtenemos el PDF desde el Excel ")
    subprocess.run("./tools/excel-to-pdfs.py "+ruta_al_libro+" \""+modulo.nombre+"\"",shell=True,check=True)
    subprocess.run("./tools/excel-to-plan-formativo.py "+ruta_al_libro+" \""+modulo.nombre+"\" "+pdplanformativo+" ",shell=True,check=True)
    #movemos el pdf a la carpeta del modulo, imprimimos la nueva ruta:
    print(" * [ PCCF ] - PDF generado: "+dir_modulo+"PD_9999_CuadroResumen.pdf")
    shutil.copy("/tmp/cuadro-resumen.pdf",dir_modulo+"PD_9999_CuadroResumen.pdf")
    
sys.exit(0)
