#!/usr/bin/env python3

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pccf_utils import (parse_pd_filename, check_excel_coherence, get_familia,
                        get_optatives_del_cicle, find_optativa_pd, OPTATIVES_DIRNAME, OPTATIVES_LIBRO,
                        get_hoja_label, get_moduls_del_cicle, hores_per_fulla,
                        CICLES_INF, CICLES_SCO, DEPARTAMENTS, get_departament,
                        dir_report_cicle, dir_report_dept)

PLACEHOLDER_RE = re.compile(r'\[#+#\]|\[\.\.\.\]')


def find_placeholders(filepath):
    places = []
    with open(filepath, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            stripped = line.strip()
            if not PLACEHOLDER_RE.search(stripped):
                continue
            # Els blocs `>` de la PD són instruccions per al docent (amb
            # exemples) i s'eliminen del PDF: mai són marques pendents.
            if stripped.startswith('>'):
                continue
            places.append((i, stripped[:120]))
    return places


def compute_pd_status(cicle, familia, pd_dir):
    status = {
        "cicle": cicle,
        "familia": familia,
        "pd_dir": pd_dir,
        "dir_found": os.path.isdir(pd_dir),
        "borrador": [],
        "ok": [],
        "placeholders": [],
        "total_places": 0,
        "excel_path": os.path.join(pd_dir, f"libro_{cicle}.xlsx"),
        "excel_issues": [],
    }
    if not status["dir_found"]:
        return status

    pd_files = sorted([f for f in os.listdir(pd_dir) if f.endswith('.md') and f.startswith('PD_')])
    for f in pd_files:
        parsed = parse_pd_filename(f)
        if parsed:
            if parsed['estat'] == 'BORRADOR':
                status["borrador"].append(parsed)
            elif parsed['estat'] == 'OK':
                status["ok"].append(parsed)

    all_md = sorted([f for f in os.listdir(pd_dir) if f.endswith('.md') and not f.startswith('out.')])
    for f in all_md:
        fp = os.path.join(pd_dir, f)
        places = find_placeholders(fp)
        if places:
            status["placeholders"].append((f, places))
            status["total_places"] += len(places)

    status["excel_issues"] = check_excel_coherence(
        status["excel_path"], hores_per_fulla(get_moduls_del_cicle(cicle, familia).values()))
    add_optatives_status(status)
    return status


def add_optatives_status(status):
    """Afig a `status` les optatives del cicle (optatives.json), que viuen
    compartides a programacions/OPTATIVES/ però formen part de les
    Programacions del cicle: si en falta la PD, està en BORRADOR, té marques
    pendents o la seua fulla de libro_optatives.xlsx no és coherent, el
    cicle no es considera verificat (marca ESBORRANY)."""
    opt_dir = os.path.join(os.path.dirname(os.path.abspath(status["pd_dir"])), OPTATIVES_DIRNAME)
    status["opt_dir"] = opt_dir
    status["opt_excel_path"] = os.path.join(opt_dir, OPTATIVES_LIBRO)
    status["optatives"] = []
    status["opt_excel_issues"] = []

    opts = get_optatives_del_cicle(status["cicle"], status["familia"])
    if not opts:
        return

    for codi, modul in opts:
        fname = find_optativa_pd(opt_dir, codi)
        estat = None if not fname else ("OK" if fname.endswith("_OK.md") else "BORRADOR")
        status["optatives"].append({"codi": codi, "nom": modul["nombre"], "fitxer": fname, "estat": estat})
        if fname:
            places = find_placeholders(os.path.join(opt_dir, fname))
            if places:
                status["placeholders"].append((f"{OPTATIVES_DIRNAME}/{fname}", places))
                status["total_places"] += len(places)

    # Només les fulles de les optatives d'este cicle: la fulla porta les
    # sigles (get_hoja_label); els llibres antics, el nom (tallat a 31)
    noms = set()
    for _, m in opts:
        noms |= {m["nombre"], m["nombre"][:31], get_hoja_label(m["nombre"])}
    for issue in check_excel_coherence(status["opt_excel_path"], hores_per_fulla(m for _, m in opts)):
        if "Fulla '" not in issue or any(f"Fulla '{n}'" in issue for n in noms):
            status["opt_excel_issues"].append(issue)


def compute_pccf_status(cicle, familia, pccf_dir):
    status = {
        "cicle": cicle,
        "familia": familia,
        "pccf_dir": pccf_dir,
        "dir_found": os.path.isdir(pccf_dir),
        "missing_src_dirs": [],
        "pccf_count": 0,
        "placeholders": [],
        "total_places": 0,
    }
    if not status["dir_found"]:
        return status

    for d in [f"src", f"src_{familia}", f"src_{familia}_{cicle}"]:
        dd = os.path.join(pccf_dir, d)
        if not os.path.isdir(dd):
            status["missing_src_dirs"].append(d)

    for root, _dirs, files in os.walk(pccf_dir):
        for f in sorted(files):
            if f.startswith("PCCF_") and f.endswith(".md"):
                status["pccf_count"] += 1
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, pccf_dir)
                places = find_placeholders(fp)
                if places:
                    status["placeholders"].append((rel, places))
                    status["total_places"] += len(places)

    return status


