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
from memories_utils import parse_filename, curs_display, get_grup_label, get_expected, get_expected_esobat, check_placeholders, build_report_lines, is_annex_file, get_output_parent, normalitza_fitxers, get_report_dir, te_incidencies_per_marcar


def _generate_pie_chart(aprov, susp, filepath, absents=None):
    data = [(aprov, '#2ecc71', 'Aprovats')]
    if susp > 0:
        data.append((susp, '#e74c3c', 'Suspensos'))
    if absents is not None and absents > 0:
        data.append((absents, '#f39c12', 'Absents'))

    if not data:
        return

    fig, ax = plt.subplots(figsize=(2, 2))
    sizes = [d[0] for d in data]
    colors = [d[1] for d in data]
    labels = [d[2] for d in data]
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors,
        startangle=90, autopct='%1.0f%%',
        textprops={'fontsize': 7}, pctdistance=0.5, labeldistance=0.7
    )
    ax.axis('equal')
    fig.savefig(filepath, dpi=100, bbox_inches='tight', transparent=True, pad_inches=0)
    plt.close(fig)


def _add_stats_row(content, pie_key):
    susp_match = re.search(r'^\|\s*Suspensos(?:\s*/\s*[^|]*)?\s*\|\s*(\d+|\[###\])\s*\|$', content, re.MULTILINE)
    aprov_match = re.search(r'^\|\s*Aprovats(?:\s*/\s*[^|]*)?\s*\|\s*(\d+|\[###\])\s*\|$', content, re.MULTILINE)
    absents_match = re.search(r'^\|\s*No avaluable\s*/\s*absentisme\s*\|\s*(\d+|\[###\])\s*\|$', content, re.MULTILINE)

    if not susp_match or not aprov_match:
        return content

    # Find the end of the stats table: last pipe-delimited row in the content
    # Use [ \t]* instead of \s* to avoid consuming trailing newlines
    all_rows = list(re.finditer(r'^\|.+\|[ \t]*$', content, re.MULTILINE))
    # Filter out header (first row) and separator (contains only -, :, |)
    data_rows = [r for r in all_rows if not re.match(r'^\|[-:| ]+\|[ \t]*$', r.group())]
    if data_rows:
        insert_pos = data_rows[-1].end()
    else:
        insert_pos = max(susp_match.end(), aprov_match.end())

    susp_val = susp_match.group(1)
    aprov_val = aprov_match.group(1)
    absents_val = absents_match.group(1) if absents_match else None

    if susp_val.isdigit() and aprov_val.isdigit():
        susp_int = int(susp_val)
        aprov_int = int(aprov_val)
        absents_int = int(absents_val) if absents_val and absents_val.isdigit() else None

        total = susp_int + aprov_int + (absents_int if absents_int else 0)
        if total > 0:
            pct = aprov_int / total * 100
            row = f"| Percentatge d'aprovats | {pct:.0f}% |"
        else:
            row = f"| Percentatge d'aprovats | N/D (0 avaluats) |"

        if HAS_MATPLOTLIB and pie_key:
            temp_dir = os.path.join(PROJECT_DIR, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            pie_path = os.path.join(temp_dir, f"pie_{pie_key}.png")
            if total > 0 or (absents_int is not None and absents_int > 0):
                _generate_pie_chart(aprov_int, susp_int, pie_path, absents=absents_int)
                extra = row + "\n\n![Distribució aprovats/suspensos]({})".format(pie_path)
            else:
                extra = row
        else:
            extra = row

        # Remove leading newlines from tail to avoid double blank line
        tail = content[insert_pos:].lstrip('\n')
        # Ensure blank line before next section (after pie chart)
        sep = "\n\n" if tail else ""
        content = content[:insert_pos] + "\n" + extra + sep + tail
        return content

    extra = "| Percentatge d'aprovats | [###] |"
    tail = content[insert_pos:].lstrip('\n')
    sep = "\n\n" if tail else ""
    content = content[:insert_pos] + "\n" + extra + sep + tail
    return content


def _extract_stats(content):
    """Extract (aprov, susp, absents) from module markdown content.
    Returns (aprov_int, susp_int, absents_int_or_None) or None if not found.
    """
    susp_match = re.search(r'^\|\s*Suspensos(?:\s*/\s*[^|]*)?\s*\|\s*(\d+|\[###\])\s*\|$', content, re.MULTILINE)
    aprov_match = re.search(r'^\|\s*Aprovats(?:\s*/\s*[^|]*)?\s*\|\s*(\d+|\[###\])\s*\|$', content, re.MULTILINE)
    absents_match = re.search(r'^\|\s*No avaluable\s*/\s*absentisme\s*\|\s*(\d+|\[###\])\s*\|$', content, re.MULTILINE)
    if not susp_match or not aprov_match:
        return None
    susp_val = susp_match.group(1)
    aprov_val = aprov_match.group(1)
    if not susp_val.isdigit() or not aprov_val.isdigit():
        return None
    susp_int = int(susp_val)
    aprov_int = int(aprov_val)
    absents_int = int(absents_match.group(1)) if absents_match and absents_match.group(1).isdigit() else None
    return aprov_int, susp_int, absents_int


def _generate_bar_chart(data, filepath):
    """Generate a stacked vertical bar chart with per-module stats.
    data: list of (label, aprovats, suspensos, absents_or_None)
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    num_bars = len(data)

    if num_bars == 0:
        ax.text(0.5, 0.5, 'No hi ha dades completes per al gràfic resum',
                ha='center', va='center', transform=ax.transAxes, fontsize=14)
        ax.set_title('Resum d\'estadístiques per mòdul')
        ax.axis('off')
    else:
        fig.set_size_inches(max(10, num_bars * 1.2), 5)
        labels = [d[0] for d in data]
        aprovats = [d[1] for d in data]
        suspensos = [d[2] for d in data]
        absents = [d[3] if d[3] else 0 for d in data]

        x_pos = range(num_bars)
        bar_width = 0.6

        ax.bar(x_pos, aprovats, bar_width, color='#2ecc71', label='Aprovats')
        ax.bar(x_pos, suspensos, bar_width, bottom=aprovats, color='#e74c3c', label='Suspensos')
        bottoms = [a + s for a, s in zip(aprovats, suspensos)]
        ax.bar(x_pos, absents, bar_width, bottom=bottoms, color='#f39c12', label='No avaluables / Absents')

        ax.set_xticks(x_pos)
        ax.set_ylabel('Alumnes')
        ax.set_title('Resum d\'estadístiques per mòdul')
        ax.legend(loc='upper right')

        max_label_len = 30
        truncated = [l[:max_label_len] + '...' if len(l) > max_label_len else l for l in labels]
        ax.set_xticklabels(truncated, rotation=45, ha='right', fontsize=8)
        ax.set_ylim(0, max([a + s + ab for a, s, ab in zip(aprovats, suspensos, absents)]) * 1.15)

    fig.tight_layout()
    fig.savefig(filepath, dpi=150, bbox_inches='tight', transparent=False, pad_inches=0.3)
    plt.close(fig)


def main():
    all_flag = "--all" in sys.argv
    base_dir = "memoriaFP"
    args = [a for a in sys.argv[1:] if a != "--all"]

    if "--base-dir" in args:
        idx = args.index("--base-dir")
        if idx + 1 < len(args):
            base_dir = args[idx + 1]
            args = args[:idx] + args[idx+2:]
        else:
            print("Error: --base-dir requereix un argument")
            sys.exit(1)

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

    config_path = os.path.join(PROJECT_DIR, base_dir, f"memories_{familia}.json")
    if not os.path.exists(config_path):
        print(f"Error: no es troba {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    output_parent = get_output_parent(base_dir)
    memories_dir = os.path.join(PROJECT_DIR, output_parent, familia)
    if not os.path.exists(memories_dir):
        print(f"Error: no es troba el directori {memories_dir}")
        sys.exit(1)

    pdf_dir = os.path.join(PROJECT_DIR, "PDFS")
    os.makedirs(pdf_dir, exist_ok=True)
    temp_dir = os.path.join(PROJECT_DIR, "temp")

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

    if "cicles" in config:
        expected = get_expected(config)
    else:
        expected = get_expected_esobat(config)

    # Build report
    report_lines, ok_files, borrador_files, missing, incomplete_ok = build_report_lines(
        familia, config, parsed, expected, output_parent
    )

    legend_path = os.path.join(SCRIPT_DIR, "report_legend.txt")
    legend = open(legend_path, encoding="utf-8").read() if os.path.exists(legend_path) else ""
    report_text = "\n".join(report_lines) + legend
    print(report_text)

    is_esobat = "cursos" in config
    # Save report
    report_dir = get_report_dir(base_dir, is_esobat)
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{familia}.txt")
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

    # Determine FP vs ESO/BAT
    is_esobat = "cursos" in config

    # Build set of duplicated module keys (both OK and BORRADOR exist)
    def _module_key(p):
        if is_esobat:
            return (p.get("curs_codi", ""), p.get("grup", ""), p.get("materia", ""))
        return (p["cicle"], p["curs"], p.get("grup", ""), p["modul"])

    ok_keys = {_module_key(p) for p in ok_files}
    borrador_keys = {_module_key(p) for p in borrador_files}
    duplicated_keys = ok_keys & borrador_keys

    # Render portada (family-specific if exists, else generic)
    env = Environment(loader=FileSystemLoader(os.path.join(PROJECT_DIR, base_dir)), autoescape=False)
    portada_file = f"portada_memoria_compilada_{familia}.md"
    if not os.path.exists(os.path.join(PROJECT_DIR, base_dir, portada_file)):
        portada_file = "portada_memoria_compilada.md"
    portada_template = env.get_template(portada_file)

    if is_esobat:
        # ESO/BAT: group by (etapa, curs)
        bar_data = []
        compiled_by_group = {}
        for p in to_compile:
            key = (p.get("etapa", ""), p.get("curs", ""))
            compiled_by_group.setdefault(key, []).append(p)
        claus_grup = ", ".join(f"{etapa} {curs}" for etapa, curs in compiled_by_group)

        portada_rendered = portada_template.render(
            curs_academic=curs_academic,
            centre=centre,
            departament=departament,
            claus_cicles=claus_grup,
        )

        compiled_md_lines = []
        compiled_md_lines.append(portada_rendered)
        compiled_md_lines.append("")

        first_group = True
        for (etapa, curs), mems in sorted(compiled_by_group.items(), key=lambda x: (x[0][0], x[0][1])):
            # Use curs_codi from first parsed file to look up config
            first_curs_codi = mems[0].get("curs_codi", curs + etapa)
            curs_nom = config.get("cursos", {}).get(first_curs_codi, {}).get("nom", first_curs_codi)
            group_heading = curs_nom if curs_nom else f"{curs} {etapa}"

            # Sub-group by grup
            sub_groups = {}
            for p in mems:
                sub_groups.setdefault(p.get("grup", ""), []).append(p)

            for grup in sorted(sub_groups.keys()):
                group_mems = sorted(sub_groups[grup], key=lambda x: x.get("materia", ""))
                heading = f"{group_heading} - Grup {grup}" if grup else group_heading

                if not first_group:
                    compiled_md_lines.append("\\newpage")
                    compiled_md_lines.append("")
                compiled_md_lines.append("\\refstepcounter{section}")
                compiled_md_lines.append("\\addcontentsline{toc}{section}{" + heading + "}")
                compiled_md_lines.append("")
                compiled_md_lines.append("\\vspace*{\\fill}")
                compiled_md_lines.append("")
                compiled_md_lines.append("\\begin{center}")
                compiled_md_lines.append("{\\Large\\bfseries\\color{heading-color} " + heading + "}")
                compiled_md_lines.append("\\end{center}")
                compiled_md_lines.append("")
                compiled_md_lines.append("\\vspace*{\\fill}")
                compiled_md_lines.append("")
                first_group = False

                for p in group_mems:
                    filepath = os.path.join(memories_dir, p["filename"])
                    with open(filepath, encoding="utf-8") as f:
                        content = f.read()

                    content = re.sub(r'(?:^|\n)[ \t]*>.*(?:\n[ \t]*>.*)*', '', content)

                    lines = content.split('\n')
                    heading_idx = None
                    for i, line in enumerate(lines):
                        if line.startswith('## ') or line.startswith('# '):
                            heading_idx = i
                            break
                    if heading_idx is not None:
                        heading_text = lines[heading_idx].lstrip('# ')
                        # Normalize ordinals en el heading del fitxer (2r→2n, 4r→4t, etc.)
                        heading_text = re.sub(r'\b(\d+)[rnt]\b', lambda m: curs_display(m.group(1)), heading_text)
                        lines.pop(heading_idx)
                        estat_marker = " ✏️" if p["estat"] == "BORRADOR" else ""
                        incidencia_marker = " ❌" if te_incidencies_per_marcar(
                            filepath, is_esobat, _module_key(p) in duplicated_keys
                        ) else ""
                        compiled_md_lines.append("\\newpage")
                        compiled_md_lines.append("")
                        compiled_md_lines.append(f"## {heading_text}{estat_marker}{incidencia_marker}")
                        compiled_md_lines.append("")

                    content = '\n'.join(lines).strip()
                    content = re.sub(r'^\\newpage\s*', '', content)

                    # Build pie key: etapa_curs_grup_materia
                    pie_parts = [etapa, curs]
                    if p.get("grup"):
                        pie_parts.append(p["grup"])
                    pie_parts.append(p.get("materia", ""))
                    pie_key = "_".join(pie_parts)
                    content = _add_stats_row(content, pie_key)

                    # Collect stats for the summary bar chart
                    stats = _extract_stats(content)
                    if stats:
                        label = f"{p.get('etapa', '')} {curs} {p.get('grup', '')} - {p.get('materia', '')}".strip()
                        bar_data.append((label, stats[0], stats[1], stats[2]))

                    compiled_md_lines.append(content)
                    compiled_md_lines.append("")

        # Generate summary bar chart (FP i ESO/BAT)
        if HAS_MATPLOTLIB:
            bar_filename = f"bar_resum_{familia}.png"
            bar_path = os.path.join(PROJECT_DIR, "temp", bar_filename)
            os.makedirs(os.path.dirname(bar_path), exist_ok=True)
            _generate_bar_chart(bar_data, bar_path)
            compiled_md_lines.append("")
            compiled_md_lines.append("\\newgeometry{top=10mm, bottom=10mm}")
            compiled_md_lines.append("\\begin{landscape}")
            compiled_md_lines.append("\\thispagestyle{empty}")
            compiled_md_lines.append("\\section*{Resum de resultats}")
            compiled_md_lines.append("\\addcontentsline{toc}{section}{Resum de resultats}")
            compiled_md_lines.append("\\vspace*{\\fill}")
            compiled_md_lines.append("\\centering")
            compiled_md_lines.append("\\includegraphics[width=1.0\\linewidth]{" + bar_path + "}")
            compiled_md_lines.append("\\vspace*{\\fill}")
            compiled_md_lines.append("\\end{landscape}")
            compiled_md_lines.append("\\restoregeometry")
            compiled_md_lines.append("")
    else:
        # FP: group by cycle
        compiled_by_cicle = {}
        for p in to_compile:
            compiled_by_cicle.setdefault(p["cicle"], []).append(p)

        cicles_llista = list(compiled_by_cicle.keys())
        claus_cicles = ", ".join(cicles_llista)

        portada_rendered = portada_template.render(
            curs_academic=curs_academic,
            centre=centre,
            departament=departament,
            claus_cicles=claus_cicles,
        )

        bar_data = []
        compiled_md_lines = []
        compiled_md_lines.append(portada_rendered)
        compiled_md_lines.append("")

        compiled_by_cicle_sorted = sorted(compiled_by_cicle.items(), key=lambda x: x[0])

        first_group = True
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

                if not first_group:
                    compiled_md_lines.append("\\newpage")
                    compiled_md_lines.append("")
                compiled_md_lines.append("\\refstepcounter{section}")
                compiled_md_lines.append("\\addcontentsline{toc}{section}{" + group_heading + "}")
                compiled_md_lines.append("")
                compiled_md_lines.append("\\vspace*{\\fill}")
                compiled_md_lines.append("")
                compiled_md_lines.append("\\begin{center}")
                compiled_md_lines.append("{\\Large\\bfseries\\color{heading-color} " + group_heading + "}")
                compiled_md_lines.append("\\end{center}")
                compiled_md_lines.append("")
                compiled_md_lines.append("\\vspace*{\\fill}")
                compiled_md_lines.append("")
                first_group = False

                for p in group_mems:
                    filepath = os.path.join(memories_dir, p["filename"])
                    with open(filepath, encoding="utf-8") as f:
                        content = f.read()

                    # Remove all blockquote lines (> ...) — used for instructions
                    # and any other meta-notes that should not appear in the final PDF
                    content = re.sub(r'(?:^|\n)[ \t]*>.*(?:\n[ \t]*>.*)*', '', content)

                    lines = content.split('\n')
                    heading_idx = None
                    for i, line in enumerate(lines):
                        if line.startswith('## ') or line.startswith('# '):
                            heading_idx = i
                            break
                    if heading_idx is not None:
                        heading_text = lines[heading_idx].lstrip('# ')
                        # Normalize ordinals en el heading del fitxer (2r→2n, 4r→4t, etc.)
                        heading_text = re.sub(r'\b(\d+)[rnt]\b', lambda m: curs_display(m.group(1)), heading_text)
                        lines.pop(heading_idx)
                        estat_marker = " ✏️" if p["estat"] == "BORRADOR" else ""
                        incidencia_marker = " ❌" if te_incidencies_per_marcar(
                            filepath, is_esobat, _module_key(p) in duplicated_keys
                        ) else ""
                        compiled_md_lines.append("\\newpage")
                        compiled_md_lines.append("")
                        compiled_md_lines.append(f"## {heading_text}{estat_marker}{incidencia_marker}")
                        compiled_md_lines.append("")

                    content = '\n'.join(lines).strip()
                    # Remove leading \newpage since we already add it before the heading
                    content = re.sub(r'^\\newpage\s*', '', content)

                    # Build pie key and process stats
                    pie_parts = [p["cicle"]]
                    if p["grup"]:
                        pie_parts.append(p["grup"])
                    if p["curs"]:
                        pie_parts.append(p["curs"])
                    pie_parts.append(p["modul"])
                    pie_key = "_".join(pie_parts)
                    content = _add_stats_row(content, pie_key)

                    # Collect stats for the summary bar chart
                    stats = _extract_stats(content)
                    if stats:
                        label = f"{p['cicle']} {p['curs']} {p['grup']} - {p['modul']}".strip()
                        bar_data.append((label, stats[0], stats[1], stats[2]))

                    compiled_md_lines.append(content)
                    compiled_md_lines.append("")

        # Generate summary bar chart (FP i ESO/BAT)
        if HAS_MATPLOTLIB:
            bar_filename = f"bar_resum_{familia}.png"
            bar_path = os.path.join(PROJECT_DIR, "temp", bar_filename)
            os.makedirs(os.path.dirname(bar_path), exist_ok=True)
            _generate_bar_chart(bar_data, bar_path)
            compiled_md_lines.append("")
            compiled_md_lines.append("\\newgeometry{top=10mm, bottom=10mm}")
            compiled_md_lines.append("\\begin{landscape}")
            compiled_md_lines.append("\\thispagestyle{empty}")
            compiled_md_lines.append("\\section*{Resum de resultats}")
            compiled_md_lines.append("\\addcontentsline{toc}{section}{Resum de resultats}")
            compiled_md_lines.append("\\vspace*{\\fill}")
            compiled_md_lines.append("\\centering")
            compiled_md_lines.append("\\includegraphics[width=1.0\\linewidth]{" + bar_path + "}")
            compiled_md_lines.append("\\vspace*{\\fill}")
            compiled_md_lines.append("\\end{landscape}")
            compiled_md_lines.append("\\restoregeometry")
            compiled_md_lines.append("")

    # Append annex (Activitats Extra-Escolars) at the end (only for FP)
    if not is_esobat:
        annex_files = sorted(f for f in os.listdir(memories_dir) if is_annex_file(f))
        for annex_filename in annex_files:
            annex_path = os.path.join(memories_dir, annex_filename)
            with open(annex_path, encoding="utf-8") as f:
                content = f.read()

            # Strip blockquotes
            content = re.sub(r'(?:^|\n)[ \t]*>.*(?:\n[ \t]*>.*)*', '', content)

            lines = content.split('\n')
            heading_idx = None
            for i, line in enumerate(lines):
                if line.startswith('## ') or line.startswith('# '):
                    heading_idx = i
                    break

            estat = "BORRADOR" if "_BORRADOR" in annex_filename else "OK"
            estat_marker = " ✏️" if estat == "BORRADOR" else ""

            if heading_idx is not None:
                heading_text = lines[heading_idx].lstrip('# ')
                lines.pop(heading_idx)
                compiled_md_lines.append("\\newpage")
                compiled_md_lines.append("")
                compiled_md_lines.append(f"# {heading_text}{estat_marker}")
                compiled_md_lines.append("")
            else:
                compiled_md_lines.append("\\newpage")

            content = '\n'.join(lines).strip()
            content = re.sub(r'^\\newpage\s*', '', content)
            compiled_md_lines.append(content)
            compiled_md_lines.append("")

    compiled_md = "\n".join(compiled_md_lines)

    # --- Emoji pre-processing: replace raw Unicode emoji with \emoji{name} ---
    emoji_table = "/usr/share/texlive/texmf-dist/tex/latex/emoji/emoji-table.def"
    char_to_name = {}
    if os.path.exists(emoji_table):
        with open(emoji_table, encoding="utf-8") as f:
            for line in f:
                m = re.match(r'\\__emoji_def:nnnnn \{([^}]+)\} \{([^}]+)\}', line)
                if m:
                    code_str = m.group(1).strip()
                    name = m.group(2)
                    parts = code_str.split("^^^^")
                    for p in parts:
                        if not p or len(p) not in (4, 6):
                            continue
                        cp = int(p, 16)
                        char = chr(cp)
                        if 0xFE00 <= cp <= 0xFE0F:
                            continue
                        if cp < 0x0080:
                            continue
                        char_to_name.setdefault(char, name)

    if char_to_name:
        emoji_re = re.compile('|'.join(map(re.escape, char_to_name)))
        def _replace_emoji(text):
            return emoji_re.sub(lambda m: '\\emoji{{{}}}'.format(char_to_name[m.group(0)]), text)
        compiled_md = _replace_emoji(compiled_md)

    curs_academic_file = curs_academic.replace("-", "_")
    compiled_filename = f"compiled_memories_{familia}_{curs_academic_file}.md"
    compiled_path = os.path.join(project_dir := PROJECT_DIR, "temp", compiled_filename)
    os.makedirs(os.path.dirname(compiled_path), exist_ok=True)

    with open(compiled_path, "w", encoding="utf-8") as f:
        f.write(compiled_md)

    # Generate PDF with pandoc
    prefix = base_dir.replace("memoria", "Memories_")
    pdf_filename = f"{prefix}_{familia}_{centre_educatiu}_{curs_academic_file}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    template_tex = os.path.join(PROJECT_DIR, "rsrc/templates/eisvogel.latex")

    # Use absolute paths for backgrounds since pandoc resolves YAML paths
    # relative to the working directory
    bg_dir = os.path.join(PROJECT_DIR, "rsrc/backgrounds")

    if os.path.isdir(bg_dir):
        # Fix any relative background paths in the compiled markdown
        with open(compiled_path, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r'"\.\./rsrc/backgrounds/([^"]+)"',
            lambda m: f'"{os.path.join(bg_dir, m.group(1))}"',
            content
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

    # Fix \pandocbounded for pandoc >= 3.2 compatibility with older templates
    header_bounded = os.path.join(PROJECT_DIR, "temp", "pandocbounded.tex")
    os.makedirs(os.path.dirname(header_bounded), exist_ok=True)
    with open(header_bounded, "w", encoding="utf-8") as f:
        f.write(r"\providecommand{\pandocbounded}[1]{#1}%" + "\n")
        f.write(r"\usepackage{emoji}%" + "\n")
        f.write(r"\setemojifont{NotoColorEmoji.ttf}[Path=/usr/share/fonts/truetype/noto/]%" + "\n")
        f.write(r"\setmainfont[Path=/usr/share/fonts/truetype/lato/,UprightFont=Lato-Regular.ttf,BoldFont=Lato-Bold.ttf,ItalicFont=Lato-Italic.ttf,BoldItalicFont=Lato-BoldItalic.ttf]{Lato}" + "\n")
        f.write(r"\RedeclareSectionCommand[afterskip=1.5ex plus .2ex]{paragraph}%" + "\n")
        f.write(r"\usepackage{pdflscape}%" + "\n")

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

    # Run pandoc from temp/ so LuaTeX creates luatex.XXXX dirs there, not in project root
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_dir)

    if result.returncode == 0:
        print(f"\nPDF generat correctament: {pdf_path}")
    else:
        print(f"\nError en generar el PDF:")
        print(result.stderr)
        sys.exit(1)

    # Clean up temp pie charts and bar charts after pandoc run
    for f in os.listdir(temp_dir):
        if (f.startswith("pie_") or f.startswith("bar_resum_")) and f.endswith(".png"):
            os.remove(os.path.join(temp_dir, f))


if __name__ == "__main__":
    main()
