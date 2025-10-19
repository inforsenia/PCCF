# Modulo de Python para funciones comunes del PCCF

def get_hoja_label(hoja):
    # Comunes
    if hoja.startswith("Lenguajes de marcas"): hoja="LM"
    if hoja.startswith("Sostenibilidad"): hoja="Sostenibilidad"
    if hoja.startswith("Itinerario personal para la empleabilidad II"): hoja="IPE2"
    if hoja.startswith("Itinerario personal para la empleabilidad I"): hoja="IPE1"
    if hoja.startswith("Digitalización aplicada a los sectores productivos (GS)"): hoja="Digitalización"
    if hoja.startswith("Inglés Profesional"): hoja ="Inglés"


    # DAW
    if hoja.startswith("Desarrollo web en entorno servi") : hoja="DWES"
    if hoja.startswith("Desarrollo Web en Entorno Clien") : hoja="DWEC"

    # ASIR
    if hoja.startswith("Implantación de Siste"): hoja = "ISO"
    if hoja.startswith("Administración de Sistemas Oper"): hoja = "ASO"
    if hoja.startswith("Planificación y Administración"): hoja = "PAX"
    if hoja.startswith("Fundamentos de Hard"): hoja = "FHW"
    if hoja.startswith("Gestión de Base de Datos"): hoja = "GBD"
    if hoja.startswith("Administración de Sistemas Ge"): hoja = "ASGBD"
    if hoja.startswith("Servicios de Red e I") : hoja = "SER"
    if hoja.startswith("Seguridad y Alt"): hoja = "SAD"
    if hoja.startswith("Implantación de Aplicaci"): hoja = "IAW"
    
    return hoja