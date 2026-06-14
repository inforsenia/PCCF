#!/usr/bin/env python3
"""Validate every *.json file inside boe_INF/ and boe_SCO/.
Exit code 0 → all files are valid.
Exit code 1 → at least one file is invalid (error printed to stderr).
"""
import sys
import json
import pathlib

DIRS = ["boe_INF", "boe_SCO"]

failed = False
files = []
for d in DIRS:
    files.extend(sorted(pathlib.Path(d).glob("*.json")))

print(f"🔍  Validating {len(files)} JSON files …")
for path in files:
    try:
        data = path.read_text(encoding="utf-8")
        json.loads(data)
    except Exception as exc:
        print(f"❌  Invalid JSON in {path}: {exc}", file=sys.stderr)
        failed = True

if failed:
    sys.exit(1)

print("✅  All JSON files are valid.")
