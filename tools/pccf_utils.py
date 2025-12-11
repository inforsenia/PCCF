# Modulo de Python para funciones comunes del PCCF

def get_hoja_label(hoja):
    # Comunes
    if hoja.startswith("Lenguajes de marcas"): hoja="LM"
    if hoja.startswith("Sostenibilidad"): hoja="Sostenibilidad"
    if hoja.startswith("Itinerario personal para la empleabilidad II"): hoja="IPE2"
    if hoja.startswith("Itinerario personal para la empleabilidad I"): hoja="IPE1"
    if hoja.startswith("Digitalización"): hoja="Digitalización"
    if hoja.startswith("Inglés Profesional"): hoja ="Inglés"

    if hoja.startswith("Montaje y "): hoja="MME"
    if hoja.startswith("Sistemas operativos monopuesto"): hoja="SOM"
    if hoja.startswith("Aplicaciones ofimáticas"): hoja="AOF"
    if hoja.startswith("Sistemas operativos en red"): hoja="SOX"
    if hoja.startswith("Seguridad informática"): hoja="SIN"
    if hoja.startswith("Servicios en red"): hoja="SRE"
    if hoja.startswith("Aplicaciones web"): hoja="AW"
    if hoja.startswith("Redes Locales"): hoja="Redes"

    # DAM DAW
    
    if hoja.startswith("Entornos de"): hoja = "ED"
    if hoja.startswith("Sistemas Informáticos"): hoja="SI"
    if hoja.startswith("Bases de "): hoja="BBDD"
    if hoja.startswith("Programación"): hoja="PROG"

    # DAW
    if hoja.startswith("Desarrollo web en entorno servi") : hoja="DWES"
    if hoja.startswith("Desarrollo Web en Entorno Clien") : hoja="DWEC"
    if hoja.startswith("Despliegue de") : hoja="DAW"
    if hoja.startswith("Diseño de interfaces web") : hoja="DIW"

    # DAM
    if hoja.startswith("Desarrollo de Inter") : hoja="DI"
    if hoja.startswith("Acceso a ") : hoja="AD"
    if hoja.startswith("Programación multimedia y dispo"): hoja="PMDM"
    if hoja.startswith("Programación de servicios y pro"): hoja="PSP"
    if hoja.startswith("Sistemas de gestión empresarial"): hoja="SGE"

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

    # CEIABD
    if hoja.startswith("Models d"): hoja = "MIA"
    if hoja.startswith("Sistemes d"): hoja = "SAA"
    if hoja.startswith("Programació d"): hoja = "PIA"
    if hoja.startswith("Sistemes de"): hoja = "SBD"
    if hoja.startswith("Big Data"): hoja = "BDA"

    # FPBIIO
    if hoja.startswith("Montatge i manteniment"): hoja = "MME"
    if hoja.startswith("Operacions auxiliars"): hoja = "OA"
    if hoja.startswith("Ofimàtica"): hoja = "OAD"
    if hoja.startswith("Instal·lació i manteniment"): hoja = "IMXTD"
    if hoja.startswith("Ciències aplicades I"): hoja = "CA1"
    if hoja.startswith("Ciències aplicades II"): hoja = "CA2"
    if hoja.startswith("Comunicació i societat I"): hoja = "CS1"
    if hoja.startswith("Comunicació i societat II"): hoja = "CS2"

    return hoja
