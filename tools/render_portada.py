#!/usr/bin/env python3

"""
Renderitza una Portada/Introduccio (PCCF_000_*.md, PD_000_*.md) com a
plantilla Jinja2, llegint el curs academic actual de pccf/curs_actual.json.

A diferencia de la resta de PD_*.md (treball del docent, mai sobreescrit),
les Portades no contenen treball del docent -- nomes text fix + el curs --
aixi que es regeneren sempre, pero nomes s'escriu la destinacio si el
contingut renderitzat difereix del que ja hi ha (per a no disparar
recompilacions constants nomes per un touch de mtime).

Us: tools/render_portada.py <fitxer_font> <fitxer_desti>
"""

import json
import os
import sys

import jinja2

CURS_FILE = "pccf/curs_actual.json"


def get_curs():
    with open(CURS_FILE, encoding="utf-8") as f:
        return json.load(f)["curs"]


def render_portada(src, dest):
    with open(src, encoding="utf-8") as f:
        template = jinja2.Template(f.read())
    output = template.render(curs=get_curs())

    if os.path.exists(dest):
        with open(dest, encoding="utf-8") as f:
            if f.read() == output:
                print(f" * Portada sense canvis: {dest}")
                return

    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(output)
    print(f" * Portada regenerada: {dest}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Us: tools/render_portada.py <fitxer_font> <fitxer_desti>", file=sys.stderr)
        sys.exit(1)
    render_portada(sys.argv[1], sys.argv[2])
