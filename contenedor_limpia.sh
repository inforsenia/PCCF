#!/bin/bash
# contenedor_limpia.sh
# Script para limpiar contenedores e imágenes Docker

echo "========================================"
echo "  LIMPIANDO CONTENEDORES PCCF"
echo "========================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detener y eliminar contenedores
echo "Deteniendo y eliminando contenedores..."
docker compose -f "$SCRIPT_DIR/docker-compose.yml" down

# Preguntar si eliminar también la imagen
read -p "¿Quieres eliminar también la imagen? (s/n): " ELIMINAR_IMAGEN

if [[ $ELIMINAR_IMAGEN == "s" || $ELIMINAR_IMAGEN == "S" ]]; then
    echo "Eliminando imagen..."
    docker image rm $(docker images -q pccf-pccf) 2>/dev/null || echo "Imagen no encontrada o ya eliminada"
fi

# Limpiar contenedores huérfanos
echo "Limpiando contenedores huérfanos..."
docker container prune -f

# Limpiar imágenes no utilizadas
echo "Limpiando imágenes no utilizadas..."
docker image prune -f

echo "========================================"
echo "  LIMPIEZA COMPLETADA"
echo "========================================"