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

mkdir -p ../../../PDFS/UPS-$MODULO/

pandoc -o ../../../PDFS/UPS-$MODULO/PD-UP-$MODULO.pdf ${PANDOC_OPTS} *.md



cd -


exit 0
