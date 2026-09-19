#!/usr/bin/env python3

"""
Renderitza una Portada/Introduccio (PCCF_000_*.md, PD_000_*.md) com a
plantilla Jinja2, llegint el curs academic actual d'un fitxer extern
(mai en git, vore CURS_ACTUAL_FILE -- mateix patro que department_emails.json
a tools/mailer.py, aixi es pot canviar el curs sense tocar codi ni fer commit).

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

from memories_utils import PROJECT_DIR

CURS_ACTUAL_FILE = os.environ.get(
    "CURS_ACTUAL_FILE", os.path.join(PROJECT_DIR, "curs_actual.json")
)


def get_curs():
    if not os.path.isfile(CURS_ACTUAL_FILE):
        sys.exit(
            f"ERROR: no es troba {CURS_ACTUAL_FILE}. Crea'l amb "
            '{"curs": "2026-2027"} (fitxer extern, mai en git -- vore AGENTS.md).'
        )
    with open(CURS_ACTUAL_FILE, encoding="utf-8") as f:
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
