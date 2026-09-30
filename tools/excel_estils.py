# Estils compartits del llibre Excel de PD (libro_{CICLE}.xlsx i
# libro_optatives.xlsx). Únic lloc on viuen colors, lletres i vores: abans
# json2excel.py i json2optatives.py duplicaven trames (darkTrellis/gray125)
# que al Quadre Resum del PDF es veien com un gris brut i poc llegible.
#
# escriu_capcalera() escriu la capçalera (files 1-5) i aplica_estils() s'aplica
# com a passada final sobre la fulla ja construïda, identificant cada tipus de
# fila de la taula pel seu contingut ("TOTS", OBJECTIUS/COMPETENCIES).

from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.dimensions import DimensionHolder
import os

from pccf_utils import HOJA_INSTRUCCIONS

LLETRA = "Liberation Sans"
MIDA = 10
MIDA_CAPCALERA = 12       # capçaleres de columna i etiquetes del mòdul
MIDA_MODUL = 15           # totals de la banda 2
MIDA_BANDA1 = 20          # nom, codi i hores del mòdul (banda 1)
MIDA_ETIQUETA_BANDA1 = 10

COLOR_FOSC = "1F3A5F"      # capçalera del mòdul i totals
COLOR_MIG = "2F5597"       # capçaleres de columna
COLOR_CLAR = "DCE6F1"      # files "TOTS" i etiquetes OBJECTIUS/COMPETENCIES
COLOR_VORA = "8EA9C1"

FILA_CAPCALERA = 8         # fila de "RESULTAT D'APRENENTATGE", "% RA", ...
COL_INI = 2                # B
COL_COMP = "D"
CENTRAT = Alignment(horizontal="center", vertical="center")
AMPLE_COMP = 12
COL_PERCENT_RA = "C"
AMPLE_RA = 40              # RESULTAT D'APRENENTATGE (B)
AMPLE_PERCENT_RA = 6.3
# Les 4 columnes numèriques porten la capçalera girada 90° per a poder ser
# estretes; les files 8-9 (capçalera fusionada) han de tindre alçada per al text.
AMPLE_NUMERIQUES = 5.25
# Amplàries de criteris (E) i continguts (J): el Quadre Resum del PDF
# inclou B..J i LibreOffice l'ajusta a l'ample de pàgina, així que
# l'amplària total fixa l'escala (i la mida del text) al PDF.
COL_CE = "E"
AMPLE_CE = 88
AMPLE_CONTINGUTS = 23      # continguts resumits
ALT_CAPCALERA = 30         # punts per fila (x2); el text girat fa 2 línies
GIRAT = Alignment(horizontal="center", vertical="center", text_rotation=90, wrap_text=True)
# Capçalera de la fulla (files 1-5), escrita per escriu_capcalera() i comuna
# a json2excel.py i json2optatives.py:
#   Banda 1 (files 1-2): MÒDUL (B:E) | CODI (F:I) | HORES (J)
#   Banda 2 (files 4-5): OBJECTIUS GENERALS (B:D) | COMPETÈNCIES (E) |
#                        H. CENTRE (F:G) | H. DUAL (H:I) |
#                        TOTAL HORES (J) = centre + dual
# Cada bloc: etiqueta a la primera fila i valor a la segona. Les hores del
# mòdul (JSON) són les hores al centre (HORES dels CE) més les hores en
# empresa (HORES DUAL): TOTAL HORES es posa en roig mentre no hi quadra
# (pccf_utils.check_excel_coherence ho valida després). Cap codi llig estes
# cel·les; la taula comença a FILA_CAPCALERA (no canvia).
#
# Un mòdul que no dualitza (pccf_utils.dualitza) no té les columnes
# REQUISIT FE (H) ni HORES DUAL (I): CONTINGUTS passa a H i la capçalera
# queda MÒDUL (B:E) | CODI (F:G) | HORES (H) i OBJECTIUS (B:D) |
# COMPETÈNCIES (E:F) | TOTAL HORES (G:H) = HORES, sense H. CENTRE ni H. DUAL.
FILES_BANDA1 = (1, 2)
FILES_BANDA2 = (4, 5)
# Les fórmules sumen les columnes HORES (F) i HORES DUAL (I); /2 perquè cada
# RA també té la fila "TOTS" amb la suma dels seus CE.
FORMULA_TOTAL = "=SUM(F8:F200)/2"
FORMULA_TOTAL_DUAL = "=SUM(I8:I200)/2"
FORMULA_TOTAL_CENTRE_DUAL = "=SUM(F8:F200)/2+SUM(I8:I200)/2"
ROIG = PatternFill("solid", fgColor="F4B6B6", bgColor="F4B6B6")
VERD = PatternFill("solid", fgColor="C6E7C6", bgColor="C6E7C6")
FILES_BUIDES = (3, 6, 7)   # separadors entre bandes i taula
ESQUERRA = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)

