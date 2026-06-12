#!/usr/bin/env python3

import json
import os
import sys

FAMILIAS = {
    "INF": "boe_INF",
    "SCO": "boe_SCO",
}

INFO_MSGS = []


def _celda_vacia(valor):
    """Comprueba si la celda del Excel quedaría sin letras (equivalente a vacía).
    None → 'None' (no tiene sentido como dato), [] y "" → vacío."""
    if valor is None:
        return True
    texto = str(valor)
    return not any(c.isalpha() for c in texto)


def analizar_ciclo(ruta_json, ciclo, familia):
    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        INFO_MSGS.append(f"  ERROR: No se pudo leer {ruta_json}: {e}")
        return

    nombre = data.get("CicloFormativo", ciclo)
    INFO_MSGS.append(f"\n{'='*60}")
    INFO_MSGS.append(f"  {nombre} ({ciclo}) [{familia}]")
    INFO_MSGS.append(f"{'='*60}")

    modulos = data.get("ModulosProfesionales", {})
    for codigo, modulo in modulos.items():
        mod_name = modulo.get("nombre", codigo)

        if _celda_vacia(modulo.get("ObjetivosGenerales")):
            INFO_MSGS.append(f"  ⚠ {codigo} - {mod_name}: falta ObjetivosGenerales")

        if _celda_vacia(modulo.get("CompetenciasTitulo")):
            INFO_MSGS.append(f"  ⚠ {codigo} - {mod_name}: falta CompetenciasTitulo")

    imp_comp = data.get("ImportanciaCompetencias")
    if imp_comp:
        INFO_MSGS.append(f"  ✓ ImportanciaCompetencias: definido ({len(imp_comp)} competencias)")
    else:
        INFO_MSGS.append(f"  ⚠ ImportanciaCompetencias: NO definido")


def main():
    INFO_MSGS.append("=" * 60)
    INFO_MSGS.append("  REPORTE DE ANÁLISIS DE JSONs")
    INFO_MSGS.append("  Revisa campos faltantes en los ciclos formativos")
    INFO_MSGS.append("=" * 60)

    total = 0
    for familia, dirname in FAMILIAS.items():
        if not os.path.isdir(dirname):
            INFO_MSGS.append(f"\n  Directorio no encontrado: {dirname}/")
            continue
        for fname in sorted(os.listdir(dirname)):
            if fname.startswith("rd-") and fname.endswith(".json"):
                ciclo = fname.replace("rd-", "").replace(".json", "").upper()
                ruta = os.path.join(dirname, fname)
                analizar_ciclo(ruta, ciclo, familia)
                total += 1

    if total == 0:
        INFO_MSGS.append("\n  No se encontraron archivos JSON.")

    INFO_MSGS.append(f"\n{'='*60}")
    INFO_MSGS.append(f"  Total ciclos analizados: {total}")
    INFO_MSGS.append(f"{'='*60}")

    print("\n".join(INFO_MSGS))

    ruta_reporte = "PDFS/reporte_analisis.txt"
    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write("\n".join(INFO_MSGS))
        f.write("\n")
    print(f"\n  Reporte guardado en: {ruta_reporte}")


if __name__ == "__main__":
    main()
