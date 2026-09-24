# Estils compartits del llibre Excel de PD (libro_{CICLE}.xlsx i
# libro_optatives.xlsx). Únic lloc on viuen colors, lletres i vores: abans
# json2excel.py i json2optatives.py duplicaven trames (darkTrellis/gray125)
# que al Quadre Resum del PDF es veien com un gris brut i poc llegible.
#
# escriu_capcalera() escriu la capçalera (files 1-5) i aplica_estils() s'aplica
# com a passada final sobre la fulla ja construïda, identificant cada tipus de
# fila de la taula pel seu contingut ("TOTS", OBJECTIUS/COMPETENCIES).

from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

LLETRA = "Liberation Sans"
MIDA = 10
MIDA_CAPCALERA = 12       # capçaleres de columna i etiquetes del mòdul
MIDA_MODUL = 15           # codi, nom i hores del mòdul

COLOR_FOSC = "1F3A5F"      # capçalera del mòdul i totals
COLOR_MIG = "2F5597"       # capçaleres de columna
COLOR_CLAR = "DCE6F1"      # files "TOTS" i etiquetes OBJECTIUS/COMPETENCIES
COLOR_VORA = "8EA9C1"

FILA_CAPCALERA = 8         # fila de "RESULTAT D'APRENENTATGE", "% RA", ...
COL_INI, COL_FI = 2, 10    # B..J
COL_COMP = "D"
COLS_NUMERIQUES = range(6, 10)  # HORES, % CE, REQUISIT FE, HORES DUAL (F..I)
CENTRAT = Alignment(horizontal="center", vertical="center")
AMPLE_COMP = 16
# Les 4 columnes numèriques porten la capçalera girada 90° per a poder ser
# estretes; les files 8-9 (capçalera fusionada) han de tindre alçada per al text.
AMPLE_NUMERIQUES = 7
# Amplàries de criteris (E) i continguts (J): el Quadre Resum del PDF
# inclou B..J i LibreOffice l'ajusta a l'ample de pàgina, així que
# l'amplària total fixa l'escala (i la mida del text) al PDF.
COL_CE = "E"
AMPLE_CE = 117
COL_CONTINGUTS = "J"
AMPLE_CONTINGUTS = 23      # continguts resumits
ALT_CAPCALERA = 30         # punts per fila (x2); el text girat fa 2 línies
GIRAT = Alignment(horizontal="center", vertical="center", text_rotation=90, wrap_text=True)
# Capçalera de la fulla (files 1-5), escrita per escriu_capcalera() i comuna
# a json2excel.py i json2optatives.py:
#   Banda 1 (files 1-2): MÒDUL (B:E) | CODI (F:I) | HORES (J)
#   Banda 2 (files 4-5): OBJECTIUS GENERALS (B:D) | COMPETÈNCIES (E:F) |
#                        TOTAL H. DUAL (G:I) | TOTAL HORES (J)
# Cada bloc: etiqueta a la primera fila i valor a la segona. Cap codi llig
# estes cel·les; la taula comença a FILA_CAPCALERA (no canvia).
FILES_BANDA1 = (1, 2)
FILES_BANDA2 = (4, 5)
BANDA1 = (("MÒDUL", 2, 5, "nom"), ("CODI", 6, 9, "codi"), ("HORES", 10, 10, "hores"))
BANDA2 = (("OBJECTIUS GENERALS", 2, 4, "objectius"), ("COMPETÈNCIES", 5, 6, "competencies"),
          ("TOTAL H. DUAL", 7, 9, "total_dual"), ("TOTAL HORES", 10, 10, "total"))
# Les fórmules sumen les columnes HORES (F) i HORES DUAL (I); /2 perquè cada
# RA també té la fila "TOTS" amb la suma dels seus CE.
FORMULA_TOTAL = "=SUM(F8:F200)/2"
FORMULA_TOTAL_DUAL = "=SUM(I8:I200)/2"
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


def _font(bold=False, blanc=False, size=MIDA):
    return Font(name=LLETRA, size=size, bold=bold, color="FFFFFF" if blanc else "000000")


