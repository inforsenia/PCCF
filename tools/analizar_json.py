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
    """Comprueba si un valor está vacío (None, [] o "").
    Los números (int/float) o strings numéricos se consideran válidos."""
    if valor is None:
        return True
    if isinstance(valor, (int, float)):
        return False
    if isinstance(valor, str):
        if valor.strip().lstrip('-').replace('.', '', 1).isdigit():
            return False
        return not any(c.isalpha() for c in valor)
    if isinstance(valor, list):
        return len(valor) == 0
    return False


# Claves esperadas en cada módulo
CLAVES_MODULO = {
    "nombre", "codigo", "horas", "creditos",
    "ResultadosAprendizaje",
    "UnidadesCompetenciaAcreditadas",
    "ObjetivosGenerales",
    "CompetenciasTitulo",
}
# Orden de presentación
CLAVES_MODULO_ORDER = [
    "nombre", "codigo", "horas", "creditos",
    "ResultadosAprendizaje",
    "UnidadesCompetenciaAcreditadas",
    "ObjetivosGenerales",
    "CompetenciasTitulo",
]

# Claves en valencià/català que haurien d'estar en castellà
CLAVES_CATALAN = {
    "credits": "creditos",
    "ObjectiusGenerals": "ObjetivosGenerales",
    "CompetènciesTitulo": "CompetenciasTitulo",
}


def analizar_ciclo(ruta_json, ciclo, familia, claves_globales):
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
        claves_modulo = set(modulo.keys())

        # Reportar claus en valencià
        for cat, esp in CLAVES_CATALAN.items():
            if cat in claves_modulo:
                INFO_MSGS.append(f"  ✗ {codigo} - {mod_name}: clau en valencià '{cat}' → hauria de ser '{esp}'")

        # Reportar faltas de claves esperadas
        for clave in CLAVES_MODULO_ORDER:
            if clave in ("nombre", "codigo"):
                continue
            if clave not in claves_modulo or _celda_vacia(modulo.get(clave)):
                INFO_MSGS.append(f"  ⚠ {codigo} - {mod_name}: falta {clave}")

        # Reportar faltas de claves que existen en otros ciclos
        for clave in sorted(claves_globales - CLAVES_MODULO - set(CLAVES_CATALAN.keys())):
            if clave not in claves_modulo:
                INFO_MSGS.append(f"  ⚠ {codigo} - {mod_name}: falta {clave} (presente en otros ciclos)")

    imp_comp = data.get("ImportanciaCompetencias")
    if imp_comp:
        INFO_MSGS.append(f"  ✓ ImportanciaCompetencias: definido ({len(imp_comp)} competencias)")
    else:
        INFO_MSGS.append(f"  ⚠ ImportanciaCompetencias: NO definido")


def _escanear_claves_globales():
    """Primera pasada: recoge todas las claves de módulo de todos los JSONs."""
    claves = set()
    for familia, dirname in FAMILIAS.items():
        if not os.path.isdir(dirname):
            continue
        for fname in sorted(os.listdir(dirname)):
            if not (fname.startswith("rd-") and fname.endswith(".json")):
                continue
            try:
                with open(os.path.join(dirname, fname), "r", encoding="utf-8") as f:
                    data = json.load(f)
                for mod in data.get("ModulosProfesionales", {}).values():
                    claves.update(mod.keys())
            except (FileNotFoundError, json.JSONDecodeError):
                pass
    return claves


def main():
    INFO_MSGS.append("=" * 60)
    INFO_MSGS.append("  REPORTE DE ANÁLISIS DE JSONs")
    INFO_MSGS.append("  Revisa campos faltantes en los ciclos formativos")
    INFO_MSGS.append("=" * 60)

    claves_globales = _escanear_claves_globales()

    total = 0
    for familia, dirname in FAMILIAS.items():
        if not os.path.isdir(dirname):
            INFO_MSGS.append(f"\n  Directorio no encontrado: {dirname}/")
            continue
        for fname in sorted(os.listdir(dirname)):
            if fname.startswith("rd-") and fname.endswith(".json"):
                ciclo = fname.replace("rd-", "").replace(".json", "").upper()
                ruta = os.path.join(dirname, fname)
                analizar_ciclo(ruta, ciclo, familia, claves_globales)
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
