# Modulo de Python para funciones comunes del PCCF

import os
import re
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

CICLES_INF = ["SMX", "DAM", "CEIABD", "FPBIIO"]
CICLES_SCO = ["APD", "EI", "IS"]
CICLES_CONEGUTS = sorted(CICLES_INF + CICLES_SCO, key=len, reverse=True)

# Frase de contextualització de cada cicle per a "... que s'imparteix en
# {contexto}." de templates/_base_pd.md (plantilla única de PD per a tots
# els cicles i famílies). Únic lloc on viu este text. CEIABD és un Curs
# d'Especialització (no un "Cicle de Grau X"), per això és una frase
# completa i no un grau+títol descompost.
# Decret autonòmic de currículum, per al subapartat "Marc normatiu" de la PD.
# Només per als cicles de grau mitjà i superior (Decret 114/2025, art. 1).
# FPBIIO (grau bàsic) i CEIABD (curs d'especialització) es regulen per una
# altra norma: sense "curriculum", la plantilla remet al PCCF.
D114_CURRICULUM = "Decret 114/2025, de 29 de juliol, del Consell, pel qual s'establixen els currículums dels cicles formatius de grau mitjà i de grau superior de Formació Professional"

CICLE_INFO = {
    "SMX": {"contexto": "el Cicle Formatiu de Grau Mitjà de \nTècnic en Sistemes Microinformàtics i Xarxes", "curriculum": D114_CURRICULUM},
    "DAM": {"contexto": "el Cicle Formatiu de Grau Superior de \nTècnic Superior en Desenvolupament d'Aplicacions Multiplataforma", "curriculum": D114_CURRICULUM},
    "CEIABD": {"contexto": "el Curs d'Especialització en Intel·ligència Artificial i Big Data"},
    "FPBIIO": {"contexto": "el Cicle Formatiu de Grau Bàsic de \nTècnic Bàsic en Informàtica d'Oficina"},
    "APD": {"contexto": "el Cicle Formatiu de Grau Mitjà de \nTècnic en Atenció a Persones en Situació de Dependència", "curriculum": D114_CURRICULUM},
    "EI": {"contexto": "el Cicle Formatiu de Grau Superior de \nTècnic Superior en Educació Infantil", "curriculum": D114_CURRICULUM},
    "IS": {"contexto": "el Cicle Formatiu de Grau Superior de \nTècnic Superior en Integració Social", "curriculum": D114_CURRICULUM},
}

# Frase de contextualització per a les PD d'optatives (compartides entre cicles).
CONTEXTO_OPTATIVA = "el cicle formatiu corresponent"

# Plantilla única de PD (templates/), usada per json2pccf.py i json2optatives.py.
PD_TEMPLATE = "_base_pd.md"

# Mòduls que no dualitzen (sense hores de FEE ni RA requisit per a la FEE):
# porten "dualitza": false al JSON (boe_*/rd-*.json o optatives.json). Sense
# la clau, el mòdul dualitza. La PD no porta la subsecció de Formació en
# empresa i la fulla de l'Excel no té REQUISIT FE / HORES DUAL.
def dualitza(modulo):
    return modulo.get("dualitza", True) is not False


# Curs (1 o 2) en què s'imparteix el mòdul: clau opcional "curs" del JSON.
# Sense la clau torna None (la plantilla RRAA_CA de FE l'agrupa a part).
def get_curs(modulo):
    curs = modulo.get("curs")
    return curs if curs in (1, 2) else None


# Primera pestanya dels llibres Excel de PD (excel_estils.escriu_instruccions):
# no és cap mòdul i els lectors del llibre l'han de saltar.
HOJA_INSTRUCCIONS = "Instruccions"


OPTATIVES_PATH = os.path.join(PROJECT_DIR, "boe_OPTATIVES", "optatives.json")

# Pattern per a noms de fitxer PD:
# PD_{CICLO}_{CODI}_{NOM}_{BORRADOR|OK}.md
PD_FILE_RE = re.compile(
    r'^PD_(' + '|'.join(CICLES_CONEGUTS) + r')_(\d+|[A-Z][A-Z0-9]*)_(.+?)_(BORRADOR|OK)\.md$'
)


