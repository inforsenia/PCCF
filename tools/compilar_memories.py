#!/usr/bin/env python3

"""
Compila les memòries completades (*_OK.md) en un únic PDF amb índex
i genera un report de l'estat de les memòries.

Ús: python3 tools/compilar_memories.py [família] [centre_educatiu]

Per defecte: família = INF, centre_educatiu = SENIA
"""

import sys
import json
import os
import re
import subprocess
import shutil

from jinja2 import Environment, FileSystemLoader

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

sys.path.insert(0, SCRIPT_DIR)
from memories_utils import parse_filename, curs_display, get_grup_label, get_expected, check_placeholders, build_report_lines


def _generate_pie_chart(aprov, susp, filepath):
    fig, ax = plt.subplots(figsize=(2, 2))
    sizes = [aprov, susp]
    colors = ['#2ecc71', '#e74c3c']
    wedges, texts, autotexts = ax.pie(
        sizes, labels=['Aprovats', 'Suspensos'], colors=colors,
        startangle=90, autopct='%1.0f%%',
        textprops={'fontsize': 7}, pctdistance=0.5, labeldistance=0.7
    )
    ax.axis('equal')
    fig.savefig(filepath, dpi=100, bbox_inches='tight', transparent=True, pad_inches=0)
    plt.close(fig)


def _add_stats_row(content, pie_key):
    susp_match = re.search(r'^\|\s*Suspensos\s*\|\s*(\d+|\[###\])\s*\|$', content, re.MULTILINE)
    aprov_match = re.search(r'^\|\s*Aprovats\s*\|\s*(\d+|\[###\])\s*\|$', content, re.MULTILINE)

    if not susp_match or not aprov_match:
        return content

    susp_val = susp_match.group(1)
    aprov_val = aprov_match.group(1)

    if susp_val.isdigit() and aprov_val.isdigit():
        susp_int = int(susp_val)
        aprov_int = int(aprov_val)
        total = susp_int + aprov_int
        if total > 0:
            pct = aprov_int / total * 100
            extra = f"| Percentatge d'aprovats | {pct:.1f}% |"

            if HAS_MATPLOTLIB and pie_key:
                temp_dir = os.path.join(PROJECT_DIR, "temp")
                os.makedirs(temp_dir, exist_ok=True)
                pie_path = os.path.join(temp_dir, f"pie_{pie_key}.png")
                _generate_pie_chart(aprov_int, susp_int, pie_path)
                extra += f"\n\n![Distribució aprovats/suspensos]({pie_path})"

            insert_pos = aprov_match.end()
            content = content[:insert_pos] + "\n" + extra + content[insert_pos:]
            return content

    insert_pos = aprov_match.end()
    content = content[:insert_pos] + "\n| Percentatge d'aprovats | [###] |" + content[insert_pos:]
    return content


