# Estils compartits del llibre Excel de PD (libro_{CICLE}.xlsx i
# libro_optatives.xlsx). Únic lloc on viuen colors, lletres i vores: abans
# json2excel.py i json2optatives.py duplicaven trames (darkTrellis/gray125)
# que al Quadre Resum del PDF es veien com un gris brut i poc llegible.
#
# S'aplica com a passada final sobre la fulla ja construïda, identificant
# cada tipus de fila pel seu contingut (capçaleres, "TOTS", OBJECTIUS/
# COMPETENCIES), perquè no depenga de les posicions de cada generador.

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
AMPLE_CE = 95
COL_CONTINGUTS = "J"
AMPLE_CONTINGUTS = 45
ALT_CAPCALERA = 30         # punts per fila (x2); el text girat fa 2 línies
GIRAT = Alignment(horizontal="center", vertical="center", text_rotation=90, wrap_text=True)
# Banda de totals (fila 5), entre la capçalera del mòdul i la taula, amb cada
# total just damunt de la seua columna: etiqueta E5 -> valor F5 (HORES) i
# etiqueta G5:H5 -> valor I5 (HORES DUAL).
FILA_TOTALS = 5
TOTALS = ((5, 6), (7, 9))  # (columna etiqueta, columna valor)
FILES_BUIDES = (6, 7)      # separadors entre els totals i la taula
# Columna J (fora del Quadre Resum del PDF, però l'edita el docent):
# OBJECTIUS / COMPETENCIES amb les seues llistes, a les files 2-5. Per això
# la fila 4 no pot ser un separador baix.
COL_LLISTES = 10
FILES_LLISTES = ((2, 3), (4, 5))  # (fila etiqueta, fila valor)
ALT_LLISTA = 30
VALOR_LLISTA = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
DRETA = Alignment(horizontal="right", vertical="center", wrap_text=True, indent=1)

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


def aplica_estils(ws):
    ultima = ws.max_row

    # Fons blanc i lletra uniforme a tota la taula
    for row in ws.iter_rows(min_row=1, max_row=ultima, min_col=COL_INI, max_col=COL_FI):
        for c in row:
            c.fill = BLANC
            c.font = _font()

    # Capçalera del mòdul, a tota l'amplària: etiquetes (B1:B3), valors (C1:I3)
    for r in range(1, 4):
        ws.cell(row=r, column=2).fill = MIG
        ws.cell(row=r, column=2).font = _font(bold=True, blanc=True, size=MIDA_CAPCALERA)
        for col in range(3, COL_FI):
            ws.cell(row=r, column=col).fill = FOSC
            ws.cell(row=r, column=col).font = _font(bold=True, blanc=True, size=MIDA_MODUL)

    # Banda de totals
    for col_etiqueta, col_valor in TOTALS:
        etiqueta = ws.cell(row=FILA_TOTALS, column=col_etiqueta)
        etiqueta.font = Font(name=LLETRA, size=MIDA_CAPCALERA, bold=True, color=COLOR_FOSC)
        etiqueta.alignment = DRETA
        valor = ws.cell(row=FILA_TOTALS, column=col_valor)
        valor.fill = CLAR
        valor.font = _font(bold=True, size=MIDA_MODUL)
        valor.border = VORA
        valor.alignment = CENTRAT
    ws.row_dimensions[FILA_TOTALS].height = 26

    # Llistes d'objectius i competències (columna J)
    for fila_etiqueta, fila_valor in FILES_LLISTES:
        etiqueta = ws.cell(row=fila_etiqueta, column=COL_LLISTES)
        etiqueta.fill = CLAR
        etiqueta.font = Font(name=LLETRA, size=MIDA, bold=True, color=COLOR_FOSC)
        etiqueta.border = VORA
        etiqueta.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        valor = ws.cell(row=fila_valor, column=COL_LLISTES)
        valor.font = _font(size=MIDA_CAPCALERA)
        valor.border = VORA
        valor.alignment = VALOR_LLISTA
        ws.row_dimensions[fila_valor].height = max(ws.row_dimensions[fila_valor].height or 0, ALT_LLISTA)
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
            if inici_ra and 5 <= col < COL_LLISTES:  # CONTINGUTS (J) queda en blanc: l'omple el docent
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
