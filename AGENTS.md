# AGENTS.md — PCCF

Curricular projects & teaching plans for vocational training at IES La Sénia. Build outputs: PDFs (Pandoc + XeLaTeX) and spreadsheets (openpyxl).

## Optatives conventions

- **Source of truth**: `optatives/optatives.json` — shared across all cycles.
- **4 modules**: MOPCOMPROF, MOPANGPROF, INP (with `codis_alternatius` for CVOPS190), IPR.
- **OG/CPSS are empty arrays**: shared optatives cannot reference cycle-specific objectives/competencies.
- **`grups` field**: each module lists which cycles offer it (`{cicle, curs, familia}`).
- **PD generation**: Jinja2 template `templates/PCCF_PD_Plantilla_MODULO_OPTATIVA.md` skips OG/CPSS sections when empty.
- **State tracking**: same as PCCF (`_BORRADOR.md` / `_OK.md`), shared across all cycles.
- **Excel**: `optatives/libro_optatives.xlsx` (shared, one sheet per module).
- **Pipeline**: `make generar-plantilles-optatives` → `make report-optatives` → `make compila-pccf-{CICLO}` copies matching optatives PDs automatically.
- **Integration**: `tools/copy_optatives_pd.py` filters by `grups` field and copies PDs to `.compila/` during per-cycle compilation.

## Build commands

```sh
make proyecto-smx          # single cycle (smx, dam, daw, asir, ceiabd, fpbiio, apd, ei, is)
make CENTRO_EDUCATIVO=XYZ proyecto-dam  # override default school (SENIA)
make todos                 # all cycles
make todos-inf / todos-sco # family subset
make validate-json         # validate all boe_{INF,SCO}/*.json
make report                # missing-fields report → PDFS/reporte_analisis.txt

# PCCF two-phase pipeline (new):
make generar-plantilles-pccf-dam   # Phase 1: gen templates (persistent, never overwrites teacher work)
make report-pccf-dam               # Report: BORRADOR/OK status + [###] + Excel coherence
make compila-pccf-dam              # Phase 2: compile PDFs from plantilles templates
make proyecto-dam                  # backward compat: generate + compile in one step
make report-tots-pccf              # report for all cycles

# Memoria pipeline (existing):
make generar-plantilles-memoria    # generate FP dept memoria templates → memories_FP/{FAMILIA}/
make report-memories               # report only (no PDF)
make compila-memories              # report + confirm + compile ALL (OK + BORRADOR) → PDF
make compilar-memories             # OLD: compile OK only, prompt for BORRADOR
make memories                      # generar-plantilles-memoria + compila-memories
make FAMILIA=SCO memories          # family override (default INF)
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories  # ESO/BAT single dept
make genera-tots-esobat            # ESO/BAT all 17 departments (generate)
make report-tots-esobat            # ESO/BAT all departments (report)
make compila-tots-esobat           # ESO/BAT all departments (compile)
make genera-tots-fp                # FP all families INF+SCO (generate)
make report-tots-fp                # FP all families (report)
make compila-tots-fp               # FP all families (compile)
make generar-plantilles-optatives  # Phase 1b: gen shared optatives Excel + PDs → optatives/plantilles/
make report-optatives             # report optatives BORRADOR/OK status + [###]
make generar-plantilles-optatives  # Phase 1b: gen shared optatives Excel + PDs → optatives/plantilles/
make report-optatives             # report optatives BORRADOR/OK status + [###]
make clean                 # rm -rf PDFS/ temp/ plantilles_*/
make dependences           # apt install pandoc, texlive-*, libreoffice, python deps
```

## ESO/BAT memories

Generate and compile ESO/BAT department memories using `BASE_DIR=memoriaESOBAT`.

17 departments configured: ANGLES, BIOLOGIA_GEOLOGIA, DIBUIX, ECONOMIA, EDUCACIO_FISICA, FILOSOFIA, FISICA_QUIMICA, FRANCES, GEOGRAFIA_HISTORIA, INFORMATICA, LLATI, LLENGUA_CASTELLANA, LLENGUA_VALENCIANA, MATEMATIQUES, MUSICA, RELIGIO, TECNOLOGIA.

```sh
# Via make (same interface as FP, just add BASE_DIR=memoriaESOBAT)
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES generar-plantilles-memoria
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES compila-memories
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories

# All 17 departments at once
make genera-tots-esobat
make report-tots-esobat
make compila-tots-esobat
```

Via Docker wrapper:

