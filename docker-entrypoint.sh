#!/usr/bin/env bash
# Entrypoint per al desplegament autònom (Portainer/git). NO s'usa en el
# desenvolupament local interactiu (docker-compose.yml hi manté `tail -f /dev/null`).
set -euo pipefail

ONEDRIVE_CONFDIR="${ONEDRIVE_CONFDIR:-/home/PCCF/.config/onedrive}"
# Path DINS del contenidor (no té per què coincidir amb cap path real de cap
# màquina concreta) -- el path real a l'amfitrió es defineix al bind mount
# del docker-compose corresponent (portainer: /docker/pccf/onedrive_memories).
MEMORIES_SYNC_ROOT="${MEMORIES_SYNC_ROOT:-/data/onedrive-memories}"
MEMORIES_ESOBAT_SUBPATH="${MEMORIES_ESOBAT_SUBPATH:-General/Memòries ESO-BAT}"
MEMORIES_FP_SUBPATH="${MEMORIES_FP_SUBPATH:-General/Memòries FP}"

if [ ! -f "$ONEDRIVE_CONFDIR/refresh_token" ]; then
    echo "ERROR: no hi ha refresh_token a $ONEDRIVE_CONFDIR"
    echo "Cal fer el bootstrap manual una vegada (vore README/pla) abans de desplegar."
    exit 1
fi

# Symlinks perquè tools/report_memories.py i tools/compilar_memories.py trobin
# les dades sincronitzades on ja les esperen (memories_{ESOBAT,FP}/{DEPART}/).
ln -sfn "$MEMORIES_SYNC_ROOT/$MEMORIES_ESOBAT_SUBPATH" /home/PCCF/memories_ESOBAT
ln -sfn "$MEMORIES_SYNC_ROOT/$MEMORIES_FP_SUBPATH" /home/PCCF/memories_FP

echo "Engegant onedrive --monitor (confdir=$ONEDRIVE_CONFDIR)..."
# NOTA important (lliçó apresa): mai --resync automàtic ací. --resync només
# s'ha de fer manualment i de manera supervisada durant el bootstrap o davant
# d'un problema conegut -- fer-ho a cada arrancada del contenidor és el que
# va causar un incident real amb fitxers renombrats.
while true; do
    onedrive --confdir="$ONEDRIVE_CONFDIR" --monitor --monitor-interval=300 \
        || echo "onedrive --monitor ha fallat, reintentant en 30s..."
    sleep 30
done &
ONEDRIVE_PID=$!

# TODO (pendent, tasca #11 del pla): llançar ací el poller que detecta
# fitxers de disparador (Verificar/Compilar) i crida report_memories.py /
# compilar_memories.py / publish_memories_output.py. De moment, el
# contenidor només manté la sincronització viva; el report/compila es
# continua llançant manualment via `docker exec`.

wait "$ONEDRIVE_PID"
