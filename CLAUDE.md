# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Start here

**Read `AGENTS.md` first** — it is the authoritative, actively-maintained reference for this repo's build commands, pipeline, repo layout, and conventions (PCCF, optatives, and memòries systems). This file only adds pointers and things not already in `AGENTS.md`.

## What this repo is

Curricular projects (PCCF) and teaching plans (Programaciones Didácticas) for vocational training cycles at IES La Sénia / IESEPM, plus a separate system for compiling end-of-course department "memòries" (FP and ESO/BAT). Everything is driven by JSON data (from BOE) + Jinja2 templates → Markdown → Pandoc/XeLaTeX → PDF, with Excel spreadsheets (openpyxl) as a teacher-editable intermediate.

Content is in Valencian/Catalan; JSON keys are in Spanish (source: BOE), values in Valencian.

## Running things

**Always test via the Docker wrapper**, not directly on the host — the host environment has broken/missing LibreOffice and LaTeX:

```sh
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM proyecto-dam"
```

See `AGENTS.md` → "Build commands", "Docker", and "Testing" sections for the full command set (PCCF two-phase pipeline, optatives, memòries for FP and ESO/BAT, reports).

## Key things not to relearn by trial and error

- `tools/pccf_utils.py::get_hoja_label()` is where you add a mapping if a new Excel sheet name doesn't match a module — see `AGENTS.md` → Key conventions.
- `tools/memories_utils.py::CICLES_CONEGUTS` must include any newly added cycle.
- Generated/teacher-workspace directories are gitignored: `plantilles_*/`, `memories_FP/`, `memories_ESOBAT/`, `PDFS/`, `temp/`. Don't treat their absence as broken state.
- `boe_{INF,SCO}/rd-{ciclo}.json` is the single source of truth for curriculum data; everything else (Excel, PDs, PCCF sections) derives from it.
- CI (`.github/workflows/makefile.yml`) only builds on `main` when the commit message contains `[build]`.
- `memories_ESOBAT`/`memories_FP` may be **symlinks** to a OneDrive-synced folder (not plain generated directories), and `tools/local_sync_poller.py` may already be auto-compiling+publishing on file changes with zero manual trigger — see `AGENTS.md` → "Sincronització OneDrive de memòries" for the full mechanism, `tools/publish_memories_output.py`, Portainer deployment, and critical safety lessons (never kill `onedrive` mid-`--resync`, never `--resync` unsupervised, `lualatex` must stay preferred over `xelatex`) before touching anything related to it.
