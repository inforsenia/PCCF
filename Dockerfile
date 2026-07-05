FROM ubuntu:latest
WORKDIR /home/PCCF
# Actualizar el sistema e instalar dependencias
RUN apt-get update && apt-get install -y \
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