def main():
    all_flag = "--all" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--all"]
    familia = args[0].upper() if len(args) > 0 else "INF"
    centre_educatiu = args[1] if len(args) > 1 else "SENIA"

    # Detect available PDF engine
    pdf_engine = None
    for engine in ["xelatex", "lualatex", "pdflatex"]:
        if shutil.which(engine):
            pdf_engine = engine
            break

    if not pdf_engine:
        print("=" * 60)
        print("ERROR: No s'ha trobat cap motor LaTeX (xelatex/lualatex/pdflatex).")
        print("Cal executar aquest script dins el contenidor Docker:")
        print("  ./contenedor_lanza.sh \"make compilar-memories\"")
        print("=" * 60)
        sys.exit(1)

    config_path = os.path.join(PROJECT_DIR, f"memoria_{familia}", "config_memories.json")
    if not os.path.exists(config_path):
        print(f"Error: no es troba {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    memories_dir = os.path.join(PROJECT_DIR, "memories_md")
    if not os.path.exists(memories_dir):
        print(f"Error: no es troba el directori {memories_dir}")
        sys.exit(1)

    pdf_dir = os.path.join(PROJECT_DIR, "PDFS")
    os.makedirs(pdf_dir, exist_ok=True)

    curs_academic = config["curs"]
    centre = config["centre"]
    departament = config["departament"]

    all_files = sorted(os.listdir(memories_dir))
    parsed = []
    for f in all_files:
        info = parse_filename(f)
        if info:
            parsed.append(info)

    ok_files = [p for p in parsed if p["estat"] == "OK"]
    borrador_files = [p for p in parsed if p["estat"] == "BORRADOR"]

    expected = get_expected(config)

    # Build report
    report_lines, ok_files, borrador_files, missing, incomplete_ok = build_report_lines(
        familia, config, parsed, expected
    )

    report_text = "\n".join(report_lines)
    print(report_text)

    # Save report
    report_path = os.path.join(pdf_dir, f"report_memories_{familia}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\nReport guardat a: {report_path}")

    # --- Decide which files to compile ---
    has_pending = bool(borrador_files) or bool(missing) or bool(incomplete_ok)

    if all_flag:
        to_compile = list(ok_files) + list(borrador_files)
        if not to_compile:
            print("\nNo hi ha memòries per compilar. El PDF no es generarà.")
            return
        if has_pending:
            print("\n" + "=" * 60)
            print("ATENCIÓ: Hi ha memòries pendents (BORRADOR/FALTA/INCOMPLETES).")
            print("=" * 60)
            if borrador_files:
                print(f"  - {len(borrador_files)} fitxers en estat BORRADOR")
            if missing:
                print(f"  - {len(missing)} mòduls sense cap fitxer (FALTA)")
            if incomplete_ok:
                print(f"  - {len(incomplete_ok)} fitxers OK amb marcadors sense omplir")
            print(f"\nTotal a compilar: {len(to_compile)} memòries (OK + BORRADOR)")
            try:
                resp = input("Vols continuar amb la compilació? (s/N): ").strip().lower()
                if resp != "s" and resp != "si":
                    print("Compilació cancel·lada per l'usuari.")
                    return
            except (EOFError, KeyboardInterrupt):
                print("\nCompilació cancel·lada.")
                return
    else:
        to_compile = list(ok_files)
        if has_pending:
            print("\n" + "=" * 60)
            print("ATENCIÓ: Hi ha memòries pendents (BORRADOR/FALTA/INCOMPLETES).")
            print("=" * 60)
            if borrador_files:
                print(f"  - {len(borrador_files)} fitxers en estat BORRADOR")
            if missing:
                print(f"  - {len(missing)} mòduls sense cap fitxer (FALTA)")
            if incomplete_ok:
                print(f"  - {len(incomplete_ok)} fitxers OK amb marcadors sense omplir")
            print(f"\nEs compilaran {len(ok_files)} memòries en estat OK")
            if borrador_files:
                print(f"  + {len(borrador_files)} en estat BORRADOR (si confirmes)")
            try:
                resp = input("Vols continuar i incloure també els BORRADOR? (s/N): ").strip().lower()
                if resp == "s" or resp == "si":
                    to_compile.extend(borrador_files)
                else:
                    if not ok_files:
                        print("Compilació cancel·lada per l'usuari.")
                        return
            except (EOFError, KeyboardInterrupt):
                print("\nCompilació cancel·lada.")
                return

        if not to_compile:
            print("\nNo hi ha memòries per compilar. El PDF no es generarà.")
            return

    # Group files by cycle for the compiled document
    compiled_by_cicle = {}
    for p in to_compile:
        compiled_by_cicle.setdefault(p["cicle"], []).append(p)

    # Render portada
    env = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, "memoria")), autoescape=False)
    portada_template = env.get_template("portada_memoria_compilada.md")

    cicles_llista = list(compiled_by_cicle.keys())
    claus_cicles = ", ".join(cicles_llista)

    portada_rendered = portada_template.render(
        curs_academic=curs_academic,
        centre=centre,
        departament=departament,
        claus_cicles=claus_cicles,
    )

    # Build compiled markdown
    compiled_md_lines = []
    compiled_md_lines.append(portada_rendered)
    compiled_md_lines.append("")

    compiled_by_cicle_sorted = sorted(compiled_by_cicle.items(), key=lambda x: x[0])

    for cicle_codi, mems in compiled_by_cicle_sorted:
        # Group mems by grup within the cycle
        groups = {}
        for p in mems:
            groups.setdefault(p["grup"], []).append(p)

        cicle_nom = config["cicles"].get(cicle_codi, {}).get("nom", cicle_codi)

        for grup in sorted(groups.keys()):
            group_mems = sorted(groups[grup], key=lambda x: (x["curs"], x["modul"]))

            if grup:
                group_heading = f"{cicle_nom} ({grup})"
            else:
                group_heading = cicle_nom

            compiled_md_lines.append(f"\\newpage")
            compiled_md_lines.append("")
            compiled_md_lines.append(f"# {group_heading}")
            compiled_md_lines.append("")

            for p in group_mems:
                filepath = os.path.join(memories_dir, p["filename"])
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()

                # Remove all blockquote lines (> ...) — used for instructions
                # and any other meta-notes that should not appear in the final PDF
                content = re.sub(r'(?:^|\n)[ \t]*>.*(?:\n[ \t]*>.*)*', '', content)

                lines = content.split('\n')
                if lines and (lines[0].startswith('## ') or lines[0].startswith('# ')):
                    heading_text = lines[0].lstrip('# ')
                    lines = lines[1:]
                    compiled_md_lines.append(f"## {heading_text}")
                    compiled_md_lines.append("")

                content = '\n'.join(lines).strip()

                # Build pie key and process stats
                pie_parts = [p["cicle"]]
                if p["grup"]:
                    pie_parts.append(p["grup"])
                if p["curs"]:
                    pie_parts.append(p["curs"])
                pie_parts.append(p["modul"])
                pie_key = "_".join(pie_parts)
                content = _add_stats_row(content, pie_key)

                compiled_md_lines.append(content)
                compiled_md_lines.append("")

    compiled_md = "\n".join(compiled_md_lines)

    curs_academic_file = curs_academic.replace("-", "_")
    compiled_filename = f"compiled_memories_{familia}_{curs_academic_file}.md"
    compiled_path = os.path.join(project_dir := PROJECT_DIR, "temp", compiled_filename)
    os.makedirs(os.path.dirname(compiled_path), exist_ok=True)

    with open(compiled_path, "w", encoding="utf-8") as f:
        f.write(compiled_md)

    # Generate PDF with pandoc
    pdf_filename = f"Memories_{familia}_{centre_educatiu}_{curs_academic_file}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    template_tex = os.path.join(PROJECT_DIR, "rsrc/templates/eisvogel.latex")
    mainfont = os.path.join(PROJECT_DIR, "rsrc/sorts-mill-goudy/OFLGoudyStM.otf")

    # Use absolute paths for backgrounds since pandoc resolves YAML paths
    # relative to the working directory
    bg_dir = os.path.join(PROJECT_DIR, "rsrc/backgrounds")
    bg_page = os.path.join(bg_dir, "bg_EPM.pdf")
    bg_title = os.path.join(bg_dir, "pccf_EPM.pdf")

    if os.path.exists(bg_page) and os.path.exists(bg_title):
        # Fix paths in the compiled markdown to use absolute paths
        with open(compiled_path, encoding="utf-8") as f:
            content = f.read()
        content = content.replace(
            '"../rsrc/backgrounds/bg_EPM.pdf"',
            f'"{bg_page}"'
        ).replace(
            '"../rsrc/backgrounds/pccf_EPM.pdf"',
            f'"{bg_title}"'
        )
        with open(compiled_path, "w", encoding="utf-8") as f:
            f.write(content)

    pandoc_opts = [
        "-V", "fontsize=12pt",
        "-V", "toc=true",
        "-V", "toc-title=Índex",
        "-V", "toc-depth=2",
        "-V", "toc-own-page=true",
        "-V", "include-before=\\newpage",
    ]

    if os.path.exists(mainfont):
        pandoc_opts.extend(["-V", f"mainfont={mainfont}"])
    else:
        print(f"  (Font no trobada, usant font per defecte)")

    # Fix \pandocbounded for pandoc >= 3.2 compatibility with older templates
    header_bounded = os.path.join(PROJECT_DIR, "temp", "pandocbounded.tex")
    os.makedirs(os.path.dirname(header_bounded), exist_ok=True)
    with open(header_bounded, "w", encoding="utf-8") as f:
        f.write(r"\providecommand{\pandocbounded}[1]{#1}%" + "\n")

    cmd = [
        "pandoc",
        "--template", template_tex,
        "--include-in-header", header_bounded,
    ] + pandoc_opts + [
        f"--pdf-engine={pdf_engine}",
        "-o", pdf_path,
        compiled_path,
    ]

    print(f"\nGenerant PDF: {pdf_filename}")
    print(f"Comanda: {' '.join(str(c) for c in cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"\nPDF generat correctament: {pdf_path}")
    else:
        print(f"\nError en generar el PDF:")
        print(result.stderr)
        sys.exit(1)

    # Clean up temp pie charts after pandoc run
    temp_dir = os.path.join(PROJECT_DIR, "temp")
    for f in os.listdir(temp_dir):
        if f.startswith("pie_") and f.endswith(".png"):
            os.remove(os.path.join(temp_dir, f))


if __name__ == "__main__":
    main()
