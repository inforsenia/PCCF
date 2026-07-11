#!/usr/bin/env python3
"""Report status of shared optative PDs: BORRADOR vs OK, [###] placeholders."""

import os
import sys
import re
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from pccf_utils import PROJECT_DIR

parser = argparse.ArgumentParser()
parser.add_argument("--pd-dir", help="Directori de les PDs optatives")
args = parser.parse_args()

pd_dir = args.pd_dir or os.path.join(PROJECT_DIR, "programacions", "OPTATIVES")
if not os.path.isdir(pd_dir):
    print(f"  No existeix {pd_dir}/")
    sys.exit(0)

# Pattern: PD_{CODI}_{NOM}_{BORRADOR|OK}.md
pat = re.compile(r'^PD_(\d+|[A-Z]+)_(.+?)_(BORRADOR|OK)\.md$')

found = 0
for f in sorted(os.listdir(pd_dir)):
    m = pat.match(f)
    if not m:
        continue
    found += 1
    codi = m.group(1)
    nom = m.group(2)
    estat = m.group(3)
    has_placeholder = False
    with open(os.path.join(pd_dir, f), encoding="utf-8") as fh:
        if "[###]" in fh.read():
            has_placeholder = True
    ph = " [###]" if has_placeholder else ""
    ok_mark = " [OK]" if estat == "OK" else ""
    print(f"  {estat:8s} {codi:12s} {nom}{ph}{ok_mark}")

if found == 0:
    print("  (no optatives PD found)")
