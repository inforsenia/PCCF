#!/usr/bin/env python3

"""
Genera plantilles de memòria en Markdown a partir de la configuració
i la plantilla Jinja2. Suporta FP (cicles/moduls) i ESO/BAT (cursos/materies).

Ús:
    python3 tools/generar_plantilles_memoria.py [--base-dir DIR] [família]
    python3 tools/generar_plantilles_memoria.py --base-dir memoriaESOBAT ANGLES

Per defecte: --base-dir = memoriaFP, família = INF
"""

import sys
import json
import os

from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def get_grup_label(grup):
    if not grup:
        return "Grup únic"
    return f"Grup {grup}"

def build_grup_suffix(grup):
    if not grup:
        return ""
    if len(grup) == 1:
        return grup
    return f"_{grup}"

def curs_display(curs):
    if not curs:
        return ""
    return f"{curs}r"

def get_output_parent(base_dir):
    # "memoriaFP" → "memories_FP", "memoriaESOBAT" → "memories_ESOBAT"
    suffix = base_dir.replace("memoria", "", 1)
    return f"memories_{suffix}"

def main():
    base_dir = "memoriaFP"
    args = sys.argv[1:]

    if "--base-dir" in args:
        idx = args.index("--base-dir")
        if idx + 1 < len(args):
            base_dir = args[idx + 1]
            args = args[:idx] + args[idx+2:]
        else:
            print("Error: --base-dir requereix un argument")
            sys.exit(1)

    familia = args[0].upper() if len(args) > 0 else "INF"

    config_path = os.path.join(PROJECT_DIR, base_dir, f"memories_{familia}.json")
    if not os.path.exists(config_path):
        print(f"Error: no es troba {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    template_dir = os.path.join(PROJECT_DIR, base_dir)
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=False)
    template = env.get_template("plantilla_memoria.md")

    output_parent = get_output_parent(base_dir)
    output_dir = os.path.join(PROJECT_DIR, output_parent, familia)
    os.makedirs(output_dir, exist_ok=True)

    curs_academic = config["curs"]
    curs_academic_file = curs_academic.replace("-", "_")
    centre = config["centre"]
    departament = config["departament"]

    total = 0

    is_fp = "cicles" in config

    if is_fp:
        for cicle_codi, cicle_data in config["cicles"].items():
            cicle_nom = cicle_data["nom"]
            for curs, curs_data in cicle_data["cursos"].items():
                grups = curs_data.get("grups", [""])
                for modul in curs_data["moduls"]:
                    modul_codi = modul["codi"]
                    modul_nom = modul["nom"]
                    for grup in grups:
                        suffix = build_grup_suffix(grup)
                        prefix = f"{curs}{cicle_codi}{suffix}"

                        filename = f"{curs_academic_file}_{prefix}_{modul_codi}_BORRADOR.md"
                        filepath = os.path.join(output_dir, filename)

                        context = {
                            "curs_academic": curs_academic,
                            "curs": curs,
                            "curs_str": curs_display(curs),
                            "cicle_codi": cicle_codi,
                            "cicle_nom": cicle_nom,
                            "grup": grup,
                            "grup_label": get_grup_label(grup),
                            "modul_codi": modul_codi,
                            "modul_nom": modul_nom,
                            "centre": centre,
                            "departament": departament,
                        }

                        rendered = template.render(context)

                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(rendered)

                        print(f"  Creat: {filename}")
                        total += 1
    else:
        for curs_codi, curs_data in config["cursos"].items():
            etapa = curs_data["etapa"]
            curs_nom = curs_data["nom"]
            grups = curs_data.get("grups", [""])
            for materia in curs_data["materies"]:
                materia_codi = materia["codi"]
                materia_nom = materia["nom"]
                for grup in grups:
                    suffix = build_grup_suffix(grup)
                    prefix = f"{curs_codi}{suffix}"

                    filename = f"{curs_academic_file}_{prefix}_{materia_codi}_BORRADOR.md"
                    filepath = os.path.join(output_dir, filename)

                    context = {
                        "curs_academic": curs_academic,
                        "curs": curs_codi,
                        "curs_str": curs_nom,
                        "etapa": etapa,
                        "curs_nom": curs_nom,
                        "grup": grup,
                        "grup_label": get_grup_label(grup),
                        "materia_codi": materia_codi,
                        "materia_nom": materia_nom,
                        "centre": centre,
                        "departament": departament,
                    }

                    rendered = template.render(context)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(rendered)

                    print(f"  Creat: {filename}")
                    total += 1

    # Generar annex d'activitats extraescolars
    annex_template = env.get_template("plantilla_annex.md")
    annex_filename = f"{curs_academic_file}_AA_ACTIVITATS_EXTRAESCOLARS_BORRADOR.md"
    annex_filepath = os.path.join(output_dir, annex_filename)
    annex_rendered = annex_template.render(
        curs_academic=curs_academic,
        departament=departament,
        centre=centre,
    )
    with open(annex_filepath, "w", encoding="utf-8") as f:
        f.write(annex_rendered)
    print(f"  Creat: {annex_filename}")
    total += 1

    print(f"\nTotal: {total} plantilles generades a {output_parent}/{familia}/")

if __name__ == "__main__":
    main()
