#!/bin/bash
# shell-progs-didacticas-standalone.sh
# Usage: shell-progs-didacticas-standalone.sh <CICLO> [base_dir]
#   base_dir: path to plantilles directory (default: ./)
#   Standalone PDs are expected in <base_dir>/temp_<CICLO>/

CICLO="$1"
BASE_DIR="${2:-.}"

# Resolve to absolute paths
BASE_DIR_ABS="$(realpath "${BASE_DIR}")"
STANDALONE_DIR="${BASE_DIR_ABS}/temp_${CICLO}"

if [ ! -d "${STANDALONE_DIR}" ]; then
    echo " * Nothing to do here (${STANDALONE_DIR} not found)"
    exit 1
fi

# Find the project root (parent of base_dir if base_dir is plantilles_*, else current dir)
PROJECT_ROOT="$(realpath "${BASE_DIR_ABS}/..")"
TEMPLATE_TEX_PD="${PROJECT_ROOT}/rsrc/templates/eisvogel.latex"
PANDOC_OPTIONS="-V fontsize=12pt -V mainfont=\"${PROJECT_ROOT}/rsrc/sorts-mill-goudy/OFLGoudyStM.otf\" -V toc-title=\"Índex\" --pdf-engine=xelatex"
PDF_DIR="${PROJECT_ROOT}/PDFS"

echo " * [ ProgsDidacticas ] CICLO : ${CICLO} (base: ${BASE_DIR_ABS})"
mkdir -p "${PDF_DIR}/PDs_${CICLO}"
rm -f "${PDF_DIR}/PDs_${CICLO}"/*

cd "${STANDALONE_DIR}"

# Leer mapa código → siglas (generado por json2pccf.py)
SIGLAS_JSON=".module_siglas.json"

for d in $(ls -1); do
    [ ! -d "$d" ] && continue
    siglas=""
    if [ -f "$SIGLAS_JSON" ]; then
        siglas=$(python3 -c "import json; m=json.load(open('$SIGLAS_JSON')); print(m.get('$d',''))" 2>/dev/null)
    fi
    [ -n "$siglas" ] && siglas="_${siglas}"
    echo -n " * [ ProgsDidacticas ] Modulo - Codigo : ${d}${siglas} -> "
    cd "$d"
    pandoc --template "${TEMPLATE_TEX_PD}" ${PANDOC_OPTIONS} -o "${PDF_DIR}/PDs_${CICLO}/PD_${CICLO}_${d}${siglas}.pdf" ./PD_*.md
    if [ -f "./PD_9999_CuadroResumen.pdf" ]; then
        echo " Existe Cuadro Resumen, aplicando pdfunite"
        pdfunite "${PDF_DIR}/PDs_${CICLO}/PD_${CICLO}_${d}${siglas}.pdf" "./PD_9999_CuadroResumen.pdf" "/tmp/PD_${CICLO}_${d}${siglas}.pdf"
        mv "/tmp/PD_${CICLO}_${d}${siglas}.pdf" "${PDF_DIR}/PDs_${CICLO}/PD_${CICLO}_${d}${siglas}.pdf"
    else
        echo " No tiene Cuadro Resumen"
    fi
    cd ..
done

exit 0
