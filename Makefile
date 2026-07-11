#!/usr/bin/make -f

SHELL := /bin/bash

# Version 0.5 - Pipeline en dues fases: generar plantilles + compilar
#               Plantilles persistents a plantilles_{FAMILIA}_{CICLO}/

# Colors
BLUE := $(shell printf '\033[1;34m')
LIGHTBLUE := $(shell printf '\033[94m')
LIGHTGREEN := $(shell printf '\033[92m')
LIGHTYELLOW := $(shell printf '\033[93m')
RESET := $(shell printf '\033[0m')

# Variables configurables
CENTRO_EDUCATIVO ?= SENIA

# Arrel on viu l'estructura completa del PCCF+PD dins de OneDrive (o localment).
# Conté: pccf/ (src* + 0_report/ + 1_esborrany/) i programacions/{CICLO}/ (PDs + 0_report/ + 1_esborrany/).
# Per defecte "." = project root (comportament local). Al contenidor, l'entrypoint
# la fixa al path de la carpeta sincronitzada amb OneDrive (pccf_sync).
PCCF_ROOT ?= .

# Anomen antic, mantingut per compatibilitat. Deprecat.
PLANTILLES_ROOT ?= .

# Project root (absolute)
PROJECT_ROOT:=$(shell readlink -f .)

# Templates (absolute paths for pandoc, since we cd to plantilles dir)
TEMPLATE_TEX_PD="$(PROJECT_ROOT)/rsrc/templates/eisvogel.latex"
PANDOC_OPTIONS="-V fontsize=12pt -V mainfont=\"$(PROJECT_ROOT)/rsrc/sorts-mill-goudy/OFLGoudyStM.otf\" -V toc-title=\"Índex\" --pdf-engine=xelatex"

# PDFS
PDF_PATH:=$(shell readlink -f PDFS)

# Lista de ciclos disponibles por familia
CICLOS_INF = smx dam ceiabd fpbiio
CICLOS_SCO = apd ei is
CICLOS_ALL = $(CICLOS_INF) $(CICLOS_SCO)

# Helper per determinar familia a partir del ciclo
check_ciclo = $(if $(filter $(1),$(CICLOS_INF)),INF,$(if $(filter $(1),$(CICLOS_SCO)),SCO,))

# RULES

todo:
	@echo " [ ${BLUE} * Cosas por hacer ${RESET}]"
	@rgrep "TODO" . | grep -v ".git" | grep -v "./temp/" | grep -v "./plantilles_"

dependences:
	@echo " [${BLUE} * Dependencias necesarias para PANDOC ${RESET}] "
	sudo apt update ; 	sudo apt install --yes make pandoc texlive-extra-utils texlive-lang-spanish texlive-latex-extra texlive-fonts-extra texlive-xetex libreoffice poppler-utils
	@echo " [${BLUE} * Dependencias necesarias para PYTHON ${RESET}] "
	sudo apt update ; sudo apt install --yes make python3-jinja2 python3-box python3-numpy python-openpyxl-doc python-pandas-doc python3-pandas python3-matplotlib

clean:
	@echo " [${BLUE} * Step : Clean ${RESET}] "
	@echo "${LIGHTBLUE} -- PDFS ${RESET}"
	rm -f PDFS/*.pdf PDFS/*.odt
	@echo "${LIGHTBLUE} -- Plantilles antigues (deprecades) ${RESET}"
	@if [ "$(PCCF_ROOT)" != "." ]; then \
		echo " ${LIGHTYELLOW} Error: PCCF_ROOT=$(PCCF_ROOT) (no és '.'): probablement apunta a la carpeta sincronitzada amb OneDrive.${RESET}"; \
		echo " ${LIGHTYELLOW} 'make clean' esborraria treball real dels docents i es replicaria com a esborrat a SharePoint. Avortant.${RESET}"; \
		echo " ${LIGHTYELLOW} Si de veres cal netejar dins d'eixa carpeta, fes-ho manualment i amb compte.${RESET}"; \
		exit 1; \
	fi
	rm -rf plantilles_INF_*/ plantilles_SCO_*/
	@# programacions/ es genera i es gitignored, nomes es neteja en local
	@if [ "$(PCCF_ROOT)" = "." ]; then rm -rf programacions/; else echo " ${LIGHTYELLOW} (programacions/ no es neteja: es dins de OneDrive) ${RESET}"; fi
	rm -rf temp/ luatex.*/