# Sigles de cada mòdul: nom de la fulla a libro_{CICLE}.xlsx i
# libro_optatives.xlsx (Excel limita el nom a 31 caràcters: amb el nom
# complet, IPO I/II tallats quedaven iguals i Excel en reanomenava un a
# "Recuperado_Hoja1"). Es tria el prefix MÉS LLARG que coincidix, perquè
# l'ordre de la llista no importe ("Programació" vs "Programació d'...",
# "... I" vs "... II").
HOJA_LABELS = [
    ('Llenguatges de marques', 'LM'),
    ('Sostenibilitat', 'SOS'),
    ("Itinerari personal per a l'ocupabilitat II", 'IPO2'),
    ("Itinerari personal per a l'ocupabilitat I", 'IPO1'),
    ('Digitalització', 'DIG'),
    ('Anglés Professional', 'ANG'),
    ('Anglés oral', 'AOEP'),
    ('Comunicació professional', 'COM'),
    ('Acompanyament a les persones amb discapacitat', 'ACD'),
    ("Activitats d'oci i temps lliure", 'OTL'),
    ('Projecte intermodular', 'PI'),
    ('Introducció al Núvol', 'NVL'),
    ('Muntatge', 'MME'),
    ('Sistemes operatius mono', 'SOM'),
    ('Aplicacions ofimàtiques', 'AOF'),
    ('Sistemes operatius en xarxa', 'SOX'),
    ('Seguretat informàtica', 'SIN'),
    ('Serveis en xarxa', 'SEX'),
    ('Aplicacions web', 'AW'),
    ('Xarxes Locals', 'XL'),
    ('Introducció a la Programació', 'IPR'),
    ('Entorns de', 'ED'),
    ('Sistemes Informàtics', 'SI'),
    ('Bases de ', 'BBDD'),
    ('Programació de serveis i pro', 'PSP'),
    ('Programació multimèdia i dispo', 'PMDM'),
    ('Programació', 'PRG'),
    ("Desenvolupament d'inter", 'DI'),
    ('Accés a ', 'AD'),
    ('Sistemes de gestió empresarial', 'SGE'),
    ('Models d', 'MIA'),
    ('Sistemes d', 'SAA'),
    ('Programació d', 'PIA'),
    ('Sistemes de', 'SBD'),
    ('Big Data', 'BDA'),
    ('Montatge i manteniment', 'MMEB'),
    ('Operacions auxiliars', 'OA'),
    ('Ofimàtica', 'OAD'),
    ('Instal·lació i manteniment', 'IMXTD'),
    ('Ciències aplicades I', 'CA1'),
    ('Ciències aplicades II', 'CA2'),
    ('Comunicació i societat I', 'CS1'),
    ('Comunicació i societat II', 'CS2'),
    ("Organització de l'atenció", 'OAPD'),
    ('Destreses socials', 'DDSS'),
    ('Característiques i necessitats', 'CNP'),
    ('Atenció i suport psicosocial', 'ASP'),
    ('Suport a la comunicació', 'SC'),
    ('Suport domiciliari', 'SD'),
    ('Atenció sanitària', 'AS'),
    ('Atenció higiènica', 'AH'),
    ('Teleassistència', 'TEL'),
    ('Primers auxilis', 'PA'),
    ("Didàctica de l'educació infantil", 'DEI'),
    ('Autonomia personal i salut infantil', 'APSI'),
    ('El joc infantil', 'JOC'),
    ('Expressió i comunicació', 'EC'),
    ('Desenvolupament cognitiu', 'DCM'),
    ('Desenvolupament socioafectiu', 'DSA'),
    ('Habilitats socials', 'HHSS'),
    ('Intervenció amb famílies', 'IFAM'),
    ("Projecte d'atenció", 'PAI'),
    ('Context de la intervenció social', 'CIS'),
    ('Inserció sociolaboral', 'ISL'),
    ('Atenció a les unitats de convivència', 'AUC'),
    ('Mediació comunitària', 'MC'),
    ('Suport a la intervenció educativa', 'SIE'),
    ("Promoció de l'autonomia personal", 'PAP'),
    ('Sistemes augmentatius', 'SAAC'),
    ('Metodologia de la intervenció social', 'MIS'),
    ('Ciències aplicades 1', 'CA1'),
    ('Ciències aplicades 2', 'CA2'),
    ('Comunicació i societat 1', 'CS1'),
    ('Comunicació i societat 2', 'CS2'),
]

_STOPWORDS = {"de", "del", "i", "a", "al", "als", "la", "les", "el", "els", "en", "per", "amb", "d", "l"}


def _sigles_automatiques(nom):
    """Inicials de les paraules significatives + numeral final (I, II, 1, 2...)."""
    paraules = re.findall(r"[\w·]+", nom.replace("'", " "))
    final = paraules[-1] if paraules and re.fullmatch(r"[IVX]+|\d+", paraules[-1]) else ""
    if final:
        paraules = paraules[:-1]
    sigles = "".join(p[0].upper() for p in paraules if p.lower() not in _STOPWORDS)
    return (sigles + final)[:31]


