#!/bin/bash
cd /home/PCCF
python3 tools/json2pccf.py APD SCO --outdir plantilles_SCO_APD/.compila --generate-competences
echo "=== ORDRE ==="
find src src_SCO src_SCO_APD plantilles_SCO_APD/.compila -maxdepth 1 -name 'PCCF_*.md' -type f 2>/dev/null | \
  while IFS= read -r f; do
    b=$(basename "$f")
    n=$(echo "$b" | cut -d_ -f2)
    echo "$n:$f"
  done | sort -t: -k1 -n | cut -d: -f2-
rm -rf plantilles_SCO_APD/.compila
