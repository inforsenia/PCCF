#!/usr/bin/env python3

import sys
import json
import os
import shutil
import subprocess
import argparse
from box import Box
import jinja2

import warnings
warnings.filterwarnings('ignore')

from pccf_utils import get_hoja_label, get_optatives


def get_template_loader_and_env(familia, template_name):
    searchpath_generico = "./templates/"
    if os.path.exists(searchpath_generico):
        try:
            templateLoader = jinja2.FileSystemLoader(searchpath=searchpath_generico)
            templateEnv = jinja2.Environment(loader=templateLoader)
            templateEnv.get_template(template_name)
            return templateLoader, templateEnv, searchpath_generico
        except jinja2.TemplateNotFound:
            pass

    searchpath_familia = f"./templates_{familia}/"
    if os.path.exists(searchpath_familia):
        templateLoader = jinja2.FileSystemLoader(searchpath=searchpath_familia)
        templateEnv = jinja2.Environment(loader=templateLoader)
        return templateLoader, templateEnv, searchpath_familia

    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath_generico)
    templateEnv = jinja2.Environment(loader=templateLoader)
    return templateLoader, templateEnv, searchpath_generico


def parse_args():
    parser = argparse.ArgumentParser(description="Genera PCCF markdowns from JSON + Jinja2")
    parser.add_argument("ciclo", help="Codi del cicle (ex: DAM, ASIR)")
    parser.add_argument("familia", help="Família (INF, SCO)")
    parser.add_argument("--outdir", default="./temp/",
                        help="Directori d'eixida per als fitxers generats (defecte: ./temp/)")
    parser.add_argument("--generate-only", action="store_true",
                        help="Només genera PDs (sense PCCF_030/033 ni cuadros ni portades)")
    parser.add_argument("--generate-competences", action="store_true",
                        help="Només genera PCCF_030/033 a outdir, després ix")
    return parser.parse_args()


args = parse_args()
ciclo = args.ciclo.lower()
familia = args.familia.upper()
s_ciclo = args.ciclo
outdir = args.outdir.rstrip("/") + "/"

nombre_archivo = f'./boe_{familia}/rd-{ciclo}.json'

