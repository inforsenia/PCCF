# Modulo de Python para funciones comunes del PCCF

def get_hoja_label(hoja):

    ## INFORMATICA

    # Comunes
    if hoja.startswith("Llenguatges de marques"): return "LM"
    if hoja.startswith("Sostenibilitat"): return "SOS"
    if hoja.startswith("Itinerari personal per a l'ocupabilitat II"): return "IPO2"
    if hoja.startswith("Itinerari personal per a l'ocupabilitat I"): return "IPO1"
    if hoja.startswith("Digitalització"): return "DIG"
    if hoja.startswith("Anglés Professional"): return "ANG"
    if hoja.startswith("Anglés oral"): return "AOEP"
    if hoja.startswith("Comunicació professional"): return "COM"
    if hoja.startswith("Projecte intermodular"): return "PI"
    if hoja.startswith("Introducció al Núvol"): return "NVL"

    # SMX
    if hoja.startswith("Muntatge"): return "MME"
    if hoja.startswith("Sistemes operatius mono"): return "SOM"
    if hoja.startswith("Aplicacions ofimátiques"): return "AOF"
    if hoja.startswith("Sistemes operatius en xarxa"): return "SOX"
    if hoja.startswith("Seguretat informàtica"): return "SIN"
    if hoja.startswith("Serveis en xarxa"): return "SEX"
    if hoja.startswith("Aplicacions web"): return "AW"
    if hoja.startswith("Xarxes locals"): return "XL"

    # DAM DAW
    if hoja.startswith("Entorns de"): return "ED"
    if hoja.startswith("Sistemes Informàtics"): return "SI"
    if hoja.startswith("Bases de "): return "BBDD"
    # Específicos antes que el genérico "Programació"
    if hoja.startswith("Programació de serveis i pro"): return "PSP"
    if hoja.startswith("Programació multimèdia i dispo"): return "PMDM"
    if hoja.startswith("Programació"): return "PRG"

    # DAM
    if hoja.startswith("Desenvolupament d'inter"): return "DI"
    if hoja.startswith("Accés a "): return "AD"
    if hoja.startswith("Sistemes de gestió empresarial"): return "SGE"

    # CEIABD
    if hoja.startswith("Models d"): return "MIA"
    if hoja.startswith("Sistemes d"): return "SAA"
    if hoja.startswith("Programació d"): return "PIA"
    if hoja.startswith("Sistemes de"): return "SBD"
    if hoja.startswith("Big Data"): return "BDA"

    # FPBIIO
    # Se usa MMEB para evitar conflicto con MME de SMX (Muntatge i manteniment d'equips)
    if hoja.startswith("Montatge i manteniment"): return "MMEB"
    if hoja.startswith("Operacions auxiliars"): return "OA"
    if hoja.startswith("Ofimàtica"): return "OAD"
    if hoja.startswith("Instal·lació i manteniment"): return "IMXTD"
    if hoja.startswith("Ciències aplicades I"): return "CA1"
    if hoja.startswith("Ciències aplicades II"): return "CA2"
    if hoja.startswith("Comunicació i societat I"): return "CS1"
    if hoja.startswith("Comunicació i societat II"): return "CS2"

    ## SERVEIS A LA COMUNITAT

    # APD
    if hoja.startswith("Organització de l'atenció"): return "OAPD"
    if hoja.startswith("Destreses socials"): return "DDSS"
    if hoja.startswith("Característiques i necessitats"): return "CNP"
    if hoja.startswith("Atenció i suport psicosocial"): return "ASP"
    if hoja.startswith("Suport a la comunicació"): return "SC"
    if hoja.startswith("Suport domiciliari"): return "SD"
    if hoja.startswith("Atenció sanitària"): return "AS"
    if hoja.startswith("Atenció higiènica"): return "AH"
    if hoja.startswith("Teleassistència"): return "TEL"
    if hoja.startswith("Primers auxilis"): return "PA"

    # EI
    if hoja.startswith("Didàctica de l'educació infantil"): return "DEI"
    if hoja.startswith("Autonomia personal i salut infantil"): return "APSI"
    if hoja.startswith("El joc infantil"): return "JOC"
    if hoja.startswith("Expressió i comunicació"): return "EC"
    if hoja.startswith("Desenvolupament cognitiu"): return "DCM"
    if hoja.startswith("Desenvolupament socioafectiu"): return "DSA"
    if hoja.startswith("Habilitats socials"): return "HHSS"
    if hoja.startswith("Intervenció amb famílies"): return "IFAM"
    if hoja.startswith("Projecte d'atenció"): return "PAI"

    # IS
    if hoja.startswith("Context de la intervenció social"): return "CIS"
    if hoja.startswith("Inserció sociolaboral"): return "ISL"
    if hoja.startswith("Atenció a les unitats de convivència"): return "AUC"
    if hoja.startswith("Mediació comunitària"): return "MC"
    if hoja.startswith("Suport a la intervenció educativa"): return "SIE"
    if hoja.startswith("Promoció de l'autonomia personal"): return "PAP"
    if hoja.startswith("Sistemes augmentatius"): return "SAAC"
    if hoja.startswith("Metodologia de la intervenció social"): return "MIS"

    return hoja