BLANC = PatternFill("solid", fgColor="FFFFFF")
FOSC = PatternFill("solid", fgColor=COLOR_FOSC)
MIG = PatternFill("solid", fgColor=COLOR_MIG)
CLAR = PatternFill("solid", fgColor=COLOR_CLAR)

_fina = Side(style="thin", color=COLOR_VORA)
_grossa = Side(style="medium", color=COLOR_FOSC)
VORA = Border(left=_fina, right=_fina, top=_fina, bottom=_fina)
VORA_INICI_RA = Border(left=_fina, right=_fina, top=_grossa, bottom=_fina)

# REQUISIT FE (H) dels mòduls que dualitzen: C = compartit (centre i
# empresa), E = sols empresa, buida = sols centre. La llig genera_fe.py per a
# la plantilla RRAA_CA de la coordinació de FE i per a la taula FE de la PD.
COL_FE = 8
VALORS_FE = ("C", "E")


def disposicio(dual):
    """Columnes de la fulla segons si el mòdul dualitza."""
    if dual:
        return {
            "col_fi": 10,                        # J
            "col_continguts": 10,
            "numeriques": range(6, 10),          # HORES, % CE, REQUISIT FE, HORES DUAL (F..I)
            "banda1": (("MÒDUL", 2, 5, "nom"), ("CODI", 6, 9, "codi"), ("HORES", 10, 10, "hores")),
            "banda2": (("OBJECTIUS GENERALS", 2, 4, "objectius"), ("COMPETÈNCIES", 5, 5, "competencies"),
                       ("H. CENTRE", 6, 7, "total_centre"), ("H. DUAL", 8, 9, "total_dual"),
                       ("TOTAL HORES", 10, 10, "total")),
        }
    return {
        "col_fi": 8,                             # H
        "col_continguts": 8,
        "numeriques": range(6, 8),               # HORES, % CE (F..G)
        "banda1": (("MÒDUL", 2, 5, "nom"), ("CODI", 6, 7, "codi"), ("HORES", 8, 8, "hores")),
        "banda2": (("OBJECTIUS GENERALS", 2, 4, "objectius"), ("COMPETÈNCIES", 5, 6, "competencies"),
                   ("TOTAL HORES", 7, 8, "total")),
    }


def _lletra(col):
    return chr(ord("A") + col - 1)


def _font(bold=False, blanc=False, size=MIDA):
    return Font(name=LLETRA, size=size, bold=bold, color="FFFFFF" if blanc else "000000")