def get_hoja_label(hoja):
    """Sigla del mòdul `hoja` (nom complet). Sense entrada a HOJA_LABELS,
    torna el nom si cap en 31 caràcters o, si no, unes sigles automàtiques."""
    candidats = [(pre, lab) for pre, lab in HOJA_LABELS if hoja.startswith(pre)]
    if candidats:
        return max(candidats, key=lambda c: len(c[0]))[1]
    return hoja if len(hoja) <= 31 else _sigles_automatiques(hoja)


def get_familia(cicle):
    cicle = cicle.upper()
    if cicle in CICLES_INF:
        return "INF"
    if cicle in CICLES_SCO:
        return "SCO"
    return None


def get_moduls_del_cicle(cicle, familia=None):
    if familia is None:
        familia = get_familia(cicle)
    if familia is None:
        return {}
    json_path = os.path.join(PROJECT_DIR, f"boe_{familia}", f"rd-{cicle.lower()}.json")
    if not os.path.exists(json_path):
        return {}
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("ModulosProfesionales", {})


def get_optatives(cicle=None, familia=None):
    """Carrega boe_OPTATIVES/optatives.json i filtra per cicle/familia.

    Si cicle i familia es donen, retorna només els mòduls optatius que
    pertanyen a eixe cicle (segons el camp 'grups').
    Si no, retorna tots.
    """
    if not os.path.exists(OPTATIVES_PATH):
        return {}
    with open(OPTATIVES_PATH, encoding="utf-8") as f:
        optatives = json.load(f)

    if cicle is None or familia is None:
        return optatives

    cicle = cicle.upper()
    familia = familia.upper()
    result = {}
    for codi, modul in optatives.items():
        for g in modul.get("grups", []):
            if g.get("cicle", "").upper() == cicle and g.get("familia", "").upper() == familia:
                # Si hi ha codi alternatiu per a este cicle, usem-lo
                codi_real = modul.get("codis_alternatius", {}).get(cicle, codi)
                result[codi_real] = modul
                break
    return result


# Fitxers de PD d'optatives a programacions/OPTATIVES/: PD_{CODI}_{NOM}_{BORRADOR|OK}.md
OPT_PD_FILE_RE = re.compile(r'^PD_(\d+|[A-Z][A-Z0-9]*)_(.+?)_(BORRADOR|OK)\.md$')
OPTATIVES_DIRNAME = "OPTATIVES"
OPTATIVES_LIBRO = "libro_optatives.xlsx"


def get_optatives_del_cicle(cicle, familia):
    """Optatives que pertanyen al cicle, com a llista de (codi, modul).

    `codi` és la clau d'optatives.json: la que porten els fitxers
    PD_{codi}_*.md de programacions/OPTATIVES/. No és el codi alternatiu
    del cicle (codis_alternatius) que torna get_optatives(), i que no
    correspon a cap fitxer (p.ex. INP és CVOPS190 per a DAM).
    """
    cicle = cicle.upper()
    familia = familia.upper()
    return [
        (codi, modul) for codi, modul in get_optatives().items()
        if any(g.get("cicle", "").upper() == cicle and g.get("familia", "").upper() == familia
               for g in modul.get("grups", []))
    ]


def find_optativa_pd(opt_dir, codi):
    """Nom del fitxer de PD de l'optativa `codi` dins opt_dir (l'_OK té
    prioritat sobre el _BORRADOR), o None si no existeix."""
    try:
        files = os.listdir(opt_dir)
    except OSError:
        return None
    trobats = sorted(f for f in files if (m := OPT_PD_FILE_RE.match(f)) and m.group(1) == codi)
    ok = [f for f in trobats if f.endswith("_OK.md")]
    return (ok or trobats or [None])[0]


def get_moduls_merged(cicle, familia=None):
    """Fusiona els mòduls del cicle + optatives que pertanyen al cicle.

    Retorna un dict {codi: modul} on els codis alternatius es resolen
    automàticament.
    """
    moduls = get_moduls_del_cicle(cicle, familia)
    optatives = get_optatives(cicle, familia)
    # Les optatives sobreescriuen si hi ha conflicte (no n'hi hauria)
    moduls.update(optatives)
    return moduls


def parse_pd_filename(filename):
    """Parseja un nom de fitxer PD i retorna un dict o None."""
    if not filename.endswith(".md"):
        return None
    m = PD_FILE_RE.match(filename)
    if not m:
        return None
    return {
        "filename": filename,
        "ciclo": m.group(1),
        "codi": m.group(2),
        "nom": m.group(3),
        "estat": m.group(4),
    }


