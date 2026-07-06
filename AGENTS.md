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
make report-pccf-dam               # Report: BORRADOR/OK status + [###] + Excel coherence + verified (draft watermark)
make compila-pccf-dam              # Phase 2: compile PDFs from plantilles templates
make proyecto-dam                  # backward compat: generate + compile in one step
make report-tots-pccf              # report for all cycles
make PLANTILLES_ROOT=/path proyecto-dam  # plantilles_* under an alternate root (OneDrive sync, see below)

# Memoria pipeline (existing):
make generar-plantilles-memoria    # generate FP dept memoria templates → memories_FP/{FAMILIA}/
make report-memories               # report only (no PDF)
make compila-memories              # report + compile ALL (OK + BORRADOR) → PDF
make compilar-memories             # OLD: compile OK only, prompt for BORRADOR
make memories                      # generar-plantilles-memoria + compila-memories
make FAMILIA=SCO memories          # family override (default INF)
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories  # ESO/BAT single dept
make genera-tots-esobat            # ESO/BAT all 17 departments (generate)
make report-tots-esobat            # ESO/BAT all departments (report)
make compila-tots-esobat           # ESO/BAT all departments (compile)
make genera-tots-fp                # FP all families ANG+FOL+INF+SCO (generate)
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
| `tools/report_legend.txt` | Legend table appended to memoria reports |
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

### PCCF reports (`make report-pccf-{CICLO}` → `tools/report_pccf.py`):
- Lists PD files: BORRADOR (pending) vs OK (completed)
- Detects `[###]` placeholders in all markdown files
- Validates Excel: RA weight sum = 100% per sheet

### Memoria reports (`make report-memories`, `make compila-memories` → `tools/report_memories.py`, `tools/compilar_memories.py`):
- Output directory: `PDFS/0_YYYYMMDD_hhmm_report_memories_{ESOBAT|FP}/`
- Detects: `[FALTA]`, `[BORRADOR]`, `[DUPLICAT]`, `[INCOMPLET]`, `[NO IMPARTIT]`, `[CONFLICTE]` (placeholders, malformed checkboxes, stats inconsistencies)
- Detects malformed checkboxes: `[ x ]`, `[x ]`, `[ x]` reported as `[CHECKBOX_FORMAT]`
- Detects stats inconsistencies: aprovats+suspensos > avaluats, total > final, etc.
- **Automatic cleanup**: `[]` → `[ ]` (fix empty checkbox), strips brackets from non-checkbox content (`[24]`→`24`, `[CAP]`→`CAP`). Preserves `[###]` and `[...]` for report detection. Runs on OK files during report generation.
- Legend appended at end of each report (source: `tools/report_legend.txt`)
- Report directory suffixed with `_ESOBAT` or `_FP` depending on config type

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
- **`_NOIMPARTIT.md` state**: third file state (besides `_OK`/`_BORRADOR`) for a module/subject that ends up with no enrolled students and is therefore never taught. The teacher/head of department renames the `_BORRADOR.md` to `_NOIMPARTIT.md` without filling it in. `tools/memories_utils.py::build_report_lines()` treats these as resolved — excluded from `missing`, listed in their own report section `[NO IMPARTIT]` — so they do **not** trigger the ESBORRANY watermark (see below). A module with both an `_NOIMPARTIT.md` and an `_OK`/`_BORRADOR` file is reported as `[CONFLICTE]` (contradictory state, must be resolved manually). If neither state nor `_NOIMPARTIT` exists, behavior is unchanged: reported as `[FALTA]` and still triggers the watermark.
- **Instructions block**: Automatically stripped from the compiled PDF (regex removes `> **Instruccions...` blocks).
- **Module-only scope**: Memorias are per-department; only modules assigned to the dept should be in the config JSON (e.g. no IPO, Anglés, Comunicació professional unless they belong to the dept).
- **CEIABD**: Specialization course → no course number in filename (curs = `""` in config).
- **Cycle code list**: `tools/memories_utils.py::CICLES_CONEGUTS` must include any new cycle added to the config.
- **Report only**: `make report-memories` generates the same report as `compilar-memories` without compiling the PDF.
- **Compilation confirmation**: `compila-memories` shows report and compiles ALL (OK + BORRADOR) without prompting.
- **Checkbox format**: Only `[x]` (or `[X]`) is valid. Variants like `[ x ]`, `[x ]`, `[ x]` are detected as `[CHECKBOX_FORMAT]` in reports.
- **Empty checkboxes**: `[ ]` are optional and NOT reported.
- **Summary bar chart (landscape)**: Generated at end of PDF via `compilar_memories.py`. Uses `width=1.0\linewidth` + `\newgeometry{top=10mm, bottom=10mm}` before landscape to fill full landscape page width (29.7cm), centered vertically with `\vspace*{\fill}`. Figsize: `max(10, num_bars*1.2), 5` (wider default to prevent tall charts with few modules). Uses absolute path in `\includegraphics{}` to avoid lualatex file-not-found issues. Works for both FP and ESO/BAT. When all stats contain `[###]`, shows "No hi ha dades completes" label.
- **Pie chart**: matplotlib charts filter out zero-value categories (e.g. 0 suspensos → no wedge shown). Absents/no avaluables are shown as a pie wedge when present; the percentage shown in the table includes absents in the total.
- **Paragraph spacing**: `####` headings in compiled PDFs now have proper line breaks via `\titlespacing` LaTeX patch.
- **Report legend**: Appended from `tools/report_legend.txt` (external file, easy to maintain).
- **Report dir naming**: `PDFS/0_YYYYMMDD_hhmm_report_memories_{ESOBAT|FP}/` (includes timestamp + type suffix).

