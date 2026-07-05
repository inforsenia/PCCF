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
COPY . .

RUN chmod +x docker-entrypoint.sh