def _fmt_h(h):
    return str(int(h)) if float(h).is_integer() else f"{h:.2f}".rstrip("0").rstrip(".")


def hores_fulla(ws):
    """Hores al centre (HORES, F) i en empresa (HORES DUAL, I, si la fulla
    en té) de les files de criteri (E amb text, fora de "TOTS"). Llig les
    cel·les i no les fórmules de capçalera: un llibre generat amb openpyxl no
    en té el valor calculat. Torna (centre, dual, errors)."""
    dual = any(c.value == "HORES DUAL" for c in ws[8])
    centre = empresa = 0.0
    errors = []
    for r in range(10, ws.max_row + 1):
        ce = ws.cell(row=r, column=5).value
        if not isinstance(ce, str) or ce.strip() in ("", "TOTS"):
            continue
        for col, nom in ((6, "HORES"),) + (((9, "HORES DUAL"),) if dual else ()):
            v = ws.cell(row=r, column=col).value
            if v is None or v == "":
                continue
            try:
                h = float(str(v).replace(",", "."))
            except ValueError:
                errors.append(f"  Fulla '{ws.title}': fila {r}, {nom} no numèric '{v}'")
                continue
            if col == 6:
                centre += h
            else:
                empresa += h
    return centre, empresa, errors


def hores_per_fulla(moduls):
    """{nom de fulla: hores del mòdul} a partir dels mòduls del JSON. Claus
    amb les sigles (get_hoja_label) i, per als llibres antics, el nom."""
    mapa = {}
    for modul in moduls:
        try:
            hores = float(str(modul.get("horas", "")).replace(",", "."))
        except ValueError:
            continue
        nom = modul["nombre"]
        for clau in (get_hoja_label(nom), nom, nom[:31]):
            mapa.setdefault(clau, hores)
    return mapa


def check_excel_coherence(filepath, hores_moduls=None):
    """Valida la coherència de l'Excel de pesos RA i, si es passa
    `hores_moduls` ({fulla: hores del mòdul}, vore hores_per_fulla), que
    HORES + HORES DUAL de cada fulla sumen les hores del mòdul.

    Retorna una llista de missatges d'error (buida si tot correcte).
    """
    issues = []
    if not os.path.exists(filepath):
        return ["Excel no trobat: " + filepath]

    try:
        import openpyxl
    except ImportError:
        return []

    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
    except Exception as e:
        return [f"Error en obrir Excel: {e}"]

    for sheet_name in wb.sheetnames:
        if sheet_name == HOJA_INSTRUCCIONS:
            continue
        ws = wb[sheet_name]
        # Buscar columna C (RA weights) i sumar
        total_weight = 0
        ra_count = 0
        errors = []
        for row in ws.iter_rows(min_row=2, max_col=3, values_only=False):
            cell_b = row[1] if len(row) > 1 else None
            cell_c = row[2] if len(row) > 2 else None
            # Sols mirem files on la columna B comença per "RA" (descripció RA)
            if not (cell_b and cell_b.value and str(cell_b.value).strip().startswith("RA")):
                continue
            if cell_c and cell_c.value is not None:
                try:
                    val = float(cell_c.value)
                    total_weight += val
                    ra_count += 1
                except (ValueError, TypeError):
                    errors.append(f"  Fila {cell_c.row}: valor no numèric '{cell_c.value}'")

        if ra_count > 0:
            if abs(total_weight - 100) > 0.01:
                issues.append(
                    f"  Fulla '{sheet_name}': suma de pesos RA = {total_weight:.1f}% (hauria de ser 100%)"
                )
        else:
            issues.append(f"  Fulla '{sheet_name}': sense dades de pesos RA")

        for e in errors:
            issues.append(e)

        if hores_moduls and sheet_name in hores_moduls:
            centre, empresa, errors_h = hores_fulla(ws)
            issues.extend(errors_h)
            esperat = hores_moduls[sheet_name]
            if abs(centre + empresa - esperat) > 0.01:
                detall = (f"HORES ({_fmt_h(centre)}) + HORES DUAL ({_fmt_h(empresa)}) = {_fmt_h(centre + empresa)} h"
                          if any(c.value == "HORES DUAL" for c in ws[8]) else f"HORES = {_fmt_h(centre)} h")
                issues.append(f"  Fulla '{sheet_name}': {detall}, però el mòdul té {_fmt_h(esperat)} h")

    wb.close()
    return issues
