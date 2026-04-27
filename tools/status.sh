#!/bin/bash
shopt -s nullglob

OUTPUT_FILE="UP/STATUS_SUMMARY.md"
mkdir -p UP

# Fecha de actualización en formato legible
LAST_UPDATED=$(date '+%d/%m/%Y a las %H:%M:%S %Z')

{
  echo "# Resumen de Estado de Módulos"
  echo ""
  echo "> 🕒 Última actualización: **${LAST_UPDATED}**"
  echo ""
  echo "---"
  echo ""

  found_cycle=0
  for cycle_path in UP/*/; do
    [ -d "$cycle_path" ] || continue
    cycle=$(basename "$cycle_path")

    [[ "$cycle" == STATUS_SUMMARY* ]] && continue

    found_cycle=1
    echo "## $cycle"
    echo ""
    echo "| Módulo | Estado |"
    echo "|--------|--------|"

    found_module=0
    for mod_path in "$cycle_path"*/; do
      [ -d "$mod_path" ] || continue
      found_module=1
      mod=$(basename "$mod_path")
      status="pendiente"

      for f in "$mod_path"*; do
        if [ -f "$f" ] && [ "$(stat -c%s "$f" 2>/dev/null)" -gt 0 ]; then
          status="**completado**"
          break
        fi
      done

      echo "| $mod | $status |"
    done

    if [ "$found_module" -eq 0 ]; then
      echo "| (ninguno) | - |"
    fi
    echo ""
  done

  if [ "$found_cycle" -eq 0 ]; then
    echo "_No se encontraron ciclos en UP/_"
    echo ""
  fi

  echo "---"
  echo ""
  echo "_Generado automáticamente el ${LAST_UPDATED}_"

} > "$OUTPUT_FILE" || { echo "Error: no se pudo escribir $OUTPUT_FILE" >&2; exit 1; }
