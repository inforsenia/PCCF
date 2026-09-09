#!/bin/bash

echo " * Procesador de UPs por Modulo"

if [ $# -ne 2 ]; then
	echo " Numero de argumento incorrecto"
	exit 1
fi

DIST=$(lsb_release -is)

PANDOC_OPTS="--template ../../../rsrc/templates/eisvogel.latex"

# Dirty Hack
if [ $DIST = "Fedora" ]; then

	PANDOC_OPTS=""

fi

MODULO=$2
CICLO=$1

if [ ! -d UP/$CICLO/$MODULO ]; then
	echo " * El Ciclo / Modulo no existen "
	exit 1
fi	

cd UP/$CICLO/$MODULO

echo "Procesando Mds"

HAYMDS=$(cat *.md| wc -l)

if [ $HAYMDS -ge 1 ]; then
	mkdir -p ../../../PDFS/UPS-$MODULO/
	pandoc -o ../../../PDFS/UPS-$MODULO/PD-UP-$MODULO.pdf ${PANDOC_OPTS} *.md
else
	echo " * En este Modulo $CICLO -> $MODULO no hay UPs en Markdown"
	echo " * * Veamos si hay ODTs "
	HAYODT=$(ls *.odt| wc -l)

	if [ $HAYODT -ge 0 ]; then
		echo " * * Los hay "
		for odt in $(find . -name "*.odt"); do
			echo " * * + WiP con $odt"
			soffice  --convert-to 'pdf:writer_pdf_Export' --outdir ../../../PDFS/UPS-$MODULO/ $odt
		done
	fi
fi


cd -


exit 0