def is_pd_verified(status):
    if not status["dir_found"]:
        return False
    if status["borrador"]:
        return False
    if status["total_places"] > 0:
        return False
    if status["excel_issues"]:
        return False
    if any(o["estat"] != "OK" for o in status.get("optatives", [])):
        return False
    if status.get("opt_excel_issues"):
        return False
    return True


def is_pccf_verified(status):
    if not status["dir_found"]:
        return False
    if status["total_places"] > 0:
        return False
    return True


def format_pd_report(status):
    lines = []
    lines.append(f"=== Report Programacions Didàctiques: {status['cicle']} (Família {status['familia']}) ===")
    lines.append(f"Directori: {status['pd_dir']}/\n")

    if not status["dir_found"]:
        lines.append(f"ERROR: Directori no trobat: {status['pd_dir']}")
        return "\n".join(lines)

    lines.append(f"PDs en BORRADOR: {len(status['borrador'])}")
    for p in status["borrador"]:
        lines.append(f"  - {p['nom']} ({p['codi']})")
    lines.append(f"PDs en OK: {len(status['ok'])}")
    for p in status["ok"]:
        lines.append(f"  - {p['nom']} ({p['codi']})")
    lines.append("")

    for f, places in status["placeholders"]:
        lines.append(f"  {f} ({len(places)} marques pendents):")
        for ln, ct in places[:10]:
            lines.append(f"    L{ln}: {ct}")
        if len(places) > 10:
            lines.append(f"    ... i {len(places) - 10} marques més")
        lines.append("")

    if status["total_places"] == 0:
        lines.append("  [###]: Cap marca pendent.\n")
    else:
        lines.append(f"  [###]: {status['total_places']} marques en {len(status['placeholders'])} fitxers.\n")

    lines.append(f"Excel: {status['excel_path']}")
    if status["excel_issues"]:
        for e in status["excel_issues"]:
            lines.append(f"  {e}")
    else:
        lines.append("  Correcte (RA suma 100% o Excel no trobat/sense dades).")
    lines.append("")

    if status.get("optatives"):
        lines.append(f"Optatives del cicle ({status['opt_dir']}/): {len(status['optatives'])}")
        for o in status["optatives"]:
            if o["estat"] is None:
                estat = "FALTA la PD (cal generar-la: genera-totes-plantilles)"
            else:
                estat = o["estat"]
            lines.append(f"  - {o['nom']} ({o['codi']}): {estat}")
        lines.append(f"Excel optatives: {status['opt_excel_path']}")
        if status["opt_excel_issues"]:
            for e in status["opt_excel_issues"]:
                lines.append(f"  {e}")
        else:
            lines.append("  Correcte (RA suma 100% o sense dades).")
        lines.append("")

    lines.append(f"Verificat (sense marca d'esborrany): {'SI' if is_pd_verified(status) else 'NO'}")

    return "\n".join(lines)


