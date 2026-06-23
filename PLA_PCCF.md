# PLA: PCCF al model de memòries

Adaptar el pipeline de Programacions Didàctiques i PCCF al mateix model
que les memòries del departament: generar → emplenar → reportar → compilar.

## Estructura de directoris

```
plantilles_{FAMILIA}_{CICLO}/          ← persistent, mai esborrat sencer
├── PD_{CICLO}_{CODI}_{NOM}_BORRADOR.md   ← generat Jinja2 (si no existia)
├── PD_{CICLO}_{CODI}_{NOM}_OK.md         ← el docent renombra
├── libro_{CICLO}.xlsx                    ← generat (si no existia)
├── PCCF_{NNN}_{CICLO}_*.md              ← auto-generats (sempre actuals)
├── (PCCF_*.md copiats de src/)           ← NO sobreescriuen PD_* / libro_*
```

## Fases del pipeline

### Fase 1 — `generar-plantilles-pccf-{CICLO}`

**Mai sobreescriure el treball del docent.**

| Pas | Què fa | Condició |
|---|---|---|
| 1 | `mkdir -p plantilles_{FAMILIA}_{CICLO}/` | sempre |
| 2 | Copia `src/*` | NO sobreescriu `PD_*.md` ni `libro_*.xlsx` |
| 3 | Copia `src_{FAMILIA}/*` | idem |
| 4 | Copia `src_{FAMILIA}_{CICLO}/*` | idem |
| 5 | Auto-genera `PCCF_030_ContribucioModuls` i `PCCF_033_ImportanciaCompetencies` | SEMPRE |
| 6 | Auto-genera `libro_{CICLO}.xlsx` des de BOE | SOLS si no existeix |
| 7 | Per a cada mòdul: genera `PD_{CICLO}_{CODI}_{NOM}_BORRADOR.md` (Jinja2 + `[###]`) | SOLS si no existeix `PD_{CICLO}_{CODI}_{NOM}_{BORRADOR,OK}.md` |
| 8 | Processa `@@@` includes en MDs nous | Opció A (resolt en gen.) |
| 9 | NO cuadros, NO portades standalone, NO PDFs | — |

### Fase 2 — Treball del docent (offline)

- Obri `PD_*_BORRADOR.md`, substituïx `[###]` per contingut real
- Ompli `libro_{CICLO}.xlsx` (pesos RA, hores CE, FEE...)
- Quan acaba: renombra `_BORRADOR.md` → `_OK.md`

### Fase 3 — `report-pccf-{CICLO}`

| Què comprova | Mecanisme |
|---|---|
| `[###]` pendents en cada PD | regex |
| Fitxers en `_BORRADOR` vs. `_OK` | enumeració |
| Excel: suma pesos RA = 100% | `openpyxl` |
| Excel: hores RA coherents | validacions |
| Genera informe a `PDFS/report_pccf_{FAMILIA}_{CICLO}.txt` | — |

### Fase 4 — `compila-pccf-{CICLO}` (script `compilar_pccf.py`)

1. Executa report + mostra a l'usuari
2. Demana confirmació (s/N)
3. Crea `temp/` (esborrable)
4. Copia `src/` + `src_{FAMILIA}/` + `src_{FAMILIA}_{CICLO}/` → `temp/`
5. Copia `plantilles_*/PD_*.md` → `temp/`
6. Portada per al combinat
7. Per a cada mòdul OK (i BORRADOR confirmat):
   a. Llig Excel → genera cuadro resumen (excel-to-pdfs + excel-to-plan-formativo)
   b. Construeix PD individual (portada + contingut + `\includepdf`)
   c. pandoc → PDF individual, pdfunite amb cuadro
8. Genera `Programaciones_{CENTRO}_{CICLO}.pdf`
9. Genera `PCCF_{CENTRO}_{CICLO}.pdf`
10. Esborra `temp/`

## Ordre d'implementació (tandes)

| Tanda | Què | Fitxers |
|---|---|---|
| **1** | generar-plantilles (no-overwrite + pccf_utils + --generate-only) | `tools/pccf_utils.py`, `tools/json2pccf.py`, `Makefile` |
| **2** | report ampliat (Excel, BORRADOR/OK) | `tools/report_pccf.py`, `tools/pccf_utils.py` |
| **3** | compilar_pccf.py (patró compilar_memories.py) | `tools/compilar_pccf.py` (NOU) |
| **4** | Makefile compila-pccf + proyecto adaptats | `Makefile` |
| **5** | Test complet DAM (genera + report + compila) | — |

## Tests

```sh
# Tanda 1
./contenedor_lanza.sh "make generar-plantilles-pccf-dam"
ls plantilles_INF_DAM/PD_*.md                    # fitxers BORRADOR
ls plantilles_INF_DAM/libro_DAM.xlsx             # Excel
# Segon cop: no sobreescriu
./contenedor_lanza.sh "make generar-plantilles-pccf-dam"

# Tanda 2
./contenedor_lanza.sh "make report-pccf-dam"

# Tanda 3-4
./contenedor_lanza.sh "make compila-pccf-dam"
ls PDFS/PCCF_SENIA_DAM.pdf PDFS/Programaciones_SENIA_DAM.pdf

# Tanda 5
./contenedor_lanza.sh "make proyecto-dam"
```
