# AGENTS.md — PCCF

Curricular projects & teaching plans for vocational training at IES La Sénia. Build outputs: PDFs (Pandoc + XeLaTeX) and spreadsheets (openpyxl).

## Build commands

```sh
make proyecto-smx          # single cycle (smx, dam, daw, asir, ceiabd, fpbiio, apd, ei, is)
make CENTRO_EDUCATIVO=XYZ proyecto-dam  # override default school (SENIA)
make todos                 # all cycles
make todos-inf / todos-sco # family subset
make validate-json         # validate all boe_{INF,SCO}/*.json
make report                # missing-fields report → PDFS/reporte_analisis.txt
make generar-plantilles-memoria  # generate dept memoria templates → memories_{FAMILIA}/ (also: genera-memories)
make report-memories             # report only (no PDF)
make compila-memories            # report + confirm + compile ALL (OK + BORRADOR) → PDF
make compilar-memories           # OLD: compile OK only, prompt for BORRADOR
make memories                    # generar-plantilles-memoria + compila-memories
make FAMILIA=SCO memories        # family override (default INF)
make clean                 # rm -rf PDFS/ temp/
make dependences           # apt install pandoc, texlive-*, libreoffice, python deps
```

## CI (`.github/workflows/makefile.yml`)

Only runs on `main` when commit message contains `[build]`. Generates only INF cycles (SMX, DAW, DAM, ASIR). Copies PDFs to `releases/{date}/` and commits them.

## Repo layout

| Path | Purpose |
|---|---|
| `boe_{INF,SCO}/rd-{ciclo}.json` | Curriculum data from BOE (single source of truth) |
| `src/` | Base/shared PCCF markdown files |
| `src_{INF,SCO}/` | Family-specific PCCF files |
| `src_{INF,SCO}_{CICLO}/` | Cycle-specific PCCF + PD markdown |
| `templates/` or `templates_{FAMILIA}/` | Jinja2 templates for auto-generated markdown |
| `excels_{INF,SCO}/` | Teacher-edited spreadsheets (after `preparar_excel.py`) |
| `PDFS/` | All generated outputs (gitignored) |
| `memoria/` | Common templates + config per family (plantilla_memoria.md, portada, memories_{FAMILIA}.json) |
| `memories_{FAMILIA}/` | Per-module/per-group memoria markdown files, one dir per family (gitignored) |
| `tools/` | Python scripts for build pipeline |
| `contenedor_lanza.sh` | Docker wrapper (recommended to avoid dep issues) |

## Build pipeline (what `make proyecto-{ciclo}` does)

1. `validate-json` — validates JSONs first
2. Copies `src/` → `temp/`, overlays `src_{FAMILIA}/`, overlays `src_{FAMILIA}_{CICLO}/`
3. `json2excel.py {CICLO} {FAMILIA}` — generates `PDFS/libro_autogenerado_{CICLO}.xlsx`
4. `json2pccf.py {CICLO} {FAMILIA}` — generates PCCF markdown files from Jinja2 templates
5. `pandoc` → `PCCF_{CENTRO}_{CICLO}.pdf` and `Programaciones_{CENTRO}_{CICLO}.pdf`
6. `shell-progs-didacticas-standalone.sh` — per-module PDFs to `PDFS/PDs_{CICLO}/`

## Excel workflow

1. Auto-generated from JSON → `PDFS/libro_autogenerado_{CICLO}.xlsx`
2. Teachers fill: RA weights (col C, must sum to 100%), CE hours (col F), FEE flags (col H), FEE hours (col I), contents (col J)
3. `python3 tools/preparar_excel.py -c CICLO -f FAMILIA` — renames sheets to short codes, saves to `excels_{FAMILIA}/libro_{CICLO}.xlsx`

## Key conventions

- **File naming**: `{TYPE}_{NNN}_{CONTEXT}_Description.md` (TYPE=PCCF|PD, NNN=3-digit order, CONTEXT=CICLO or FAMILIA). Order in `ls` determines PDF page order.
- **Include syntax**: `@@@filename.md` in markdown pulls in content from another file at compile time.
- **`ImportanciaCompetencias`**: JSON dict with values 1-3 (stars). Missing = 2 stars default.
- **Module code mapping**: `tools/pccf_utils.py::get_hoja_label()` maps full module names to short codes. If a new Excel sheet name doesn't match, add it there. Use "1"/"2" suffix for modules with I/II to avoid prefix collisions (e.g. "Ciències aplicades 1" not "Ciències aplicades I").
- **PD override**: Place a file with the same name in `src_{FAMILIA}_{CICLO}/` to override auto-generated PD markdown.

## Memoria conventions

- **Config**: Edit `memoria/memories_{FAMILIA}.json` each academic year (curs, groups per cycle/course, modules).
- **Group naming**: Single letter (A, B) → concatenated to cycle code (`SMXA`). Multi-letter (SEMI) → underscore-separated (`DAM_SEMI`). Empty → no group suffix (`DAM`).
- **State tracking**: `_BORRADOR.md` = pending teacher review. Teacher renames to `_OK.md` when completed.
- **Instructions block**: Automatically stripped from the compiled PDF (regex removes `> **Instruccions...` blocks).
- **Module-only scope**: Memorias are per-department; only modules assigned to the dept should be in the config JSON (e.g. no IPO, Anglés, Comunicació professional unless they belong to the dept).
- **CEIABD**: Specialization course → no course number in filename (curs = `""` in config).
- **Cycle code list**: `tools/memories_utils.py::CICLES_CONEGUTS` must include any new cycle added to the config.
- **Report only**: `make report-memories` generates the same report as `compilar-memories` without compiling the PDF.
- **Compilation confirmation**: `compila-memories` shows report, then asks for confirmation before compiling ALL files (OK + BORRADOR).

## Docker

```sh
./contenedor_lanza.sh                          # interactive bash
./contenedor_lanza.sh "make proyecto-dam"       # run command
./contenedor_lanza.sh -d                       # detach
```

**IESEPM**: to override the default school, pass the var after `make`:
```sh
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM proyecto-smx"   # single cycle
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM todos"           # all cycles
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM memories"        # generate + report + compile dept memorias
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM FAMILIA=SCO memories"  # SCO family override
```

Container image has all deps pre-installed (Pandoc, TeX Live, LibreOffice, Python libs).

## Language

All content is in Valencian/Catalan. JSON keys are in Spanish (from BOE), values in Valencian.