def format_pccf_report(status):
    lines = []
    lines.append(f"=== Report Framework PCCF: {status['cicle']} (Família {status['familia']}) ===")
    lines.append(f"Directori: {status['pccf_dir']}/\n")

    if not status["dir_found"]:
        lines.append(f"ERROR: Directori no trobat: {status['pccf_dir']}")
        return "\n".join(lines)

    lines.append(f"Directoris src esperats:")
    for d in [f"src", f"src_{status['familia']}", f"src_{status['familia']}_{status['cicle']}"]:
        dd = os.path.join(status['pccf_dir'], d)
        present = "✓" if os.path.isdir(dd) else "✗"
        lines.append(f"  {present} {d}/")

    lines.append(f"\nFitxers PCCF_*.md trobats: {status['pccf_count']}")

    for f, places in status["placeholders"]:
        lines.append(f"  {f} ({len(places)} marques pendents):")
        for ln, ct in places[:10]:
            lines.append(f"    L{ln}: {ct}")
        if len(places) > 10:
            lines.append(f"    ... i {len(places) - 10} marques més")
        lines.append("")

    if status["total_places"] == 0:
        lines.append("  [###]: Cap marca pendent en fitxers PCCF.\n")
    else:
        lines.append(f"  [###]: {status['total_places']} marques en {len(status['placeholders'])} fitxers.\n")

    lines.append(f"Verificat (sense marca d'esborrany): {'SI' if is_pccf_verified(status) else 'NO'}")

    return "\n".join(lines)


def report_pd(cicle, familia, pd_dir):
    return format_pd_report(compute_pd_status(cicle, familia, pd_dir))


def report_pccf(cicle, familia, pccf_dir):
    return format_pccf_report(compute_pccf_status(cicle, familia, pccf_dir))


# --- Report per departament ------------------------------------------------

def _issues_fulla(issues, nombre):
    """Incidències de l'Excel que són de la fulla del mòdul `nombre` (la
    fulla porta les sigles; els llibres antics, el nom tallat a 31)."""
    noms = {nombre, nombre[:31], get_hoja_label(nombre)}
    return [i.strip() for i in issues if any(f"Fulla '{n}'" in i for n in noms)]


def estat_moduls_cicle(cicle, prog_dir, status=None):
    """Una entrada per mòdul del cicle (inclosos els de les optatives), amb
    el departament, l'estat de la PD (OK/BORRADOR/FALTA), les marques
    pendents, les incidències de la seua fulla de l'Excel i les de FE."""
    import genera_fe
    familia = get_familia(cicle)
    pd_dir = os.path.join(prog_dir, cicle)
    if not os.path.isdir(pd_dir):
        return []
    if status is None:
        status = compute_pd_status(cicle, familia, pd_dir)
    marques = {f: len(p) for f, p in status["placeholders"]}
    fitxers = {p["codi"]: p for p in status["borrador"] + status["ok"]}
    fe = {m["codi"]: m["incidencies"] for m in
          genera_fe.estat_cicle(cicle, os.path.dirname(os.path.abspath(prog_dir)))}

    moduls = []
    for codi, modul in get_moduls_del_cicle(cicle, familia).items():
        codi = str(codi)
        p = fitxers.get(codi)
        moduls.append({
            "cicle": cicle, "codi": codi, "nom": modul["nombre"],
            "departament": get_departament(familia, codi),
            "estat": p["estat"] if p else "FALTA",
            "marques": marques.get(p["filename"], 0) if p else 0,
            "excel": _issues_fulla(status["excel_issues"], modul["nombre"]),
            "fe": fe.get(codi, []),
        })
    for o in status.get("optatives", []):
        moduls.append({
            "cicle": cicle, "codi": o["codi"], "nom": o["nom"],
            "departament": get_departament(familia, o["codi"]),
            "estat": o["estat"] or "FALTA",
            "marques": marques.get(f"{OPTATIVES_DIRNAME}/{o['fitxer']}", 0) if o["fitxer"] else 0,
            "excel": _issues_fulla(status.get("opt_excel_issues", []), o["nom"]),
            "fe": [],
        })
    return moduls


def estat_departaments(prog_dir, estats_cicle=None):
    """{dept: [mòduls]} de tots els cicles. `estats_cicle` ({cicle: status})
    permet reutilitzar els compute_pd_status ja calculats."""
    estats_cicle = estats_cicle or {}
    depts = {d: [] for d in DEPARTAMENTS}
    for cicle in CICLES_INF + CICLES_SCO:
        for m in estat_moduls_cicle(cicle, prog_dir, estats_cicle.get(cicle)):
            depts.setdefault(m["departament"], []).append(m)
    return depts


