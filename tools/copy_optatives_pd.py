#!/usr/bin/env python3
"""Copy optative PDs that belong to a specific cycle into a temp dir for compilation."""

import os
import glob
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from pccf_utils import get_optatives, OPTATIVES_PLANTILLES

if len(sys.argv) < 4:
    print("Usage: copy_optatives_pd.py CICLO FAMILIA PLANTILLES_DIR")
    sys.exit(1)

ciclo = sys.argv[1].upper()
familia = sys.argv[2].upper()
plantilles_dir = sys.argv[3]

dest = os.path.join(plantilles_dir, ".optatives_pd")
os.makedirs(dest, exist_ok=True)

opts = get_optatives(ciclo, familia)
copied = 0
for codi in opts:
    for f in glob.glob(os.path.join(OPTATIVES_PLANTILLES, f"PD_{codi}_*.md")):
        shutil.copy(f, dest)
        copied += 1
        print(f"  \u2022 {os.path.basename(f)}")

with open(os.path.join(dest, ".copied_count"), "w") as fh:
    fh.write(str(copied))

if copied == 0:
    print(f"  (no optatives PDs for {ciclo})")