def escriu_capcalera(ws, codi, modul, dual=True):
    """Escriu (i fusiona) les dues bandes de la capçalera de la fulla."""
    d = disposicio(dual)
    valors = {
        "nom": modul.nombre,
        "codi": codi,
        "hores": _numero(modul.horas),
        "objectius": ", ".join(str(x) for x in (modul.get("ObjetivosGenerales") or [])),
        "competencies": ", ".join(str(x) for x in (modul.get("CompetenciasTitulo") or [])),
        "total": FORMULA_TOTAL_CENTRE_DUAL if dual else FORMULA_TOTAL,
        "total_centre": FORMULA_TOTAL,
        "total_dual": FORMULA_TOTAL_DUAL,
    }
    for (fila_etiqueta, fila_valor), blocs in ((FILES_BANDA1, d["banda1"]), (FILES_BANDA2, d["banda2"])):
        for etiqueta, c0, c1, clau in blocs:
            if c1 > c0:
                ws.merge_cells(start_row=fila_etiqueta, start_column=c0, end_row=fila_etiqueta, end_column=c1)
                ws.merge_cells(start_row=fila_valor, start_column=c0, end_row=fila_valor, end_column=c1)
            ws.cell(row=fila_etiqueta, column=c0).value = etiqueta
            ws.cell(row=fila_valor, column=c0).value = valors[clau]
    _marca_total(ws, d)


def _numero(valor):
    """Hores del JSON ("233") com a número, perquè es puguen comparar."""
    try:
        f = float(str(valor).replace(",", "."))
    except ValueError:
        return valor
    return int(f) if f.is_integer() else f


def _marca_total(ws, d):
    """TOTAL HORES en roig si no coincidix amb les HORES del mòdul, en verd si sí."""
    blocs = {clau: (c0, c1) for _e, c0, c1, clau in d["banda1"] + d["banda2"]}
    c0, c1 = blocs["total"]
    total = f"{_lletra(c0)}{FILES_BANDA2[1]}"
    hores = f"${_lletra(blocs['hores'][0])}${FILES_BANDA1[1]}"
    rang = f"{total}:{_lletra(c1)}{FILES_BANDA2[1]}"
    ws.conditional_formatting.add(rang, FormulaRule(formula=[f"ABS({total}-{hores})>0.01"], fill=ROIG, stopIfTrue=True))
    ws.conditional_formatting.add(rang, FormulaRule(formula=[f"ABS({total}-{hores})<=0.01"], fill=VERD))


def _estil_bloc(ws, fila, c0, c1, fill, font, alignment, border=None):
    for col in range(c0, c1 + 1):
        c = ws.cell(row=fila, column=col)
        c.fill = fill
        c.font = font
        c.alignment = alignment
        if border:
            c.border = border


