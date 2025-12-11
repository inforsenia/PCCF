#!/bin/bash
# contenedor_lanza.sh
# Script para lanzar el contenedor Docker del proyecto PCCF

echo "========================================"
echo "  LANZANDO CONTENEDOR PCCF"
echo "========================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verificar que existe docker-compose.yml
if [ ! -f "$SCRIPT_DIR/docker-compose.yml" ]; then
    echo "ERROR: No se encuentra docker-compose.yml en $SCRIPT_DIR"
    exit 1
fi

# Opciones por defecto
MODE="interactive"
COMMAND="bash"

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--detach)
            MODE="detach"
            shift
            ;;
        -c|--command)
            COMMAND="$2"
            shift 2
            ;;
        -h|--help)
            echo "Uso: $0 [OPCIONES]"
            echo ""
            echo "Opciones:"
            echo "  -d, --detach          Ejecutar en segundo plano"
            echo "  -c, --command COMANDO Ejecutar comando específico (default: bash)"
            echo "  -h, --help            Mostrar esta ayuda"
            echo ""
            echo "Ejemplos:"
            echo "  $0                     # Sesión interactiva con bash"
            echo "  $0 -d                  # Iniciar en segundo plano"
            echo "  $0 --command \"make proyecto-daw\"  # Ejecutar comando específico"
            echo "  $0 --command \"ls -la\"           # Listar archivos"
            exit 0
            ;;
        *)
            # Si se pasa un argumento sin opción, asumimos que es un comando
            if [[ -z "$COMMAND_SET" ]]; then
                COMMAND="$1"
                COMMAND_SET=1
            fi
            shift
            ;;
    esac
done

# Verificar si el contenedor ya está corriendo
if docker ps --format '{{.Names}}' | grep -q "^pccf$"; then
    echo "El contenedor 'pccf' ya está corriendo."
    echo "¿Qué quieres hacer?"
    echo "  1) Acceder al contenedor corriendo"
    echo "  2) Detener y recrear el contenedor"
    echo "  3) Salir"
    read -p "Opción [1-3]: " OPTION
    
    case $OPTION in
        1)
            echo "Accediendo al contenedor existente..."
            docker exec -it pccf $COMMAND
            exit 0
            ;;
        2)
            echo "Deteniendo y eliminando contenedor existente..."
            docker compose -f "$SCRIPT_DIR/docker-compose.yml" down
            ;;
        3)
            echo "Saliendo..."
            exit 0
            ;;
        *)
            echo "Opción no válida. Saliendo..."
            exit 1
            ;;
    esac
fi

# Ejecutar según el modo seleccionado
case $MODE in
    "detach")
        echo "Iniciando contenedor en segundo plano..."
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" up -d
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "Contenedor iniciado en segundo plano."
            echo "Para acceder a él, ejecuta:"
            echo "  docker exec -it pccf bash"
            echo ""
            echo "Para ver los logs:"
            echo "  docker logs -f pccf"
            echo ""
            echo "Para detenerlo:"
            echo "  docker compose -f $SCRIPT_DIR/docker-compose.yml down"
        fi
        ;;
    "interactive")
        echo "Iniciando sesión interactiva con comando: $COMMAND"
        echo ""
        
        # Usar docker compose run para sesión interactiva
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" run --rm pccf $COMMAND
        
        if [ $? -eq 0 ]; then
            echo "========================================"
            echo "  SESIÓN FINALIZADA"
            echo "========================================"
        else
            echo "========================================"
            echo "  ERROR EN LA EJECUCIÓN"
            echo "========================================"
        fi
        ;;
esac