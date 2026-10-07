#!/usr/bin/env python3
"""Validate every *.json file inside boe_INF/, boe_SCO/ and boe_OPTATIVES/.
The optional module key "dualitza" must be a boolean (false = no FEE) and
the optional key "curs" must be 1 or 2 (course where the module is taught).
A semipresencial cycle (rd-{cicle}semi.json) is a copy of its presencial
cycle (rd-{cicle}.json) and must stay in sync with it: same title data and
same modules, except "dualitza" (the SEMI cycle may have a subset of modules).
Exit code 0 → all files are valid.
Exit code 1 → at least one file is invalid (error printed to stderr).
"""
import sys
import json
import pathlib

DIRS = ["boe_INF", "boe_SCO", "boe_OPTATIVES"]

failed = False
files = []
for d in DIRS:
    files.extend(sorted(pathlib.Path(d).glob("*.json")))

print(f"🔍  Validating {len(files)} JSON files …")
for path in files:
    try:
        data = path.read_text(encoding="utf-8")
        parsed = json.loads(data)
        moduls = parsed.get("ModulosProfesionales", parsed)
        for codi, modul in moduls.items():
            if isinstance(modul, dict) and not isinstance(modul.get("dualitza", True), bool):
                print(f"❌  {path}: module {codi}: \"dualitza\" must be true/false", file=sys.stderr)
                failed = True
            if isinstance(modul, dict) and modul.get("curs", 1) not in (1, 2):
                print(f"❌  {path}: module {codi}: \"curs\" must be 1 or 2", file=sys.stderr)
                failed = True
    except Exception as exc:
        print(f"❌  Invalid JSON in {path}: {exc}", file=sys.stderr)
        failed = True

# Cicles semipresencials: còpia del presencial, han de seguir iguals.
def sense_dualitza(modul):
    return {k: v for k, v in modul.items() if k != "dualitza"}

for semi in sorted(pathlib.Path("boe_SCO").glob("rd-*semi.json")) + sorted(pathlib.Path("boe_INF").glob("rd-*semi.json")):
    base = semi.with_name(semi.name.replace("semi.json", ".json"))
    try:
        s, b = (json.loads(x.read_text(encoding="utf-8")) for x in (semi, base))
    except Exception:
        continue  # ja s'ha informat de l'error de JSON
    for clau in b:
        if clau != "ModulosProfesionales" and s.get(clau) != b[clau]:
            print(f"❌  {semi}: \"{clau}\" differs from {base}", file=sys.stderr)
            failed = True
    for codi, modul in s.get("ModulosProfesionales", {}).items():
        orig = b.get("ModulosProfesionales", {}).get(codi)
        if orig is None or sense_dualitza(modul) != sense_dualitza(orig):
            print(f"❌  {semi}: module {codi} differs from {base} (keep them in sync)", file=sys.stderr)
            failed = True

if failed:
    sys.exit(1)

print("✅  All JSON files are valid.")
