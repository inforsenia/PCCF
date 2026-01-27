# Modulo de Python para funciones comunes del PCCF

def get_hoja_label(hoja):
    # Comunes
    if hoja.startswith("Lenguajes de marcas"): hoja="LM"
    if hoja.startswith("Sostenibilitat"): hoja="Sostenibilitat"
    if hoja.startswith("Itinerari personal per a l'ocupabilitat II"): hoja="IPO2"
    if hoja.startswith("Itinerari personal per a l'ocupabilitat I"): hoja="IPO1"
    if hoja.startswith("Digitalització"): hoja="Digitalització"
    if hoja.startswith("Anglés Professional"): hoja ="Anglés"

    if hoja.startswith("Muntatge"): hoja="MME"
    if hoja.startswith("Sistemes operatius mono"): hoja="SOM"
    if hoja.startswith("Aplicacions ofimátiques"): hoja="AOF"
    if hoja.startswith("Sistemes operatius en xarxa"): hoja="SOX"
    if hoja.startswith("Seguretat informàtica"): hoja="SIN"
    if hoja.startswith("Serveis en xarxa"): hoja="SEX"
    if hoja.startswith("Aplicacions web"): hoja="AW"
    if hoja.startswith("Xarxes locals"): hoja="XL"

    # DAM DAW
    if hoja.startswith("Entorns de"): hoja = "ED"
    if hoja.startswith("Sistemes Informàtics"): hoja="SI"
    if hoja.startswith("Bases de "): hoja="BBDD"
    if hoja.startswith("Programació"): hoja="PRG"

    # DAM
    if hoja.startswith("Desenvolupament d'Inter") : hoja="DI"
    if hoja.startswith("Accés a ") : hoja="AD"
    if hoja.startswith("Programació multimèdia i dispo"): hoja="PMDM"
    if hoja.startswith("Programació de serveis i pro"): hoja="PSP"
    if hoja.startswith("Sistemes de gestió empresarial"): hoja="SGE"

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
