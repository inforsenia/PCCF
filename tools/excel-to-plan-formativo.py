#!/usr/bin/env python3

import sys
import json
import os
import shutil
from openpyxl import load_workbook
import subprocess
import os
import warnings
warnings.filterwarnings('ignore')  # Por ahora ignoro todos los warnings

fila_inicio=10
columna_a_buscar="I"

ruta_excel = sys.argv[1]
hoja = sys.argv[2]
plan_empresa_md = sys.argv[3]
hoja_orig=hoja

if hoja.startswith("Lenguajes de marcas"): hoja="Lenguajes de marcas y sistemas "
if hoja.startswith("Desarrollo web en entorno servi") : hoja="Desarrollo Web en Entorno Servi"
if hoja.startswith("Desarrollo Web en Entorno Clien") : hoja="Desarrollo Web en Entorno Clien"
if hoja.startswith("Sostenibilidad"): hoja="Sostenibilidad aplicada al sist"
if hoja.startswith("Itinerario personal para la empleabilidad II"): hoja="IPE2"
if hoja.startswith("Itinerario personal para la empleabilidad I"): hoja="IPE1"
if hoja.startswith("Digitalización aplicada a los sectores productivos (GS)"): hoja="Digitalización aplicada a los s"
if hoja.startswith("Inglés Profesional (GM)"): hoja ="Inglés Profesional (GM)"


def generar_tabla_markdown(strings,hoja_orig):
    
    # Crear fichero y escribir
    with open(plan_empresa_md, 'a', encoding='utf-8') as fichero:
        
        print("## "+hoja_orig, file=fichero)
        print("\n\n", file=fichero)
        print("| RA       | Descripción |", file=fichero)
        print("|----------|-------------|", file=fichero)
        for s in strings:
            # Separar el código (ej: "RA06.") del resto del texto
            partes = s.split('. ', 1)
            codigo = partes[0] + '.'
            descripcion = partes[1] if len(partes) > 1 else ""
            print(f"| {codigo.ljust(8)} | {descripcion} |", file=fichero)
        print("\n\n\n",file=fichero)

# Ejemplo de uso:
strings = set()




wb = load_workbook(ruta_excel)
try:
    ws = wb[hoja]
except KeyError as ke:
    print(" * Hoja no encontrada : "+str(ke))
    sys.exit(0)

print(" * [ PCCF ] : Generando plan de Formacion en Empresa ")
for fila in range(fila_inicio, ws.max_row + 1):
        celda_actual = ws[f"{columna_a_buscar}{fila}"]
        if celda_actual.value is not None:
            # Obtener la columna anterior (ej: 'B' si columna_a_buscar es 'C')
            columna_anterior = chr(ord(columna_a_buscar) - 7)
            celda_anterior = ws[f"{columna_anterior}{fila}"]

            # Verificar si la celda anterior está fusionada
            for merged_range in ws.merged_cells.ranges:
                if celda_anterior.coordinate in merged_range:
                    # Obtener la celda superior izquierda del rango fusionado
                    celda_fusionada = ws[merged_range.start_cell.coordinate]
                    strings.add(celda_fusionada.value)
            strings.add(celda_anterior.value)

ras_ordenados=sorted(strings)
generar_tabla_markdown(ras_ordenados,hoja_orig)