def aplica_estils(ws, dual=True):
    d = disposicio(dual)
    col_fi = d["col_fi"]
    numeriques = d["numeriques"]
    ultima = ws.max_row

    # Fons blanc i lletra uniforme a tota la taula
    for row in ws.iter_rows(min_row=1, max_row=ultima, min_col=COL_INI, max_col=col_fi):
        for c in row:
            c.fill = BLANC
            c.font = _font()

    # Banda 1: identificació del mòdul (etiqueta menuda, valor gran)
    fe, fv = FILES_BANDA1
    for _etiqueta, c0, c1, clau in d["banda1"]:
        al = ESQUERRA if clau == "nom" else CENTRAT  # etiqueta alineada amb el seu valor
        _estil_bloc(ws, fe, c0, c1, MIG, _font(bold=True, blanc=True, size=MIDA_ETIQUETA_BANDA1), al)
        if clau == "codi":  # els codis d'optativa (MOPACOMDIS...) no caben en F:G dels mòduls no duals
            al = Alignment(horizontal="center", vertical="center", shrink_to_fit=True)
        _estil_bloc(ws, fv, c0, c1, FOSC, _font(bold=True, blanc=True, size=MIDA_BANDA1), al)
    ws.row_dimensions[fe].height = 18
    ws.row_dimensions[fv].height = 36

    # Banda 2: objectius, competències i totals
    fe, fv = FILES_BANDA2
    for _etiqueta, c0, c1, clau in d["banda2"]:
        al = CENTRAT if clau.startswith("total") else ESQUERRA
        _estil_bloc(ws, fe, c0, c1, CLAR, Font(name=LLETRA, size=9, bold=True, color=COLOR_FOSC), al, VORA)
        if clau.startswith("total"):
            _estil_bloc(ws, fv, c0, c1, BLANC, _font(bold=True, size=MIDA_MODUL), CENTRAT, VORA)
        else:
            _estil_bloc(ws, fv, c0, c1, BLANC, _font(size=MIDA_CAPCALERA), ESQUERRA, VORA)
    ws.row_dimensions[fe].height = 16
    ws.row_dimensions[fv].height = 30

    for r in FILES_BUIDES:
        ws.row_dimensions[r].height = 6

    # Capçaleres de columna (files 8-9, fusionades)
    for r in (FILA_CAPCALERA, FILA_CAPCALERA + 1):
        for col in range(COL_INI, col_fi + 1):
            c = ws.cell(row=r, column=col)
            c.fill = MIG
            c.font = _font(bold=True, blanc=True, size=MIDA_CAPCALERA)
            c.border = VORA
            if col in numeriques:
                c.alignment = GIRAT
        ws.row_dimensions[r].height = ALT_CAPCALERA

    # Cos: vores a totes les cel·les, vora grossa a l'inici de cada RA
    # (fila "TOTS"), i ressalt de "TOTS" i de les etiquetes de competències
    for r in range(FILA_CAPCALERA + 2, ultima + 1):
        inici_ra = ws.cell(row=r, column=5).value == "TOTS"
        for col in range(COL_INI, col_fi + 1):
            c = ws.cell(row=r, column=col)
            c.border = VORA_INICI_RA if inici_ra else VORA
            if inici_ra and 5 <= col < col_fi:  # CONTINGUTS (última columna) queda en blanc: l'omple el docent
                c.fill = CLAR
                c.font = _font(bold=True)
        for col in numeriques:
            ws.cell(row=r, column=col).alignment = CENTRAT
        comp = ws.cell(row=r, column=4)
        if comp.value in ("OBJECTIUS", "COMPETENCIES"):
            comp.fill = CLAR
            comp.font = _font(bold=True, size=9)
        ra = ws.cell(row=r, column=2)
        if isinstance(ra.value, str) and ra.value.startswith("RA"):
            ra.font = _font(bold=True)

    if dual:
        _valida_fe(ws, ultima)
    protegeix(ws, dual, ultima)
    aplica_amplades(ws, dual)


def es_dual(ws):
    """Una fulla ja generada dualitza si té la columna HORES DUAL."""
    return any(c.value == "HORES DUAL" for c in ws[FILA_CAPCALERA])


def aplica_amplades(ws, dual):
    """Amplàries de disseny de les columnes B..CONTINGUTS. Les fixen el
    Quadre Resum del PDF (s'ajusta a l'ample de pàgina, així que l'amplària
    total decidix la mida del text). excel-to-pdfs.py la torna a aplicar
    abans d'exportar: les descarta si el docent les ha canviades (llibres
    antics) i torna a mostrar les files/columnes amagades."""
    d = disposicio(dual)
    amplades = {COL_INI: AMPLE_RA, 3: AMPLE_PERCENT_RA, 4: AMPLE_COMP, 5: AMPLE_CE,
                d["col_continguts"]: AMPLE_CONTINGUTS}
    amplades.update({col: AMPLE_NUMERIQUES for col in d["numeriques"]})
    # Dimensions noves (una per columna): openpyxl agrupa les columnes
    # contigües d'igual amplària en un sol <col min max>, i modificar-ne una
    # del mig deixaria definicions solapades.
    ws.column_dimensions = DimensionHolder(worksheet=ws, default_factory=ws._add_column)
    for col, ample in amplades.items():
        ws.column_dimensions[_lletra(col)].width = ample
    for rd in ws.row_dimensions.values():
        rd.hidden = False


