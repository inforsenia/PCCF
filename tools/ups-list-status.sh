#!/bin/bash

echo " * Procesador de UPs por Modulo"

if [ $# -ne 1 ]; then
	echo " Numero de argumento incorrecto"
	exit 1
fi

DIST=$(lsb_release -is)

PANDOC_OPTS="--template ../../../rsrc/templates/eisvogel.latex"

# Dirty Hack
if [ $DIST = "Fedora" ]; then

	PANDOC_OPTS=""

fi

CICLO=$1

if [ ! -d UP/$CICLO ]; then
	echo " * El Ciclo no existen "
	exit 1
fi	

cd UP/$CICLO/

echo "Procesando Markdowns/odts"

for updir in $(ls -1); do
	cd $updir
	echo -n " ** ${updir} "
	HAYMDS=$(cat *.md| wc -l)

	if [ $HAYMDS -ge 1 ]; then
		echo -n " --> $HAYMDS lineas: UPS OK"
	else
		echo -n " --> ODT? "
		HAYODT=$(find . -name "*.odt" | wc -l)
		if [ $HAYODT -gt 0 ]; then
			echo -n " ODT Presente: UPS OK"
		else
			echo -n " FALTAN UPS : UPS ERROR"
		fi
	fi
	echo ""
	cd ..
done

cd -


exit 0
