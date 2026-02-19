#!/bin/bash

if [ ! -d ./temp_$1 ]; then
    echo " * Nothing to do here "
    exit 1 
fi

TEMPLATE_TEX_PD="../../rsrc/templates/eisvogel.latex"
PANDOC_OPTIONS="-V fontsize=12pt -V toc-title="Índx" -V --pdf-engine=xelatex"
TEMPLATE_TEX_TASK="../../rsrc/templates/eisvogel.latex"

echo " * [ ProgsDidacticas ] CICLO : $1"
mkdir -p PDFS/PDs_$1
rm -f PDFS/PDs_$1/*

cd ./temp_$1/

for d in $(ls -1); do 
    echo -n " * [ ProgsDidacticas ] Modulo - Codigo : $d -> "
    cd $d
    pandoc --template ${TEMPLATE_TEX_PD} ${PANDOC_OPTIONS} -o ../../PDFS/PDs_$1/PD_$1_$d.pdf ./PD_*.md
    if [ -f "./PD_9999_CuadroResumen.pdf" ]; then
        echo " Existe Cuadro Resumen, aplicando pdfunite"
        pdfunite ../../PDFS/PDs_$1/PD_$1_$d.pdf "PD_9999_CuadroResumen.pdf" /tmp/PD_$1_$d.pdf
        mv /tmp/PD_$1_$d.pdf ../../PDFS/PDs_$1/PD_$1_$d.pdf
    else
        echo " No tiene Cuadro Resumen"
    fi
    cd ..
done

exit 0