def _valida_fe(ws, ultima):
    """Desplegable C/E a REQUISIT FE (H) de les files de criteri."""
    dv = DataValidation(type="list", formula1='"' + ",".join(VALORS_FE) + '"', allow_blank=True,
                        showErrorMessage=True, errorTitle="REQUISIT FE",
                        error="C = compartit (centre i empresa), E = sols empresa, buit = sols centre",
                        promptTitle="REQUISIT FE",
                        prompt="C = compartit (centre i empresa)\nE = sols empresa\nbuit = sols centre")
    dv.showInputMessage = True
    ws.add_data_validation(dv)
    lletra = _lletra(COL_FE)
    for r in range(FILA_CAPCALERA + 2, ultima + 1):
        ce = ws.cell(row=r, column=5).value
        if isinstance(ce, str) and ce and ce != "TOTS":
            dv.add(f"{lletra}{r}")


# Protecció de la fulla: tot el que ve del JSON (RA, CE, codi, hores del
# mòdul, objectius, competències) i les fórmules (TOTS, totals) queden
# bloquejats. El docent només pot escriure a les cel·les pròpies:
# % RA (C), COMP (D, sota OBJECTIUS/COMPETENCIES), HORES (F), % CE (G),
# REQUISIT FE (H) i HORES DUAL (I) si dualitza, i CONTINGUTS.
# Contrasenya opcional per variable d'entorn (el repositori és públic);
# sense ella, la protecció evita errors però es pot llevar des d'Excel.
EDITABLE = Protection(locked=False)


def protegeix(ws, dual, ultima=None):
    d = disposicio(dual)
    ultima = ultima or ws.max_row
    cols_ce = [6, 7] + ([COL_FE, COL_FE + 1] if dual else [])
    for r in range(FILA_CAPCALERA + 2, ultima + 1):
        ra = ws.cell(row=r, column=2).value
        if isinstance(ra, str) and ra.startswith("RA"):
            for col in (3, d["col_continguts"]):  # cel·la superior de les fusionades
                ws.cell(row=r, column=col).protection = EDITABLE
        ce = ws.cell(row=r, column=5).value
        if isinstance(ce, str) and ce and ce != "TOTS":
            for col in cols_ce:
                ws.cell(row=r, column=col).protection = EDITABLE
            comp = ws.cell(row=r, column=4)
            if comp.value not in ("OBJECTIUS", "COMPETENCIES"):
                comp.protection = EDITABLE
    p = ws.protection
    p.sheet = True
    # Es pot canviar l'alçada de les files (CONTINGUTS és una cel·la fusionada
    # i Excel no l'ajusta sola), però no l'amplària de les columnes: fixa la
    # mida del text al Quadre Resum del PDF (vore aplica_amplades).
    p.formatRows = False
    p.formatColumns = True
    p.selectLockedCells = False
    p.selectUnlockedCells = False
    contrasenya = os.environ.get("EXCEL_PROTECCIO_PASSWORD")
    if contrasenya:
        p.password = contrasenya


