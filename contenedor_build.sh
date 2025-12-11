#!/bin/bash
# contenedor_build.sh
# Script para construir la imagen Docker del proyecto PCCF

echo "========================================"
echo "  CONSTRUYENDO IMAGEN DOCKER PCCF"
echo "========================================"

# Directorio actual
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Directorio del proyecto: $PROJECT_ROOT"

# Verificar que existe docker-compose.yml
if [ ! -f "$SCRIPT_DIR/docker-compose.yml" ]; then
    echo "ERROR: No se encuentra docker-compose.yml en $SCRIPT_DIR"
    exit 1
fi

# Verificar que existe Dockerfile
if [ ! -f "$SCRIPT_DIR/Dockerfile" ]; then
    echo "ERROR: No se encuentra Dockerfile en $SCRIPT_DIR"
    exit 1
fi

# Construir la imagen
echo "Construyendo imagen Docker..."
docker compose -f "$SCRIPT_DIR/docker-compose.yml" build --no-cache

# Verificar si la construcción fue exitosa
if [ $? -eq 0 ]; then
    echo "========================================"
    echo "  IMAGEN CONSTRUIDA EXITOSAMENTE"
    echo "========================================"
    echo ""
    echo "Para lanzar el contenedor, ejecuta:"
    echo "  ./contenedor_lanza.sh"
    echo ""
    echo "O para una sesión interactiva directa:"
    echo "  ./contenedor_lanza.sh bash"
else
    echo "========================================"
    echo "  ERROR EN LA CONSTRUCCIÓN"
    echo "========================================"
    exit 1
fi