```sh
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES compila-memories"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT genera-tots-esobat"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT compila-tots-esobat"
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
| `plantilles_{FAMILIA}_{CICLO}/` | Persistent teacher workspace (gitignored); contains PD_*.md + libro_*.xlsx |
| `optatives/` | Shared optative modules JSON + plantilles/ (PDs) + libro_optatives.xlsx |
| `memoriaFP/` | FP department configs + templates (memories_{FAMILIA}.json, plantilla_memoria.md, portada) |
| `memoriaESOBAT/` | ESO/BAT department configs + templates (same structure as memoriaFP) |
| `memories_FP/{FAMILIA}/` | Per-module/per-group FP memoria markdown files (gitignored via `memories_*/`) |
| `memories_ESOBAT/{FAMILIA}/` | Per-course/per-group ESO/BAT memoria markdown files (gitignored) |
| `PDFS/` | All generated outputs (gitignored) |
| `tools/` | Python scripts for build pipeline |
| `contenedor_lanza.sh` | Docker wrapper (recommended to avoid dep issues) |

## Build pipeline (what `make proyecto-{ciclo}` does)

1. `validate-json` — validates JSONs first
2. Phase 1: `generar-plantilles-pccf-{CICLO}`:
   - Copies `PD_*.md` from `src/` + `src_{FAMILIA}/` + `src_{FAMILIA}_{CICLO}/` → `plantilles_{FAMILIA}_{CICLO}/` (never overwrites existing)
   - `json2excel.py {CICLO} {FAMILIA} --outdir $(PLANTILLES_DIR)` — generates `libro_{CICLO}.xlsx` directly in plantilles
   - `json2pccf.py {CICLO} {FAMILIA} --generate-only` — generates `PD_*_BORRADOR.md` from Jinja2 templates (only if neither `_BORRADOR` nor `_OK` exist)
   - **Plantilles conté només PDs + Excel** (no PCCF framework files)
 3. Phase 2: `compila-pccf-{CICLO}`:
    - `json2pccf.py --generate-competences` — genera `PCCF_030/033` a `.compila/` dins plantilles
    - `copy_optatives_pd.py` — copia PDs optatives que corresponguen al cicle des de `optatives/plantilles/`
    - `pandoc` des de `src/`, `src_{FAMILIA}/`, `src_{FAMILIA}_{CICLO}/` + `.compila/` → `PCCF_{CENTRO}_{CICLO}.pdf`
    - `pandoc` des de plantilles → `Programaciones_{CENTRO}_{CICLO}.pdf`
    - `rm -rf .compila/`
    - `shell-progs-didacticas-standalone.sh` — per-module PDFs a `PDFS/PDs_{CICLO}/`

## Report pipeline

`make report-pccf-{CICLO}` → `tools/report_pccf.py`:
- Lists PD files: BORRADOR (pending) vs OK (completed)
- Detects `[###]` placeholders in all markdown files
- Validates Excel: RA weight sum = 100% per sheet

## Excel workflow

1. Auto-generated from JSON → `plantilles_{FAMILIA}_{CICLO}/libro_{CICLO}.xlsx`
2. Teachers fill: RA weights (col C, must sum to 100%), CE hours (col F), FEE flags (col H), FEE hours (col I), contents (col J)
3. `python3 tools/preparar_excel.py -c CICLO -f FAMILIA` — renames sheets to short codes, saves to `excels_{FAMILIA}/libro_{CICLO}.xlsx`

## Key conventions

- **File naming**: `{TYPE}_{NNN}_{CONTEXT}_Description.md` (TYPE=PCCF|PD, NNN=3-digit order, CONTEXT=CICLO or FAMILIA). Order in `ls` determines PDF page order.
- **Include syntax**: `@@@filename.md` in markdown pulls in content from another file at compile time.
- **`ImportanciaCompetencias`**: JSON dict with values 1-3 (stars). Missing = 2 stars default.
- **Module code mapping**: `tools/pccf_utils.py::get_hoja_label()` maps full module names to short codes. If a new Excel sheet name doesn't match, add it there. Use "1"/"2" suffix for modules with I/II to avoid prefix collisions (e.g. "Ciències aplicades 1" not "Ciències aplicades I").
- **PD override**: Place a file with the same name in `src_{FAMILIA}_{CICLO}/` to override auto-generated PD markdown.
- **State tracking**: `_BORRADOR.md` = pending teacher review. Teacher renames to `_OK.md` when completed.
- **Instructions block**: Automatically stripped from the compiled PDF (regex removes `> **Instruccions...` blocks).

## Memoria conventions

- **Config**: Edit `memoriaFP/memories_{FAMILIA}.json` each academic year (curs, groups per cycle/course, modules). For ESO/BAT, edit `memoriaESOBAT/memories_{DEPART}.json`.
- **Group naming**: Single letter (A, B) → concatenated to cycle code (`SMXA`). Multi-letter (SEMI) → underscore-separated (`DAM_SEMI`). Empty → no group suffix (`DAM`).
- **Per-materia groups (ESO/BAT)**: Each subject in the config can have its own `grups` array. If missing, inherits from the course level. Example: `{"codi": "COMPCOM", "nom": "Competència Comunicativa", "grups": ["G1"]}`.
- **Special course types (ESO/BAT)**: PDC and APLI courses are automatically detected and treated as ESO etapa for filename parsing.
- **17 ESO/BAT departments**: Config files in `memoriaESOBAT/memories_{DEPART}.json` for ANGLES, BIOLOGIA_GEOLOGIA, DIBUIX, ECONOMIA, EDUCACIO_FISICA, FILOSOFIA, FISICA_QUIMICA, FRANCES, GEOGRAFIA_HISTORIA, INFORMATICA, LLATI, LLENGUA_CASTELLANA, LLENGUA_VALENCIANA, MATEMATIQUES, MUSICA, RELIGIO, TECNOLOGIA.
- **State tracking** (same as PCCF): `_BORRADOR.md` = pending teacher review. Teacher renames to `_OK.md` when completed.
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

For ESO/BAT department memories:
```sh
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES compila-memories"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT genera-tots-esobat"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT compila-tots-esobat"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM genera-tots-fp"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM compila-tots-fp"
```

Container image has all deps pre-installed (Pandoc, TeX Live, LibreOffice, Python libs).

## Language

## Testing

**Important**: Always test via Docker to avoid LibreOffice/LaTeX dependency issues in the development environment:
```sh
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM proyecto-dam"
# or for the default school (SENIA):
./contenedor_lanza.sh "make proyecto-dam"
```
Calling `make` or Python scripts directly from the host will likely fail due to missing/broken LibreOffice.

All content is in Valencian/Catalan. JSON keys are in Spanish (from BOE), values in Valencian.