INSTRUCCIONS = [
    ("titol", "Llibre de programacions — {titol}"),
    ("text", "Este llibre conté una pestanya per mòdul (amb les sigles del mòdul). De cada pestanya ix "
             "l'Esquema general (Quadre Resum) que s'afig al final de la programació didàctica del mòdul "
             "en compilar les Programacions, i la plantilla RRAA_CA que rep la coordinació de Formació en Empresa."),
    ("seccio", "Què és protegit"),
    ("text", "Els RA, els criteris d'avaluació, el codi, les hores del mòdul, els objectius generals i les "
             "competències venen del currículum (BOE/DOGV) i no es poden modificar. Les files TOTS i els "
             "totals de la capçalera són fórmules i es calculen soles. Tampoc canvieu el nom de les pestanyes "
             "ni inseriu o esborreu files o columnes."),
    ("seccio", "Què heu d'omplir en la pestanya del vostre mòdul"),
    ("camp", "% RA (columna C)", "Ponderació de cada RA en la qualificació del mòdul. La suma de tots els RA ha de ser 100."),
    ("camp", "COMP (columna D)", "Sota OBJECTIUS i COMPETENCIES, les lletres dels objectius generals i de les competències que treballa el RA."),
    ("camp", "HORES (columna F)", "Hores al centre dedicades a cada criteri d'avaluació. Les hores del mòdul són les hores al centre "
             "més les hores en l'empresa (HORES DUAL): el TOTAL HORES de la capçalera (H. CENTRE + H. DUAL) "
             "es posa en roig mentre no coincidix amb les HORES del mòdul, i en verd quan quadra."),
    ("camp", "% CE (columna G)", "Pes de cada criteri dins del seu RA. La suma dels criteris d'un RA (fila TOTS) ha de ser 100."),
    ("camp", "REQUISIT FE (C/E) (columna H)", "Només en els mòduls que dualitzen. Per a cada criteri que es treballa en l'empresa: "
             "C = compartit (centre i empresa), E = sols empresa. Buit = sols al centre."),
    ("camp", "HORES DUAL (columna I)", "Només en els mòduls que dualitzen. Hores en l'empresa de cada criteri marcat amb C o E. "
             "Tot criteri marcat ha de tindre hores i no hi pot haver hores sense marca."),
    ("camp", "CONTINGUTS (última columna)", "Resum dels continguts associats a cada RA."),
    ("seccio", "Què es comprova automàticament"),
    ("text", "El report de les Programacions avisa si la suma dels % RA no és 100 i si HORES + HORES DUAL no suma "
             "les hores del mòdul (la programació no es dona per verificada). Per als mòduls que dualitzen, "
             "si cap criteri té C/E, si les hores dual són 0 o si hi ha criteris marcats sense hores (o hores sense "
             "marca), el mòdul consta com a pendent i la coordinació de Formació en Empresa en rep l'avís."),
    ("text", "Els mòduls que no dualitzen (Digitalització, Sostenibilitat, IPO, Projecte intermodular, les "
             "optatives i els del curs d'especialització) no tenen les columnes REQUISIT FE ni HORES DUAL."),
]


def escriu_instruccions(wb, titol):
    """Primera pestanya del llibre: com s'usa i què ha d'omplir el docent."""
    ws = wb.create_sheet(title=HOJA_INSTRUCCIONS, index=0)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 100
    r = 2
    for entrada in INSTRUCCIONS:
        tipus = entrada[0]
        if tipus == "titol":
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
            c = ws.cell(row=r, column=2, value=entrada[1].format(titol=titol))
            c.font = _font(bold=True, blanc=True, size=MIDA_BANDA1 - 4)
            c.fill = FOSC
            c.alignment = ESQUERRA
            ws.cell(row=r, column=3).fill = FOSC
            ws.row_dimensions[r].height = 32
            r += 2
            continue
        if tipus == "seccio":
            r += 1
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
            c = ws.cell(row=r, column=2, value=entrada[1])
            c.font = Font(name=LLETRA, size=MIDA_CAPCALERA, bold=True, color=COLOR_FOSC)
            for col in (2, 3):
                ws.cell(row=r, column=col).fill = CLAR
        elif tipus == "text":
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
            c = ws.cell(row=r, column=2, value=entrada[1])
            c.font = _font(size=11)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r].height = 15 * (len(entrada[1]) // 115 + 1)
        else:  # camp
            b = ws.cell(row=r, column=2, value=entrada[1])
            b.font = _font(bold=True, size=11)
            b.alignment = Alignment(wrap_text=True, vertical="top")
            c = ws.cell(row=r, column=3, value=entrada[2])
            c.font = _font(size=11)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r].height = 15 * (len(entrada[2]) // 90 + 1)
        r += 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True  # en imprimir, una pàgina d'ample
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.protection.sheet = True
    contrasenya = os.environ.get("EXCEL_PROTECCIO_PASSWORD")
    if contrasenya:
        ws.protection.password = contrasenya
    wb.active = 0
    return ws
