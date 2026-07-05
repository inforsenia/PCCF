FROM ubuntu:latest
WORKDIR /home/PCCF

# Zona horària fixada a nivell de sistema (no només la variable d'entorn TZ
# de docker-compose, que no totes les eines respecten) -- evita que noms de
# fitxer amb data/hora (p. ex. els timestamps de report/PDF) isquen en UTC
# en compte de l'hora local.
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Actualizar el sistema e instalar dependencias
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tzdata \
    make \
    pandoc \
    texlive-extra-utils \
    texlive-lang-spanish \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-xetex \
    texlive-luatex \
    texlive-publishers \
    libreoffice \
    poppler-utils \
    python3-jinja2 \
    python3-box \
    python3-numpy \
    python3-pandas \
    python3-openpyxl \
    python3-matplotlib \
    fonts-ubuntu \
    onedrive \
    && rm -rf /var/lib/apt/lists/*

# Codi del repositori (per al desplegament autònom des de GitHub/Portainer).
# En desenvolupament local, docker-compose.yml el sobreescriu amb un bind mount.
# --chown és necessari: el contenidor corre com a usuari 1000:1000 (no root),
# i sense això /home/PCCF quedaria de root, impedint crear-hi els symlinks
# (docker-entrypoint.sh) -- causa exacta d'un "ln: Permission denied" real.
COPY --chown=1000:1000 . .

# --chown de COPY només afecta el contingut, no la pròpia carpeta /home/PCCF
# (creada per WORKDIR, propietat de root) -- cal canviar-ho explícitament.
RUN chown 1000:1000 /home/PCCF && chmod +x docker-entrypoint.sh