def modul_verificat(m):
    return m["estat"] == "OK" and not m["marques"] and not m["excel"] and not m["fe"]


def format_dept_report(dept, moduls):
    lines = [f"=== Report Programacions Didàctiques: departament {dept} ===", ""]
    if not moduls:
        lines.append("Cap mòdul adscrit al departament.")
        return "\n".join(lines) + "\n"
    for estat in ("OK", "BORRADOR", "FALTA"):
        lines.append(f"PDs en {estat}: {sum(m['estat'] == estat for m in moduls)}")
    pendents = [m for m in moduls if not modul_verificat(m)]
    lines.append(f"Mòduls amb alguna incidència: {len(pendents)} de {len(moduls)}")
    lines.append("")
    cicle_actual = None
    for m in moduls:
        if m["cicle"] != cicle_actual:
            cicle_actual = m["cicle"]
            lines.append(f"{cicle_actual}:")
        marca = "✓" if modul_verificat(m) else "✗"
        lines.append(f"  {marca} {m['codi']} {m['nom']}: {m['estat']}")
        if m["marques"]:
            lines.append(f"      · {m['marques']} marques pendents ([###]/[...])")
        lines.extend(f"      · Excel: {i}" for i in m["excel"])
        lines.extend(f"      · FE: {i}" for i in m["fe"])
    lines.append("")
    lines.append(f"Verificat (sense marca d'esborrany): {'SI' if not pendents else 'NO'}")
    return "\n".join(lines) + "\n"


def escriu_reports_dept(prog_dir, estats_cicle=None):
    """Escriu programacions/0_report/{DEPT}/report_{DEPT}.txt de tots els
    departaments. Torna {dept: mòduls} (per a l'empremta del poller)."""
    depts = estat_departaments(prog_dir, estats_cicle)
    for dept, moduls in depts.items():
        report_dir = dir_report_dept(prog_dir, dept)
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, f"report_{dept}.txt"), "w", encoding="utf-8") as f:
            f.write(format_dept_report(dept, moduls))
    return depts


def main():
    parser = argparse.ArgumentParser(description="Genera report de PCCF o Programacions")
    parser.add_argument("cicle", nargs="?", default="", help="Cicle (ex: APD)")
    parser.add_argument("--prog-dir", default=os.environ.get("PCCF_ROOT", ".") + "/programacions",
                        help="Directori programacions/ (per a --type dept)")
    parser.add_argument("--type", choices=["pd", "pccf", "dept"], default="pd",
                        help="Tipus de report: pd (PD + Excel, dins programacions/), pccf (framework, dins pccf/) "
                             "o dept (un report per departament, de tots els cicles; el cicle s'ignora)")
    parser.add_argument("--pd-dir", help="Directori de les PD (ex: programacions/APD)")
    parser.add_argument("--pccf-dir", default=os.environ.get("PCCF_ROOT", ".") + "/pccf",
                        help="Directori del framework PCCF (conté src*/)")
    parser.add_argument("--centre", default="SENIA")
    args = parser.parse_args()

    if args.type == "dept":
        for dept, moduls in escriu_reports_dept(args.prog_dir).items():
            print(f"Report del departament {dept} ({len(moduls)} mòduls) guardat a: "
                  f"{os.path.join(dir_report_dept(args.prog_dir, dept), f'report_{dept}.txt')}")
        return

    cicle = args.cicle.upper()
    if not cicle:
        parser.error("cal indicar el cicle")
    familia = get_familia(cicle) or "INF"

    if args.type == "pd":
        pd_dir = args.pd_dir or f"programacions/{cicle}"
        status = compute_pd_status(cicle, familia, pd_dir)
        report_text = format_pd_report(status)
        report_dir = dir_report_cicle(os.path.dirname(os.path.abspath(pd_dir)))
    else:
        pccf_dir = args.pccf_dir
        status = compute_pccf_status(cicle, familia, pccf_dir)
        report_text = format_pccf_report(status)
        report_dir = os.path.join(pccf_dir, "0_report")

    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{familia}_{cicle}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(report_text)
    print(f"Report guardat a: {report_path}")


if __name__ == "__main__":
    main()