try:
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f" * No se encontró el archivo para el ciclo: {args.ciclo}")
    print(f" * Archivo buscado: {nombre_archivo}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f" * Error al leer el archivo JSON: {nombre_archivo}")
    sys.exit(1)

# Standalone PD output directory (inside outdir to keep it self-contained)
# Only needed when not in generate-only mode
dir_ciclo = outdir + "temp_" + s_ciclo + "/"

os.makedirs(outdir, exist_ok=True)
if not args.generate_only:
    os.makedirs(dir_ciclo, exist_ok=True)

data_box = Box(data)

# Load optatives for this cycle and merge into a single dict for PCCF_030
optatives_moduls = get_optatives(ciclo, familia)
moduls_merged = {**dict(data_box.ModulosProfesionales), **optatives_moduls}

# -----------------------------------------------------------------------
# Mode només competències: genera PCCF_030/033 a outdir i ix
# -----------------------------------------------------------------------
if args.generate_competences:
    os.makedirs(outdir, exist_ok=True)
    try:
        TEMPLATE_COMP = "PCCF_033_Cicle_ImportanciaCompetencies.md"
        tloader, tenv, tpath = get_template_loader_and_env(familia, TEMPLATE_COMP)
        template = tenv.get_template(TEMPLATE_COMP)
        output = template.render(
            ciclo=s_ciclo,
            competencias_profesionales=data_box.CompetenciasProfesionales,
            competencias_sociales=data_box.CompetenciasSociales,
            cpps=data_box.CompetenciasProfesionalesPersonalesSociales,
            importancia=data.get("ImportanciaCompetencies", {}),
        )
        fpath = os.path.join(outdir, f"PCCF_033_{s_ciclo}_ImportanciaCompetencies.md")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(output)
        print(f" * PCCF: competències → {fpath}")
    except jinja2.TemplateNotFound:
        print(f" * PCCF: plantilla {TEMPLATE_COMP} no trobada, s'omet")

    try:
        TEMPLATE_CONTRIB = "PCCF_030_Cicle_ContribucioModuls.md"
        tloader, tenv, tpath = get_template_loader_and_env(familia, TEMPLATE_CONTRIB)
        template = tenv.get_template(TEMPLATE_CONTRIB)
        output = template.render(
            ciclo=s_ciclo,
            competencias_profesionales=data_box.CompetenciasProfesionales,
            competencias_sociales=data_box.CompetenciasSociales,
            cpps=data_box.CompetenciasProfesionalesPersonalesSociales,
            modulos=moduls_merged,
        )
        fpath = os.path.join(outdir, f"PCCF_030_{s_ciclo}_ContribucioModuls.md")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(output)
        print(f" * PCCF: contribució → {fpath}")
    except jinja2.TemplateNotFound:
        print(f" * PCCF: plantilla {TEMPLATE_CONTRIB} no trobada, s'omet")
    sys.exit(0)

# -----------------------------------------------------------------------
# Mode complet: genera PCCF_030/033 a outdir
# -----------------------------------------------------------------------
if not args.generate_only:
    try:
        TEMPLATE_COMP = "PCCF_033_Cicle_ImportanciaCompetencies.md"
        templateLoader, tenv, used_path = get_template_loader_and_env(familia, TEMPLATE_COMP)
        print(f" * PCCF: usando plantillas desde: {used_path}")
        template = tenv.get_template(TEMPLATE_COMP)
        output_comp = template.render(
            ciclo=s_ciclo,
            competencias_profesionales=data_box.CompetenciasProfesionales,
            competencias_sociales=data_box.CompetenciasSociales,
            cpps=data_box.CompetenciasProfesionalesPersonalesSociales,
            importancia=data.get("ImportanciaCompetencies", {}),
        )
        comp_file = os.path.join(outdir, f"PCCF_033_{s_ciclo}_ImportanciaCompetencies.md")
        with open(comp_file, "w", encoding="utf-8") as fc:
            fc.write(output_comp)
        print(f" * PCCF: fichero de competencias generado: {comp_file}")
    except jinja2.TemplateNotFound:
        print(f" * PCCF: plantilla {TEMPLATE_COMP} no encontrada, se omite generación de competencias")
    except Exception as e:
        print(f" * PCCF: error al generar fichero de competencias: {e}")

    try:
        TEMPLATE_CONTRIB = "PCCF_030_Cicle_ContribucioModuls.md"
        templateLoader, tenv, used_path = get_template_loader_and_env(familia, TEMPLATE_CONTRIB)
        print(f" * PCCF: usando plantillas desde: {used_path}")
        template = tenv.get_template(TEMPLATE_CONTRIB)
        output_contrib = template.render(
            ciclo=s_ciclo,
            competencias_profesionales=data_box.CompetenciasProfesionales,
            competencias_sociales=data_box.CompetenciasSociales,
            cpps=data_box.CompetenciasProfesionalesPersonalesSociales,
            modulos=moduls_merged,
        )
        contrib_file = os.path.join(outdir, f"PCCF_030_{s_ciclo}_ContribucioModuls.md")
        with open(contrib_file, "w", encoding="utf-8") as fc:
            fc.write(output_contrib)
        print(f" * PCCF: fichero de contribución de módulos generado: {contrib_file}")
    except jinja2.TemplateNotFound:
        print(f" * PCCF: plantilla {TEMPLATE_CONTRIB} no encontrada, se omite generación de contribución de módulos")
    except Exception as e:
        print(f" * PCCF: error al generar fichero de contribución de módulos: {e}")


def clean_path(p):
    return p.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')


def nom_fitxer_modul(modul_nom):
    return clean_path(modul_nom.replace(' ', ''))


for codigo in data_box.ModulosProfesionales:

    modulo = data_box.ModulosProfesionales[codigo]
    modulo.CPSS = data_box.CompetenciasProfesionalesPersonalesSociales
    modulo.OG = data_box.ObjetivosGenerales
    nom_net = nom_fitxer_modul(modulo.nombre)

    # Eliminar archivos antiguos (sin prefijo s_ciclo) para evitar duplicados
    for fname in os.listdir(outdir):
        if fname.startswith(f"PD_{codigo}_") and fname.endswith(".md") and not fname.startswith(f"PD_{s_ciclo}_{codigo}_"):
            os.remove(os.path.join(outdir, fname))
            print(f" * [PCCF] Eliminado archivo obsoleto (renombrar a PD_{s_ciclo}_ prefix si es una sobrescritura): {fname}")

    # Determineix ruta del PD markdown
    if args.generate_only:
        # Mode plantilles: busca _BORRADOR o _OK, genera _BORRADOR
        fmod_borrador = os.path.join(outdir, f"PD_{s_ciclo}_{codigo}_{nom_net}_BORRADOR.md")
        fmod_ok = os.path.join(outdir, f"PD_{s_ciclo}_{codigo}_{nom_net}_OK.md")

        if os.path.exists(fmod_ok) or os.path.exists(fmod_borrador):
            existing = fmod_ok if os.path.exists(fmod_ok) else fmod_borrador
            print(f" PD provisionado : {os.path.basename(existing)}")
            continue  # saltar generacio i @@@ per a fitxer existent
        else:
            fmod = fmod_borrador
            print(f" PD generado : {os.path.basename(fmod)}")
            TEMPLATE_FILE = "PCCF_PD_Plantilla_MODULO_" + args.ciclo + ".md"
            templateLoader, templateEnv, used_path = get_template_loader_and_env(familia, TEMPLATE_FILE)
            print(f" * PD: usando plantillas desde: {used_path}")
            template = templateEnv.get_template(TEMPLATE_FILE)
            outputText = template.render(modulo=modulo)
            with open(fmod, "w") as fmodulo:
                fmodulo.write(outputText)
    else:
        # Mode complet: busca PD_{s_ciclo}_{codigo}_{nom}.md
        fmod = os.path.join(outdir, f"PD_{s_ciclo}_{codigo}_{nom_net}.md")
        if os.path.exists(fmod):
            print(" PD provisionado : " + nom_net)
        else:
            print(" PD generado : Programacion Didactica para " + nom_net)
            TEMPLATE_FILE = "PCCF_PD_Plantilla_MODULO_" + args.ciclo + ".md"
            templateLoader, templateEnv, used_path = get_template_loader_and_env(familia, TEMPLATE_FILE)
            print(f" * PD: usando plantillas desde: {used_path}")
            template = templateEnv.get_template(TEMPLATE_FILE)
            outputText = template.render(modulo=modulo)
            with open(fmod, "w") as fmodulo:
                fmodulo.write(outputText)

    # Processar @@@ includes (només per fitxers nous en mode plantilles, sempre en mode complet)
    with open(fmod, "rt") as fin:
        with open(os.path.join(outdir, "out.txt"), "wt") as fout:
            for line in fin:
                if "@@@" in line:
                    pccff = "".join(line.split('@')[3]).rstrip()
                    if os.path.exists(os.path.join(outdir, pccff)):
                        newpages = 0
                        with open(os.path.join(outdir, pccff), "rt") as fincluded:
                            for linein in fincluded:
                                ignorar = False
                                if linein.startswith('\\newpage') and newpages < 10:
                                    ignorar = True
                                if linein.startswith('# '):
                                    ignorar = True
                                if linein.startswith('#'):
                                    linein = '#' + linein
                                if not ignorar:
                                    fout.write(linein)
                                newpages = newpages + 1
                    else:
                        print(" File not exists, not included : " + os.path.join(outdir, pccff))
                else:
                    fout.write(line)
    shutil.move(os.path.join(outdir, "out.txt"), fmod)

    # --- A partir d'ací, coses només per al mode complet (no generate-only) ---
    if args.generate_only:
        continue

    dir_modulo = dir_ciclo + str(codigo) + "/"
    os.makedirs(dir_modulo, exist_ok=True)

    # Copia el PD a la carpeta standalone
    pdmod = os.path.join(dir_modulo, f"PD_{s_ciclo}_{codigo}_{nom_net}.md")
    pdtit = os.path.join(dir_modulo, f"PD_0000_{codigo}_{nom_net}.md")
    pdplanformativo = os.path.join(outdir, "PCCF_222_PlanFormativo.md")
    shutil.copy(fmod, pdmod)

    # Crear PD Individual (portada)
    print("  - Generando PD Standalone para " + nom_net)
    TEMPLATE_TITULO = "PCCF_PD_Plantilla_Portada_Modulo.md"
    templateLoader, templateEnv, used_path = get_template_loader_and_env(familia, TEMPLATE_TITULO)
    print(f" * PD Standalone: usando plantillas desde: {used_path}")
    template = templateEnv.get_template(TEMPLATE_TITULO)
    outputText = template.render(modulo=modulo)
    with open(pdtit, "w") as ftitulo:
        ftitulo.write(outputText)

    # Buscar Excel
    ruta_al_libro = f"excels_{familia}/libro_" + s_ciclo + ".xlsx"
    if os.path.exists(ruta_al_libro):
        print(" * [PCCF] - Excel provisto ")
    else:
        ruta_outdir = os.path.join(outdir, f"libro_{s_ciclo}.xlsx")
        if os.path.exists(ruta_outdir):
            ruta_al_libro = ruta_outdir
            print(" * [PCCF] - Excel desde outdir ")
        else:
            ruta_al_libro = f"PDFS/libro_autogenerado_{s_ciclo}.xlsx"
            print(" * [PCCF] - Excel por defecto ")

    subprocess.run(f"./tools/excel-to-pdfs.py \"{ruta_al_libro}\" \"{modulo.nombre}\"", shell=True, check=True)
    subprocess.run(f"./tools/excel-to-plan-formativo.py \"{ruta_al_libro}\" \"{modulo.nombre}\" \"{pdplanformativo}\"", shell=True, check=True)

    pdf_cuadro = "/tmp/cuadro-resumen.pdf"
    if os.path.exists(pdf_cuadro):
        print(" * [PCCF] - PDF generado: " + os.path.join(dir_modulo, "PD_9999_CuadroResumen.pdf"))
        shutil.copy(pdf_cuadro, os.path.join(dir_modulo, "PD_9999_CuadroResumen.pdf"))
        compiled_pdf = os.path.join(outdir, f"PD_9999_{codigo}_CuadroResumen.pdf")
        shutil.copy(pdf_cuadro, compiled_pdf)
        with open(fmod, "a", encoding="utf-8") as f:
            f.write(f"\n\n\\includepdf[pages=-,noautoscale=true,fitpaper=true]{{./PD_9999_{codigo}_CuadroResumen.pdf}}\n")

# Guardar mapa código → siglas (només en mode complet)
if not args.generate_only:
    siglas_map = {}
    for codigo in data_box.ModulosProfesionales:
        nombre = data_box.ModulosProfesionales[codigo].nombre
        label = get_hoja_label(nombre)
        siglas_map[str(codigo)] = label if label != nombre else ""
    with open(os.path.join(dir_ciclo, ".module_siglas.json"), "w", encoding="utf-8") as f:
        json.dump(siglas_map, f, ensure_ascii=False)

sys.exit(0)
