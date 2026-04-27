#!/bin/bash
shopt -s nullglob

OUTPUT_FILE="UP/STATUS_SUMMARY.md"

{
  echo "# Resumen de Estado de Módulos"
  echo ""

  for cycle_path in UP/*/; do
    [ -d "$cycle_path" ] || continue
    cycle=$(basename "$cycle_path")

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

    if [ $found_module -eq 0 ]; then
      echo "| (ninguno) | - |"
    fi
    echo ""
  done
} > "$OUTPUT_FILE"