.PHONY: validate-json
validate-json:
	@python3 tools/validate_json.py

files:
	@echo " [${BLUE} * Creando Espacio ${RESET}] "
	@echo "${LIGHTBLUE} * Carpeta [ PDFS ]${RESET}"
	mkdir -p PDFS

proyecto-base: files
	@echo " [${BLUE} * Poblando el Proyecto Base ${RESET}"

# ============================================================
#  PCCF - PHASE 1: generate templates
# ============================================================
# Target-specific variables for generate
generar-plantilles-pccf-%: validate-json
	$(eval CICLO_RAW := $*)
	$(eval CICLO := $(shell echo $* | tr '[:upper:]' '[:lower:]'))
	$(eval CICLO_UPPER := $(shell echo $(CICLO) | tr '[:lower:]' '[:upper:]'))
	$(eval FAMILIA := $(call check_ciclo,$(CICLO)))
	$(eval PCCF_SRC := $(PCCF_ROOT)/pccf)
	$(eval PD_DIR := $(PCCF_ROOT)/programacions/$(CICLO_UPPER))
	@if [ -z "$(FAMILIA)" ]; then echo " ${LIGHTYELLOW} Error: ciclo no reconocido '$(CICLO)' ${RESET}"; exit 1; fi
	@echo " ${LIGHTBLUE} [ Generant plantilles PCCF: $(CICLO_UPPER) (Familia $(FAMILIA)) ] ${RESET}"

	@# Si PCCF_ROOT != project root, copiar pccf/ al sync root (bootstrap OneDrive)
	@if [ "$(shell readlink -f $(PCCF_ROOT))" != "$(PROJECT_ROOT)" ]; then \
		echo " ${LIGHTBLUE} Copiant pccf/ a $(PCCF_ROOT)/ (no sobreescriu)${RESET}"; \
		for d in src src_$(FAMILIA) src_$(FAMILIA)_$(CICLO_UPPER); do \
			[ -d "$(PROJECT_ROOT)/pccf/$$d" ] || continue; \
			mkdir -p "$(PCCF_SRC)/$$d" && \
			for f in "$(PROJECT_ROOT)/pccf/$$d"/*.md; do \
				[ -f "$$f" ] || continue; \
				b=$$(basename "$$f"); \
				[ -f "$(PCCF_SRC)/$$d/$$b" ] || cp -n "$$f" "$(PCCF_SRC)/$$d/"; \
			done; \
		done; \
	fi
	@echo " ${LIGHTBLUE} Copiant PD_*.md a programacions/$(CICLO_UPPER)/ (no sobreescriu)${RESET}"
	mkdir -p "$(PD_DIR)"
	@for d in $(PCCF_SRC)/src $(PCCF_SRC)/src_$(FAMILIA) $(PCCF_SRC)/src_$(FAMILIA)_$(CICLO_UPPER); do \
		[ -d "$$d" ] || continue; \
		for f in $$d/PD_*.md; do \
			[ -f "$$f" ] || continue; \
			b=$$(basename "$$f"); \
			[ -f "$(PD_DIR)/$$b" ] || cp -n "$$f" "$(PD_DIR)/"; \
		done; \
	done
	@echo " ${LIGHTBLUE} Generant Excel (si no existeix)${RESET}"
	@if [ ! -f "$(PD_DIR)/libro_$(CICLO_UPPER).xlsx" ]; then \
		./tools/json2excel.py $(CICLO_UPPER) $(FAMILIA) --outdir "$(PD_DIR)"; \
		echo " ${LIGHTBLUE} Excel generat${RESET}"; \
	else echo " ${LIGHTYELLOW} Excel conservat${RESET}"; fi
	@echo " ${LIGHTBLUE} Generant PDs des de plantilles Jinja2${RESET}"
	python3 tools/json2pccf.py $(CICLO_UPPER) $(FAMILIA) --outdir "$(PD_DIR)" --generate-only
	@echo " ${LIGHTGREEN} [ Plantilles $(CICLO_UPPER) generades a $(PD_DIR)/ ] ${RESET}"

# ============================================================
#  PCCF - PHASE 2: compile PDFs from templates
# ============================================================
compila-pccf-%:
	$(eval CICLO_RAW=$*)
	$(eval CICLO=$(shell echo $* | tr '[:upper:]' '[:lower:]'))
	$(eval CICLO_UPPER=$(shell echo $(CICLO) | tr '[:lower:]' '[:upper:]'))
	$(eval FAMILIA=$(call check_ciclo,$(CICLO)))
	@if [ -z "$(FAMILIA)" ]; then echo " ${LIGHTYELLOW} Error: ciclo no reconocido '$(CICLO_RAW)' ${RESET}"; exit 1; fi
	$(eval PCCF_SRC:=$(PCCF_ROOT)/pccf)
	$(eval PD_DIR:=$(PCCF_ROOT)/programacions/$(CICLO_UPPER))
	$(eval COMPILA_DIR:=$(PCCF_ROOT)/.compila_$(CICLO_UPPER))
	$(eval OUTPUT_DIR:=$(PCCF_ROOT)/pccf/1_esborrany)
	@if [ ! -d "$(PCCF_SRC)" ]; then echo " ${LIGHTYELLOW} Error: no existeix $(PCCF_SRC)/. Executa 'make generar-plantilles-pccf-$(CICLO_RAW)' primer. ${RESET}"; exit 1; fi
	@echo " ${LIGHTBLUE} [ Compilant PCCF: $(CICLO_UPPER) (Familia $(FAMILIA)) ] ${RESET}"
	mkdir -p "$(OUTPUT_DIR)"
	@echo " ${LIGHTBLUE} Generant PCCF_030/033 a .compila/ ${RESET}"
	mkdir -p "$(COMPILA_DIR)"
	python3 tools/json2pccf.py $(CICLO_UPPER) $(FAMILIA) --outdir "$(COMPILA_DIR)" --generate-competences
	@echo " ${LIGHTBLUE} Generant PCCF_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf ${RESET}"
	@# Staging: copiar PCCF_*.md de pccf/src* a .compila, després compilar
	@for d in src src_$(FAMILIA) src_$(FAMILIA)_$(CICLO_UPPER); do \
		[ -d "$(PCCF_SRC)/$$d" ] || continue; \
		for f in "$(PCCF_SRC)/$$d"/PCCF_*.md; do \
			[ -f "$$f" ] || continue; \
			b=$$(basename "$$f"); \
			[ -f "$(COMPILA_DIR)/$$b" ] || cp -n "$$f" "$(COMPILA_DIR)/"; \
		done; \
	done
	@# PCCF_*.md des de programacions/ (optatives, etc.)
	@for f in "$(PD_DIR)"/PCCF_*.md; do \
		[ -f "$$f" ] || continue; \
		b=$$(basename "$$f"); \
		[ -f "$(COMPILA_DIR)/$$b" ] || cp -n "$$f" "$(COMPILA_DIR)/"; \
	done
	@cd "$(PROJECT_ROOT)" && \
		FILES=$$(find "$(COMPILA_DIR)" -maxdepth 1 -name 'PCCF_*.md' -type f 2>/dev/null | \
			while IFS= read -r f; do \
				b=$$(basename "$$f"); \
				n=$$(echo "$$b" | cut -d_ -f2); \
				echo "$$n:$$f"; \
			done | sort -t: -k1 -n | cut -d: -f2-); \
		mapfile -t FILES_ARR <<< "$$FILES"; \
		pandoc --resource-path "$(COMPILA_DIR)" \
			--template $(TEMPLATE_TEX_PD) $(PANDOC_OPTIONS) \
			-o "$(OUTPUT_DIR)/PCCF_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf" \
			"$${FILES_ARR[@]}"
	@echo " ${LIGHTBLUE} Incluint PDs d'optatives (només les del cicle)${RESET}"
	python3 tools/copy_optatives_pd.py "$(CICLO_UPPER)" "$(FAMILIA)" "$(PD_DIR)" "$(PCCF_ROOT)/programacions/OPTATIVES"
	@echo " ${LIGHTBLUE} Netejant fitxers temporals${RESET}"
	rm -rf "$(COMPILA_DIR)" "$(PD_DIR)/.optatives_pd"
	@echo " ${LIGHTGREEN} [ Compilacio PCCF $(CICLO_UPPER) completada ] ${RESET}"

# ============================================================
#  PD (Programacions) - compile manually (disparat per cap de departament)
# ============================================================
compila-pd-pccf-%:
	$(eval CICLO_RAW=$*)
	$(eval CICLO=$(shell echo $* | tr '[:upper:]' '[:lower:]'))
	$(eval CICLO_UPPER=$(shell echo $(CICLO) | tr '[:lower:]' '[:upper:]'))
	$(eval FAMILIA=$(call check_ciclo,$(CICLO)))
	@if [ -z "$(FAMILIA)" ]; then echo " ${LIGHTYELLOW} Error: ciclo no reconocido '$(CICLO_RAW)' ${RESET}"; exit 1; fi
	$(eval PD_DIR:=$(PCCF_ROOT)/programacions/$(CICLO_UPPER))
	$(eval OUTPUT_DIR:=$(PD_DIR)/1_esborrany)
	@if [ ! -d "$(PD_DIR)" ]; then echo " ${LIGHTYELLOW} Error: no existeix $(PD_DIR)/. Executa 'make generar-plantilles-pccf-$(CICLO_RAW)' primer. ${RESET}"; exit 1; fi
	@echo " ${LIGHTBLUE} [ Compilant Programaciones: $(CICLO_UPPER) ] ${RESET}"
	mkdir -p "$(OUTPUT_DIR)"
	@echo " ${LIGHTBLUE} Generant Programaciones_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf ${RESET}"
	@# Es compila des d'un directori de muntatge local (temp/), no directament
	@# des de PD_DIR: les Portada.md referencien fons amb path relatiu
	@# "../rsrc/backgrounds/..." assumint que la plantilla és germana de rsrc/
	@# a l'arrel del projecte -- fals quan PCCF_ROOT apunta fora (OneDrive).
	@# Reescrivim eixe path a absolut en una còpia, mai als fitxers dels docents.
	@STAGE="$(PROJECT_ROOT)/temp/compila_pd_$(CICLO_UPPER)"; \
		rm -rf "$$STAGE" && mkdir -p "$$STAGE" && \
		cp "$(PD_DIR)"/PD_*.md "$$STAGE/" && \
		if [ -f "$(PD_DIR)/.optatives_pd/.copied_count" ] && [ "$$(cat "$(PD_DIR)/.optatives_pd/.copied_count")" -gt 0 ]; then \
			cp "$(PD_DIR)"/.optatives_pd/PD_*.md "$$STAGE/"; \
		fi && \
		sed -i "s#\.\./rsrc/backgrounds/#$(PROJECT_ROOT)/rsrc/backgrounds/#g" "$$STAGE"/*.md && \
		cd "$$STAGE" && \
		pandoc --template $(TEMPLATE_TEX_PD) $(PANDOC_OPTIONS) \
			-o "$(OUTPUT_DIR)/Programaciones_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf" ./PD_*.md
	@echo " ${LIGHTBLUE} Generant PDs individuals (ignorant errors)${RESET}"
	-./tools/shell-progs-didacticas-standalone.sh $(CICLO_UPPER) "$(PD_DIR)" 2>&1 | tail -3
	@echo " ${LIGHTBLUE} Generant report de PD a $(PD_DIR)/0_report/${RESET}"
	python3 tools/report_pccf.py $(CICLO_UPPER) --pd-dir "$(PD_DIR)" --type pd
	@echo " ${LIGHTBLUE} Netejant fitxers temporals${RESET}"
	rm -rf "$(PD_DIR)/.optatives_pd" "$(PROJECT_ROOT)/temp/compila_pd_$(CICLO_UPPER)"
	@echo " ${LIGHTGREEN} [ Compilacio Programaciones $(CICLO_UPPER) completada ] ${RESET}"

# ============================================================
#  PCCF - Backward compatible: generate + compile (només PCCF)
# ============================================================
proyecto-%: generar-plantilles-pccf-% compila-pccf-%
	@echo " ${LIGHTGREEN} [ Proyecto $(shell echo $* | tr '[:lower:]' '[:upper:]') Completado ] ${RESET}"

# ============================================================
#  Report: detect pending [###] placeholders in templates
# ============================================================
report-pccf-%:
	$(eval CICLO_RAW=$*)
	$(eval CICLO=$(shell echo $* | tr '[:upper:]' '[:lower:]'))
	$(eval CICLO_UPPER=$(shell echo $(CICLO) | tr '[:lower:]' '[:upper:]'))
	$(eval FAMILIA=$(call check_ciclo,$(CICLO)))
	@if [ -z "$(FAMILIA)" ]; then echo " ${LIGHTYELLOW} Error: ciclo no reconocido '$(CICLO_RAW)' ${RESET}"; exit 1; fi
	$(eval PD_DIR:=$(PCCF_ROOT)/programacions/$(CICLO_UPPER))
	@if [ ! -d "$(PD_DIR)" ]; then echo " ${LIGHTYELLOW} Error: no existeix $(PD_DIR)/. Executa 'make generar-plantilles-pccf-$(CICLO_RAW)' primer. ${RESET}"; exit 1; fi
	python3 tools/report_pccf.py $(CICLO_UPPER) --pd-dir "$(PD_DIR)" --type pd

# ============================================================
#  OPTATIVES (shared transversal modules)
# ============================================================
generar-plantilles-optatives:
	@echo " ${LIGHTBLUE} [ Generant plantilles optatives compartides ] ${RESET}"
	@mkdir -p "$(PCCF_ROOT)/programacions/OPTATIVES"
	python3 tools/json2optatives.py --outdir "$(PCCF_ROOT)/programacions/OPTATIVES"
	@echo " ${LIGHTGREEN} [ Plantilles optatives generades a $(PCCF_ROOT)/programacions/OPTATIVES/ ] ${RESET}"

report-optatives:
	@echo " ${LIGHTYELLOW} [ Report optatives ] ${RESET}"
	python3 tools/report_optatives.py --pd-dir "$(PCCF_ROOT)/programacions/OPTATIVES"

# ============================================================
#  Bulk targets (all cycles)
# ============================================================
todos: $(addprefix proyecto-,$(CICLOS_ALL)) report
	@echo " ${LIGHTGREEN} [ Todos los proyectos generados ] ${RESET}"

todos-inf: $(addprefix proyecto-,$(CICLOS_INF)) report
	@echo " ${LIGHTGREEN} [ Todos los proyectos INF generados ] ${RESET}"

todos-sco: $(addprefix proyecto-,$(CICLOS_SCO)) report
	@echo " ${LIGHTGREEN} [ Todos los proyectos SCO generados ] ${RESET}"

report:
	@echo " ${LIGHTYELLOW} [ Generando reporte de análisis de JSONs... ] ${RESET}"
	python3 tools/analizar_json.py

report-tots-pccf:
	@for c in $(CICLOS_ALL); do \
		$(MAKE) report-pccf-$$c; \
	done

## ----------------------------------------------------------------
##  Memòries del Departament
## ----------------------------------------------------------------

FAMILIA ?= INF
BASE_DIR ?= memoriaFP

DEPARTAMENTS_ESOBAT = ANGLES BIOLOGIA_GEOLOGIA DIBUIX ECONOMIA EDUCACIO_FISICA FILOSOFIA FISICA_QUIMICA FRANCES GEOGRAFIA_HISTORIA INFORMATICA LLATI LLENGUA_CASTELLANA LLENGUA_VALENCIANA MATEMATIQUES MUSICA RELIGIO TECNOLOGIA

genera-tots-esobat:
	@for dep in $(DEPARTAMENTS_ESOBAT); do \
		echo " ${LIGHTBLUE} [ Generant plantilles: $$dep ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaESOBAT FAMILIA=$$dep generar-plantilles-memoria; \
	done

report-tots-esobat:
	@REPORT_TIMESTAMP=$$(date +%Y%m%d_%H%M); export REPORT_TIMESTAMP; \
	for dep in $(DEPARTAMENTS_ESOBAT); do \
		echo " ${LIGHTYELLOW} [ Report: $$dep ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaESOBAT FAMILIA=$$dep report-memories; \
	done

compila-tots-esobat:
	@REPORT_TIMESTAMP=$$(date +%Y%m%d_%H%M); export REPORT_TIMESTAMP; \
	for dep in $(DEPARTAMENTS_ESOBAT); do \
		echo " ${LIGHTBLUE} [ Compilant: $$dep ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaESOBAT FAMILIA=$$dep compila-memories; \
	done

FAMILIES_FP = ANG FOL INF SCO

genera-tots-fp:
	@for fam in $(FAMILIES_FP); do \
		echo " ${LIGHTBLUE} [ Generant plantilles FP: $$fam ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaFP FAMILIA=$$fam generar-plantilles-memoria; \
	done

report-tots-fp:
	@REPORT_TIMESTAMP=$$(date +%Y%m%d_%H%M); export REPORT_TIMESTAMP; \
	for fam in $(FAMILIES_FP); do \
		echo " ${LIGHTYELLOW} [ Report FP: $$fam ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaFP FAMILIA=$$fam report-memories; \
	done

compila-tots-fp:
	@REPORT_TIMESTAMP=$$(date +%Y%m%d_%H%M); export REPORT_TIMESTAMP; \
	for fam in $(FAMILIES_FP); do \
		echo " ${LIGHTBLUE} [ Compilant FP: $$fam ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaFP FAMILIA=$$fam compila-memories; \
	done

generar-plantilles-memoria genera-memories:
	@echo " ${LIGHTBLUE} [ Generant plantilles de memòria ($(FAMILIA), base=$(BASE_DIR)) ] ${RESET}"
	python3 tools/generar_plantilles_memoria.py --base-dir $(BASE_DIR) $(FAMILIA)

report-memories:
	@echo " ${LIGHTYELLOW} [ Generant report de memòries ($(FAMILIA), base=$(BASE_DIR)) ] ${RESET}"
	python3 tools/report_memories.py --base-dir $(BASE_DIR) $(FAMILIA) $(CENTRO_EDUCATIVO)

compila-memories:
	@echo " ${LIGHTBLUE} [ Compilant memòries ($(FAMILIA), base=$(BASE_DIR)) ] ${RESET}"
	python3 tools/compilar_memories.py --base-dir $(BASE_DIR) $(FAMILIA) $(CENTRO_EDUCATIVO) --all

compilar-memories:
	@echo " ${LIGHTBLUE} [ Compilant memòries ($(FAMILIA), base=$(BASE_DIR)) ] ${RESET}"
	python3 tools/compilar_memories.py --base-dir $(BASE_DIR) $(FAMILIA) $(CENTRO_EDUCATIVO)

memories: generar-plantilles-memoria compila-memories
	@echo " ${LIGHTGREEN} [ Procés de memòries completat ] ${RESET}"

# Regla para mostrar ayuda
help:
	@echo "Uso: make [CENTRO_EDUCATIVO=nombre_del_centro] <target>"
	@echo ""
	@echo "Targets disponibles:"
	@echo "  Families INF i SCO:"
	@echo "    generar-plantilles-pccf-{ciclo}  Genera PCCF + PDs + Excel a pccf/ i programacions/"
	@echo "    compila-pccf-{ciclo}             Compila PCCF PDF (auto si canvia pccf/src*)"
	@echo "    compila-pd-pccf-{ciclo}          Compila Programaciones PDF (manual, cap dept)"
	@echo "    report-pccf-{ciclo}              Report de [###] pendents d'emplenar"
	@echo "    proyecto-{ciclo}                 Equival a generar-plantilles + compila-pccf"
	@echo "    report-tots-pccf                 Report de [###] per a tots els cicles"
	@echo "  Cicles disponibles:"
	@echo "    Familia INF: smx, dam, ceiabd, fpbiio"
	@echo "    Familia SCO: apd, ei, is"
	@echo "  Conjunt:"
	@echo "    todos              Generar todos los proyectos"
	@echo "    todos-inf          Generar todos los proyectos INF"
	@echo "    todos-sco          Generar todos los proyectos SCO"
	@echo "    report             Generar reporte de análisis de JSONs"
	@echo "  Optatives (compartides):"
	@echo "    generar-plantilles-optatives  Genera Excel + PDs dels mòduls optatius compartits a programacions/OPTATIVES"
	@echo "    report-optatives               Report de l'estat de les optatives"
	@echo ""
	@echo "  Memòries:"
	@echo "    report-memories             Report de l'estat de les memòries"
	@echo "    compila-memories            Report + confirmació + compila tot"
	@echo "    memories                    Tot el procés (genera + compila)"
	@echo "    genera-tots-esobat / report-tots-esobat / compila-tots-esobat"
	@echo "    genera-tots-fp / report-tots-fp / compila-tots-fp"
	@echo "  Altres:"
	@echo "    clean              Limpiar archivos generados (PDFS + plantilles)"
	@echo "    dependences        Instalar dependencias"
	@echo "    validate-json      Validar JSONs"
	@echo ""
	@echo "Exemples:"
	@echo "  make proyecto-dam                           # Genera + compila PCCF"
	@echo "  make compila-pd-pccf-apd                    # Compila Programaciones (manual)"
	@echo "  make generar-plantilles-pccf-dam            # Només plantilles (per a docents)"
	@echo "  make compila-pccf-dam                       # Compila PCCF des de plantilles"
	@echo "  make report-pccf-dam                        # Què falta per emplenar?"
	@echo "  make CENTRO_EDUCATIVO=IESEPM proyecto-smx   # Escolarització diferent"
	@echo "  ./contenedor_lanza.sh \"make proyecto-dam\"   # Via Docker (recomanat)"