def escriu_capcalera(ws, codi, modul):
    """Escriu (i fusiona) les dues bandes de la capçalera de la fulla."""
    valors = {
        "nom": modul.nombre,
        "codi": codi,
        "hores": modul.horas,
        "objectius": ", ".join(str(x) for x in (modul.get("ObjetivosGenerales") or [])),
        "competencies": ", ".join(str(x) for x in (modul.get("CompetenciasTitulo") or [])),
        "total": FORMULA_TOTAL,
        "total_dual": FORMULA_TOTAL_DUAL,
    }
    for (fila_etiqueta, fila_valor), blocs in ((FILES_BANDA1, BANDA1), (FILES_BANDA2, BANDA2)):
        for etiqueta, c0, c1, clau in blocs:
            if c1 > c0:
                ws.merge_cells(start_row=fila_etiqueta, start_column=c0, end_row=fila_etiqueta, end_column=c1)
                ws.merge_cells(start_row=fila_valor, start_column=c0, end_row=fila_valor, end_column=c1)
            ws.cell(row=fila_etiqueta, column=c0).value = etiqueta
            ws.cell(row=fila_valor, column=c0).value = valors[clau]


def _estil_bloc(ws, fila, c0, c1, fill, font, alignment, border=None):
    for col in range(c0, c1 + 1):
        c = ws.cell(row=fila, column=col)
        c.fill = fill
        c.font = font
        c.alignment = alignment
        if border:
            c.border = border


def aplica_estils(ws):
    ultima = ws.max_row

    # Fons blanc i lletra uniforme a tota la taula
    for row in ws.iter_rows(min_row=1, max_row=ultima, min_col=COL_INI, max_col=COL_FI):
        for c in row:
            c.fill = BLANC
            c.font = _font()

    # Banda 1: identificació del mòdul (etiqueta menuda, valor gran)
    fe, fv = FILES_BANDA1
    for _etiqueta, c0, c1, clau in BANDA1:
        al = ESQUERRA if clau == "nom" else CENTRAT  # etiqueta alineada amb el seu valor
        _estil_bloc(ws, fe, c0, c1, MIG, _font(bold=True, blanc=True, size=9), al)
        _estil_bloc(ws, fv, c0, c1, FOSC, _font(bold=True, blanc=True, size=MIDA_MODUL), al)
    ws.row_dimensions[fe].height = 16
    ws.row_dimensions[fv].height = 28

    # Banda 2: objectius, competències i totals
    fe, fv = FILES_BANDA2
    for _etiqueta, c0, c1, clau in BANDA2:
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
        for col in range(COL_INI, COL_FI + 1):
            c = ws.cell(row=r, column=col)
            c.fill = MIG
            c.font = _font(bold=True, blanc=True, size=MIDA_CAPCALERA)
            c.border = VORA
            if col in COLS_NUMERIQUES:
                c.alignment = GIRAT
        ws.row_dimensions[r].height = ALT_CAPCALERA

    # Cos: vores a totes les cel·les, vora grossa a l'inici de cada RA
    # (fila "TOTS"), i ressalt de "TOTS" i de les etiquetes de competències
    for r in range(FILA_CAPCALERA + 2, ultima + 1):
        inici_ra = ws.cell(row=r, column=5).value == "TOTS"
        for col in range(COL_INI, COL_FI + 1):
            c = ws.cell(row=r, column=col)
            c.border = VORA_INICI_RA if inici_ra else VORA
            if inici_ra and 5 <= col < COL_FI:  # CONTINGUTS (J) queda en blanc: l'omple el docent
                c.fill = CLAR
                c.font = _font(bold=True)
        for col in COLS_NUMERIQUES:
            ws.cell(row=r, column=col).alignment = CENTRAT
        comp = ws.cell(row=r, column=4)
        if comp.value in ("OBJECTIUS", "COMPETENCIES"):
            comp.fill = CLAR
            comp.font = _font(bold=True, size=9)
        ra = ws.cell(row=r, column=2)
        if isinstance(ra.value, str) and ra.value.startswith("RA"):
            ra.font = _font(bold=True)

    ws.column_dimensions[COL_COMP].width = AMPLE_COMP
    ws.column_dimensions[COL_CE].width = AMPLE_CE
    ws.column_dimensions[COL_CONTINGUTS].width = AMPLE_CONTINGUTS
    for col in COLS_NUMERIQUES:
        ws.column_dimensions[chr(ord("A") + col - 1)].width = AMPLE_NUMERIQUES
