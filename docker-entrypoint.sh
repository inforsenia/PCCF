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

# Segon perfil onedrive, separat i aïllat del de memòries (--confdir i procés
# --monitor propis): així un --resync o un bug en un dels dos pollers mai
# afecta l'altre sistema. Sincronitza el subpath de PCCF/Programacions.
PCCF_ONEDRIVE_CONFDIR="${PCCF_ONEDRIVE_CONFDIR:-/home/PCCF/.config/onedrive-pccf}"
PCCF_SYNC_ROOT="${PCCF_SYNC_ROOT:-/data/onedrive-pccf}"
PCCF_SUBPATH="${PCCF_SUBPATH:-General/PCCF i Programacions}"

if [ ! -f "$ONEDRIVE_CONFDIR/refresh_token" ]; then
    echo "ERROR: no hi ha refresh_token a $ONEDRIVE_CONFDIR"
    echo "Cal fer el bootstrap manual una vegada (vore README/pla) abans de desplegar."
    exit 1
fi

# El perfil de PCCF és OPCIONAL: mentre no s'haja fet el seu bootstrap manual
# (encara pendent), el contenidor arranca igualment i les memòries seguixen
# funcionant exactament igual que abans -- no bloquegem tot el desplegament
# per una peça nova que encara no s'ha configurat.
PCCF_SYNC_ENABLED=1
if [ ! -f "$PCCF_ONEDRIVE_CONFDIR/refresh_token" ]; then
    echo "AVÍS: no hi ha refresh_token a $PCCF_ONEDRIVE_CONFDIR"
    echo "Sincronització PCCF/Programacions desactivada fins que es faça el bootstrap manual (vore README/pla). Les memòries no es veuen afectades."
    PCCF_SYNC_ENABLED=0
fi

# Symlinks perquè tools/report_memories.py i tools/compilar_memories.py trobin
# les dades sincronitzades on ja les esperen (memories_{ESOBAT,FP}/{DEPART}/).
ln -sfn "$MEMORIES_SYNC_ROOT/$MEMORIES_ESOBAT_SUBPATH" /home/PCCF/memories_ESOBAT
ln -sfn "$MEMORIES_SYNC_ROOT/$MEMORIES_FP_SUBPATH" /home/PCCF/memories_FP

echo "Engegant onedrive --monitor memòries (confdir=$ONEDRIVE_CONFDIR)..."
# NOTA important (lliçó apresa): mai --resync automàtic ací. --resync només
# s'ha de fer manualment i de manera supervisada durant el bootstrap o davant
# d'un problema conegut -- fer-ho a cada arrancada del contenidor és el que
# va causar un incident real amb fitxers renombrats.
while true; do
    onedrive --confdir="$ONEDRIVE_CONFDIR" --monitor --monitor-interval=300 \
        || echo "onedrive --monitor (memòries) ha fallat, reintentant en 30s..."
    sleep 30
done &
PIDS=("$!")

echo "Engegant el poller de compilació automàtica de memòries (sync-root=$MEMORIES_SYNC_ROOT)..."
# Sense fitxer disparador: sondeja les dates de modificació dels .md reals
# contra les de l'últim report publicat, i compila+publica sol quan detecta
# un canvi (vore tools/local_sync_poller.py).
python3 /home/PCCF/tools/local_sync_poller.py --sync-root "$MEMORIES_SYNC_ROOT" &
PIDS+=("$!")

if [ "$PCCF_SYNC_ENABLED" = "1" ]; then
    # Symlink perquè el Makefile (PCCF_ROOT=pccf_sync) trobe l'estructura
    # pccf/ (src* + 0_report/ + 1_esborrany/) i programacions/{CICLO}/ (PDs + 0_report/ + 1_esborrany/).
    ln -sfn "$PCCF_SYNC_ROOT/$PCCF_SUBPATH" /home/PCCF/pccf_sync

    echo "Engegant onedrive --monitor PCCF (confdir=$PCCF_ONEDRIVE_CONFDIR)..."
    while true; do
        onedrive --confdir="$PCCF_ONEDRIVE_CONFDIR" --monitor --monitor-interval=300 \
            || echo "onedrive --monitor (PCCF) ha fallat, reintentant en 30s..."
        sleep 30
    done &
    PIDS+=("$!")

    echo "Engegant el poller de compilació automàtica de PCCF (sync-root=$PCCF_SYNC_ROOT/$PCCF_SUBPATH)..."
    # Mateix disseny (sense fitxer disparador). El poller sondeja pccf/src*/
    # per a PCCF (auto-compila) i programacions/ per a PD (report only, manual).
    # Dins del sync-root hi viuen: pccf/, programacions/, 0_report_pccf/ i
    # 1_esborrany_pccf/.
    python3 /home/PCCF/tools/pccf_sync_poller.py --sync-root "$PCCF_SYNC_ROOT/$PCCF_SUBPATH" &
    PIDS+=("$!")
fi

wait -n "${PIDS[@]}"