## Sincronització OneDrive de memòries + desplegament autònom (Docker/Portainer)

Sistema per a eliminar la baixada/pujada manual de fitxers OneDrive/SharePoint del coordinador. En compte de Graph API propi o Power Automate (bloquejats en este tenant EDU centralitzat sense rol d'Entra ID disponible), s'usa el client de sincronització OneDrive per a Linux (`abraunegg/onedrive`, paquet `onedrive` d'apt), que ja s'autentica amb una app pre-consentida sense necessitar cap acció d'administrador.

**Mecanisme**:
- Un perfil `onedrive` separat (propi `--confdir`) sincronitza només `General/Memòries ESO-BAT` i `General/Memòries FP` del lloc SharePoint compartit del centre (via `sync_list`, no tota la biblioteca).
- `memories_ESOBAT` i `memories_FP` al arrel del repo són **symlinks** (no directoris reals) cap a eixa carpeta sincronitzada — `tools/report_memories.py`/`tools/compilar_memories.py` operen sobre ells sense cap canvi de codi.
- **FP té 4 departaments**: ANG, FOL, INF, SCO (`FAMILIES_FP = ANG FOL INF SCO` al Makefile) — ANG (no ANGLES) per a coincidir amb la convenció de sigles de la resta.

**Poller automàtic** (`tools/local_sync_poller.py`): sondeja cada departament (17 ESOBAT + 4 FP) comparant la data de modificació més recent dels seus `.md` reals contra la de l'últim report ja publicat (`0_report_memories_{TIPUS}/{FAMILIA}_*.txt`). Si detecta un canvi, executa sol `compila-memories` + `publish_memories_output.py` — **sense cap fitxer disparador ni acció manual** del docent/cap de departament (disseny deliberat: es va descartar un disseny amb fitxer "COMPILAR_ARA" perquè calia minimitzar accions manuals al màxim). S'executa en bucle des de `docker-entrypoint.sh`, en paral·lel a `onedrive --monitor` (`wait -n` entre tots dos: si un dels dos processos mor inesperadament, el contenidor sencer es reinicia via `restart: unless-stopped`).

**Publicació de resultats** (`tools/publish_memories_output.py`): després de `compila-memories`, copia el report i el PDF cap a una **única carpeta fixa per tipus** a l'arrel de la carpeta sincronitzada corresponent:
```
General/Memòries {ESO-BAT|FP}/0_report_memories_{ESOBAT|FP}/{FAMILIA}_{timestamp}.txt
General/Memòries {ESO-BAT|FP}/1_esborrany_memories_{ESOBAT|FP}/Memories_{ESOBAT|FP}_{FAMILIA}_{CENTRE}_{CURS}_{timestamp}.pdf
```
Cada publicació esborra automàticament la versió anterior d'eixe mateix departament (mateix nom base, timestamp diferent) — només queda l'última. Ús manual (poc habitual ja, el poller ho fa sol):
```sh
python3 tools/publish_memories_output.py --base-dir memoriaESOBAT --dest "/data/onedrive-memories/General/Memòries ESO-BAT" --centre IESEPM
# --familia OMÉS per a un sol departament; sense --familia publica tots els presents al report
```

**Desplegament autònom a Portainer (des del repositori de GitHub)**:
- `Dockerfile`: afig el paquet `onedrive`; `COPY --chown=1000:1000 . .` + `RUN chown 1000:1000 /home/PCCF` (necessari perquè el contenidor corre com a usuari no-root `1000:1000` — sense el `chown` explícit de la carpeta, `WORKDIR` la deixa de `root` i qualsevol `ln`/escriptura falla amb "Permission denied", encara que `--chown` de `COPY` ja haja corregit el contingut). També fixa la zona horària a nivell de sistema (`ENV TZ=Europe/Madrid` + `tzdata` + `/etc/localtime`, no només la variable d'entorn de docker-compose, que no totes les eines respecten).
- `docker-entrypoint.sh`: crea els symlinks `memories_ESOBAT`/`memories_FP` cap a `$MEMORIES_SYNC_ROOT` (per defecte `/data/onedrive-memories`, un path **net dins del contenidor que no coincideix amb cap màquina concreta** — diferent del `docker-compose.yml` de desenvolupament local, on el path SÍ ha de coincidir amb l'amfitrió perquè els symlinks es creen allí, no dins del contenidor), llança `onedrive --monitor` en bucle i el poller en bucle. **Mai `--resync` automàtic ací.**
- `docker-compose.portainer.yml` (diferent del `docker-compose.yml` de desenvolupament local, que no es toca): bind mounts a `${PCCF_DATA_DIR:-/docker/pccf}/onedrive_confdir` i `.../onedrive_memories:/data/onedrive-memories` (mateix conveni `/docker/<contenidor>/` que la resta d'stacks), xarxa externa `internal_pccf` (`external: true`, ha d'existir prèviament a Portainer, el contenidor només necessita eixida a Internet).
- **Bootstrap manual, una sola vegada**: crear les carpetes del bind mount amb `chown 1000:1000` abans del primer desplegament; `scp` dels fitxers `config`/`sync_list`/`refresh_token` (mai `items.sqlite3`) del perfil d'escriptori cap al bind mount del servidor; `--sync --resync --resync-auth` manual i supervisat via `docker exec` abans de reiniciar i deixar l'entrypoint normal prendre el control.
- El **token mai va per git** — viu només al bind mount del servidor; `.gitignore` té una xarxa de seguretat explícita (`refresh_token`, `onedrive_confdir/`, `.config/onedrive/`).

**⚠️ Lliçons apreses (incidents reals, 2026-07-05) — crítiques per a evitar repetir-les**:
1. **Mai matar un procés `onedrive` a mig `--resync`.** Corromp la base de dades local de seguiment, i el següent `--monitor`/`--sync` pot interpretar fitxers reals com "conflicte" i renombrar-los amb sufix `-pubuntusb-safeBackup-0001.md` al SharePoint compartit (contingut no es perd, però cal detectar-ho i restaurar el nom manualment — ja ha passat dos vegades).
2. **Mai col·locar/baixar fitxers dins la carpeta sincronitzada per fora del client `onedrive`** (p. ex. via crides pròpies a Graph API). La seua base de dades no se n'assabenta, i el següent sync ho tracta com a conflicte, generant el mateix problema de sufix `-safeBackup-`.
3. **`--resync` només manual i supervisat**, revisant el log línia a línia buscant `"Deleting item from Microsoft OneDrive"` inesperats abans de confiar-hi. Mai `--resync` automàtic en cap script/entrypoint que córrega sense supervisió.
4. Si apareix algun fitxer `*-safeBackup-*`: comprovar primer que l'original (sense sufix) existeix — si és així, és un duplicat inofensiu, esborrar-lo (local + remot via Graph API); si NO existeix l'original, cal renombrar el `-safeBackup-` de tornada al nom correcte (mai esborrar-lo sense comprovar-ho abans).
5. **Qualsevol canvi al fitxer `config` d'onedrive** (fins i tot afegir una línia com `threads`) fa que el client exigisca un nou `--resync` abans de continuar en `--monitor` — comportament normal del client, cal repetir el `--resync` supervisat cada vegada que s'edite `config`.
6. `tools/compilar_memories.py` prova motors LaTeX en l'ordre `lualatex` → `xelatex` → `pdflatex` (no a l'inrevés): el document usa el paquet `emoji` (marcador ❌ d'incidències a l'índex), que **requereix LuaTeX específicament** — amb `xelatex` falla amb "Critical Package emoji Error".
7. El `threads` del client `onedrive` per defecte és 8; si el servidor/contenidor té menys nuclis, afig `threads = "N"` (N = nuclis disponibles o menys) al `config` per evitar l'avís de sobrecàrrega (i recorda el punt 5: això dispararà un `--resync` necessari).

**Notificacions per correu al cap de departament (`tools/mailer.py`)**: implementació de l'opció (A) descrita més avall — quan `publish_memories_output.py` publica un report/PDF nou, `notify_department()` envia un correu al cap de departament corresponent. Disseny explícitament **no invasiu**: el mecanisme només s'activa si es compleixen totes dues condicions, i si en falta qualsevol el comportament és idèntic al d'abans que existira (cap error, cap canvi):
1. Variables d'entorn `SMTP_HOST` i `SMTP_FROM` configurades (vore `docker-compose.portainer.yml` → secció "Environment variables" de l'stack a Portainer; mai en git). Opcionals: `SMTP_PORT` (defecte `587`), `SMTP_USER`/`SMTP_PASSWORD` (login SMTP), `SMTP_USE_TLS` (defecte `1`, `starttls`), `SMTP_REPLY_TO` (capçalera `Reply-To` independent del remitent, p. ex. per a enviar amb un compte `notreply@...` i rebre respostes a una bústia vigilada).
2. El departament apareix a `department_emails.json`.

**Les adreces mai van en git** (el repositori és **públic** a GitHub): a diferència de la resta de configuració de departament (`memoriaESOBAT/memories_{DEPART}.json` / `memoriaFP/memories_{FAMILIA}.json`, que sí és pública i no conté dades personals), els emails viuen en un fitxer separat, exclusivament al bind mount del servidor:
```json
{"ESOBAT": {"ECONOMIA": "cap.economia@..."}, "FP": {"INF": "cap.informatica@..."}}
```
- Path per defecte: `DEPARTMENT_EMAILS_FILE` (Portainer: `/data/department_emails.json`, bind mount `${PCCF_DATA_DIR:-/docker/pccf}/department_emails.json`; en local sense la variable: `temp/department_emails.json`, ja gitignorat). **Ha d'existir al host ABANS del primer desplegament amb este bind mount** — si Docker no troba el fitxer origen en muntar-lo, crea un directori buit en son lloc i el contenidor falla en llegir-lo.
- `tools/mailer.py::get_department_email(tipus, familia)` llig eixe fitxer; qualsevol departament absent (o el fitxer sencer absent/malformat) es tracta com "sense email", mai llança excepció.
- Deliberadament **no** s'ha triat mesclar l'email dins del JSON de currículum via bind mount fitxer-a-fitxer: crearia una còpia duplicada de l'estructura de currículum al servidor que es desincronitzaria silenciosament de la versió en git cada volta que canviara un mòdul/curs.
- `tools/mailer.py::smtp_configured()` comprova la condició 1; `send_report_email()` fa l'enviament real (adjunta el `.txt` del report i el PDF si existeixen) i capça qualsevol excepció (SMTP caigut, credencials incorrectes) registrant-la per stdout sense interrompre el poller/publicació.
- Mecanisme d'enviament recomanat: SMTP amb un compte dedicat (p. ex. Gmail + contrasenya d'aplicació), evitant dependre de permisos del tenant GVA.

**Notificacions al propi docent (opció B, `tools/local_sync_poller.py::notify_teachers()`)**: avisa el docent de les deficiències de la seua pròpia memòria (no el report sencer del departament) quan el fitxer `.md` conté una línia opcional `correu-e` a la secció `### DOCENT`, p. ex.:
```
### DOCENT

**Docent**: Nom Cognoms

**correu-e**: nom.cognoms@edu.gva.es
```
- El camp és **opcional i el posa el propi docent dins del seu fitxer** — mai en git (el contingut dels `.md` viu exclusivament a la carpeta sincronitzada OneDrive, mai al repositori) i mai als JSON de departament.
- `memories_utils.py::get_teacher_email()` (regex `CORREU_E_RE`) l'extrau; accepta variants de negreta Markdown al voltant de `correu-e` (`**correu-e**:`, `correu-e:`, etc.), sensible a majúscules/minúscules.
- Reutilitza `check_placeholders()`/`check_stats_consistency()` (les mateixes funcions que ja usa el report) **sobre eixe fitxer en concret**, no sobre tot el departament — el correu només conté les deficiències d'eixa memòria individual.
- Executat des de `poll_once()` a cada passada del poller, per a cada fitxer `.md` de cada departament, **independentment** de si el departament dispara compilació/publicació (evita acoblament amb eixe flux).
- Estat persistent per fitxer (mtime ja notificat) a `temp/memories_teacher_notify_state.json` (mateix patró que `temp/pccf_poller_state.json`, mai dins la carpeta sincronitzada). Cada versió (mtime) d'un fitxer es processa com a màxim una vegada: si no té `correu-e` o no té deficiències, es marca com a vista i no es reavalua fins que canvie el fitxer; si l'enviament SMTP falla, l'estat NO es guarda i es reintenta a la propera passada.
- No invasiu en tots els nivells: sense `SMTP_HOST`/`SMTP_FROM` la funció no fa absolutament res (ni llig l'estat); sense el camp `correu-e` al fitxer, comportament idèntic a abans que existira esta funció.

## Sincronització OneDrive de PCCF/Programacions Didàctiques + marca d'aigua ESBORRANY

Extensió del mateix patró de sincronització OneDrive de la secció anterior a la generació del PCCF i les Programacions Didàctiques, mantenint el pipeline de dues fases (`generar-plantilles-pccf-%` / `compila-pccf-%`) intacte. Perfil `onedrive` i poller **separats** dels de memòries (aïlla els riscos de `--resync`/bugs entre els dos sistemes).

**Diferència clau amb memòries**: allà el docent crea els fitxers de zero; ací cal generar contingut previ (BORRADOR + Excel des del JSON del BOE) abans que hi haja res a editar. Com que la Fase 1 ja és idempotent per disseny (`cp -n`, mai sobreescriu `_BORRADOR`/`_OK` existent, Excel només si no existeix), el poller de PCCF reexecuta `generar-plantilles-pccf-{cicle}` a cada passada com a "bootstrap" sense risc — així un cicle nou queda disponible a OneDrive sense cap pas manual.

**`PLANTILLES_ROOT` (Makefile)**: nova variable (`?= .`, sense canvis en local) que substitueix el `plantilles_$(FAMILIA)_$(CICLO_UPPER)` hardcoded per `$(PLANTILLES_ROOT)/plantilles_$(FAMILIA)_$(CICLO_UPPER)` a `generar-plantilles-pccf-%`, `compila-pccf-%` i `report-pccf-%`. Al contenidor l'entrypoint la fixa a un symlink (`pccf_sync`) cap a la carpeta sincronitzada.

**Marca d'aigua "ESBORRANY"** (PCCF, Programaciones i Memòries): substitueix la idea d'un llindar de verificació que bloqueja alguna cosa — el PDF simplement porta una marca d'aigua visible quan queden incidències pendents, i no la porta quan tot està net:
- `rsrc/templates/eisvogel.latex`: bloc `$if(draft)$\usepackage{draftwatermark}...$endif$` (paquet ja disponible via `texlive-latex-extra`), activat amb `-V draft=true`.
- PCCF: `tools/report_pccf.py::is_verified()` torna `False` si queda algun PD en BORRADOR, algun placeholder `[###]`/`[...]`, o l'Excel de pesos RA és incoherent. El Makefile calcula això a `compila-pccf-%` (variable `DRAFT_OPT`) abans de cridar `pandoc`.
- Memòries: `tools/compilar_memories.py` activa `draft=true` si apareix qualsevol marcador ❌ (incidències) o ✏️ (BORRADOR) al TOC, o si hi ha mòduls `[FALTA]` (variable `document_has_draft_marker`). Els mòduls marcats `_NOIMPARTIT.md` (sense alumnat, confirmat pel cap de departament) NO compten com a `[FALTA]` i per tant no activen esta marca d'aigua.

**Poller de PCCF** (`tools/pccf_sync_poller.py`, anàleg a `tools/local_sync_poller.py`): per a cada cicle, quan detecta un canvi de mtime als `.md`/`.xlsx` de `plantilles_{FAMILIA}_{CICLO}/`:
1. Bootstrap idempotent (`generar-plantilles-pccf-{cicle}`).
2. Regenera i publica **sempre** el report (`compute_status`/`format_report`, barat: regex + `openpyxl`, sense LaTeX) a `0_report_pccf/{FAMILIA}_{CICLO}.txt`.
3. Només compila i publica els PDFs (car: pandoc+xelatex) quan l'estat `is_verified()` **canvia** respecte de l'última vegada (estat intern a `temp/pccf_poller_state.json`, mai dins la carpeta sincronitzada). Si la compilació o publicació fallen, l'estat NO es guarda, per a que la propera passada ho reintente encara que el docent no haja tornat a editar res.

**Publicació** (`tools/publish_pccf_output.py`, anàleg a `publish_memories_output.py` però sense timestamp perquè els noms de PDF ja són fixos):
```
General/PCCF i Programacions/0_report_pccf/{FAMILIA}_{CICLO}.txt
General/PCCF i Programacions/1_esborrany_pccf/PCCF_{CENTRE}_{CICLO}.pdf
General/PCCF i Programacions/1_esborrany_pccf/Programaciones_{CENTRE}_{CICLO}.pdf
```

**Desplegament**: `docker-entrypoint.sh` llança un segon `onedrive --monitor` (confdir `PCCF_ONEDRIVE_CONFDIR`, per defecte `/home/PCCF/.config/onedrive-pccf`) i `tools/pccf_sync_poller.py` (sync-root `$PCCF_SYNC_ROOT/$PCCF_SUBPATH`, per defecte `/data/onedrive-pccf/General/PCCF i Programacions`), en paral·lel als de memòries (`wait -n` ara amb 4 PIDs). `docker-compose.portainer.yml` afig els bind mounts `onedrive_confdir_pccf`/`onedrive_pccf`. Bootstrap manual del nou perfil: mateix procediment que memòries (token, `sync_list`, `--resync` únic i supervisat), repetit per a aquest segon `--confdir`.

**Seguretat de `make clean`**: com que `plantilles_*/` pot viure ara sota `PLANTILLES_ROOT` sincronitzat amb OneDrive, `clean` avorta si `PLANTILLES_ROOT != .` (esborrar-ho esborraria treball real dels docents i es replicaria com a esborrat a SharePoint).

**Nota tècnica**: les Portada `PD_000_*.md` referencien fons amb path relatiu `../rsrc/backgrounds/...`, assumint que `plantilles_{FAMILIA}_{CICLO}/` és germana de `rsrc/` a l'arrel del projecte — fals quan `PLANTILLES_ROOT` apunta fora. `compila-pccf-%` ho resol compilant les Programaciones des d'una còpia de muntatge a `temp/compila_pd_{CICLO}/` amb eixe path reescrit a absolut (mai es toquen els fitxers originals dels docents).

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
