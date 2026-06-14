#!/usr/bin/env python3

"""
Genera plantilles de memòria en Markdown a partir de la configuració
i la plantilla Jinja2.

Ús: python3 tools/generar_plantilles_memoria.py [família]

Per defecte: família = INF
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

def main():
    familia = sys.argv[1].upper() if len(sys.argv) > 1 else "INF"

    config_path = os.path.join(PROJECT_DIR, f"memoria_{familia}", "config_memories.json")
    if not os.path.exists(config_path):
        print(f"Error: no es troba {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    template_dir = os.path.join(PROJECT_DIR, "memoria")
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=False)
    template = env.get_template("plantilla_memoria.md")

    output_dir = os.path.join(PROJECT_DIR, "memories_md")
    os.makedirs(output_dir, exist_ok=True)

    curs_academic = config["curs"]
    curs_academic_file = curs_academic.replace("-", "_")
    centre = config["centre"]
    departament = config["departament"]

    total = 0

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

    print(f"\nTotal: {total} plantilles generades a memories_md/")

if __name__ == "__main__":
    main()
