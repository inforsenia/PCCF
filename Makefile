#!/usr/bin/make -f

SHELL := /bin/bash

# Version 0.5 - Pipeline en dues fases: generar plantilles + compilar
#               Plantilles persistents a plantilles_{FAMILIA}_{CICLO}/

# Colors
BLUE= \e[1;34m
LIGHTBLUE= \e[94m
LIGHTGREEN= \e[92m
LIGHTYELLOW= \e[93m
RESET= \e[0m

# Variables configurables
CENTRO_EDUCATIVO ?= SENIA

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
	@echo "${LIGHTBLUE} -- Plantilles ${RESET}"
	rm -rf plantilles_INF_*/ plantilles_SCO_*/
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
	$(eval PLANTILLES_DIR := plantilles_$(FAMILIA)_$(CICLO_UPPER))
	@if [ -z "$(FAMILIA)" ]; then echo " ${LIGHTYELLOW} Error: ciclo no reconocido '$(CICLO)' ${RESET}"; exit 1; fi
	@echo " ${LIGHTBLUE} [ Generant plantilles PCCF: $(CICLO_UPPER) (Familia $(FAMILIA)) ] ${RESET}"
	mkdir -p "$(PLANTILLES_DIR)"
	@echo " ${LIGHTBLUE} Copiant PD_*.md des de src/ (no sobreescriu)${RESET}"
	@for d in src src_$(FAMILIA) src_$(FAMILIA)_$(CICLO_UPPER); do \
		[ -d "$$d" ] || continue; \
		for f in $$d/PD_*.md; do \
			[ -f "$$f" ] || continue; \
			b=$$(basename "$$f"); \
			[ -f "$(PLANTILLES_DIR)/$$b" ] || cp -n "$$f" "$(PLANTILLES_DIR)/"; \
		done; \
	done
	@echo " ${LIGHTBLUE} Generant Excel (si no existeix)${RESET}"
	@if [ ! -f "$(PLANTILLES_DIR)/libro_$(CICLO_UPPER).xlsx" ]; then \
		./tools/json2excel.py $(CICLO_UPPER) $(FAMILIA) --outdir "$(PLANTILLES_DIR)"; \
		echo " ${LIGHTBLUE} Excel generat${RESET}"; \
	else echo " ${LIGHTYELLOW} Excel conservat${RESET}"; fi
	@echo " ${LIGHTBLUE} Generant PDs des de plantilles Jinja2${RESET}"
	python3 tools/json2pccf.py $(CICLO_UPPER) $(FAMILIA) --outdir "$(PLANTILLES_DIR)" --generate-only
	@echo " ${LIGHTGREEN} [ Plantilles $(CICLO_UPPER) generades a $(PLANTILLES_DIR)/ ] ${RESET}"

# ============================================================
#  PCCF - PHASE 2: compile PDFs from templates
# ============================================================
compila-pccf-%:
	$(eval CICLO_RAW=$*)
	$(eval CICLO=$(shell echo $* | tr '[:upper:]' '[:lower:]'))
	$(eval CICLO_UPPER=$(shell echo $(CICLO) | tr '[:lower:]' '[:upper:]'))
	$(eval FAMILIA=$(call check_ciclo,$(CICLO)))
	@if [ -z "$(FAMILIA)" ]; then echo " ${LIGHTYELLOW} Error: ciclo no reconocido '$(CICLO_RAW)' ${RESET}"; exit 1; fi
	$(eval PLANTILLES_DIR=plantilles_$(FAMILIA)_$(CICLO_UPPER))
	@if [ ! -d "$(PLANTILLES_DIR)" ]; then echo " ${LIGHTYELLOW} Error: no existeix $(PLANTILLES_DIR)/. Executa 'make generar-plantilles-pccf-$(CICLO_RAW)' primer. ${RESET}"; exit 1; fi
	@echo " ${LIGHTBLUE} [ Compilant PCCF: $(CICLO_UPPER) (Familia $(FAMILIA)) ] ${RESET}"
	mkdir -p PDFS
	@echo " ${LIGHTBLUE} Generant PCCF_030/033 a .compila/ ${RESET}"
	mkdir -p "$(PLANTILLES_DIR)/.compila"
	python3 tools/json2pccf.py $(CICLO_UPPER) $(FAMILIA) --outdir "$(PLANTILLES_DIR)/.compila" --generate-competences
	@echo " ${LIGHTBLUE} Generant PCCF_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf ${RESET}"
	@cd "$(PROJECT_ROOT)" && \
		FILES=$$(find src src_$(FAMILIA) src_$(FAMILIA)_$(CICLO_UPPER) "$(PLANTILLES_DIR)/.compila" \
			-maxdepth 1 -name 'PCCF_*.md' -type f 2>/dev/null | \
			while IFS= read -r f; do \
				b=$$(basename "$$f"); \
				n=$$(echo "$$b" | cut -d_ -f2); \
				echo "$$n:$$f"; \
			done | sort -t: -k1 -n | cut -d: -f2-); \
		pandoc --resource-path src:src_$(FAMILIA):src_$(FAMILIA)_$(CICLO_UPPER):"$(PLANTILLES_DIR)"/.compila \
			--template $(TEMPLATE_TEX_PD) $(PANDOC_OPTIONS) \
			-o "$(PDF_PATH)/PCCF_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf" \
			$$FILES
	@echo " ${LIGHTBLUE} Incluint PDs d'optatives (només les del cicle)${RESET}"
	python3 tools/copy_optatives_pd.py "$(CICLO_UPPER)" "$(FAMILIA)" "$(PLANTILLES_DIR)"
	@echo " ${LIGHTBLUE} Generant Programaciones_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf ${RESET}"
	@cd "$(PLANTILLES_DIR)" && \
		OPT_PD_GLOB="./.optatives_pd/PD_*.md"; \
		if [ -f "./.optatives_pd/.copied_count" ] && [ "$$(cat ./.optatives_pd/.copied_count)" -gt 0 ]; then \
			pandoc --template $(TEMPLATE_TEX_PD) $(PANDOC_OPTIONS) -o "$(PDF_PATH)/Programaciones_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf" ./PD_*.md $$OPT_PD_GLOB; \
		else \
			pandoc --template $(TEMPLATE_TEX_PD) $(PANDOC_OPTIONS) -o "$(PDF_PATH)/Programaciones_$(CENTRO_EDUCATIVO)_$(CICLO_UPPER).pdf" ./PD_*.md; \
		fi
	@echo " ${LIGHTBLUE} Netejant fitxers temporals${RESET}"
	rm -rf "$(PLANTILLES_DIR)/.compila" "$(PLANTILLES_DIR)/.optatives_pd"
	@echo " ${LIGHTBLUE} Generant PDs individuals (ignorant errors)${RESET}"
	-./tools/shell-progs-didacticas-standalone.sh $(CICLO_UPPER) "$(PLANTILLES_DIR)" 2>&1 | tail -3
	@echo " ${LIGHTGREEN} [ Compilacio $(CICLO_UPPER) completada ] ${RESET}"

# ============================================================
#  PCCF - Backward compatible: generate + compile
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
	$(eval PLANTILLES_DIR=plantilles_$(FAMILIA)_$(CICLO_UPPER))
	@if [ ! -d "$(PLANTILLES_DIR)" ]; then echo " ${LIGHTYELLOW} Error: no existeix $(PLANTILLES_DIR)/. Executa 'make generar-plantilles-pccf-$(CICLO_RAW)' primer. ${RESET}"; exit 1; fi
	python3 tools/report_pccf.py $(CICLO_UPPER) "$(PLANTILLES_DIR)"

# ============================================================
#  OPTATIVES (shared transversal modules)
# ============================================================
generar-plantilles-optatives:
	@echo " ${LIGHTBLUE} [ Generant plantilles optatives compartides ] ${RESET}"
	@mkdir -p optatives/plantilles
	python3 tools/json2optatives.py
	@echo " ${LIGHTGREEN} [ Plantilles optatives generades a optatives/plantilles/ ] ${RESET}"

report-optatives:
	@echo " ${LIGHTYELLOW} [ Report optatives ] ${RESET}"
	python3 tools/report_optatives.py

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
	@for dep in $(DEPARTAMENTS_ESOBAT); do \
		echo " ${LIGHTYELLOW} [ Report: $$dep ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaESOBAT FAMILIA=$$dep report-memories; \
	done

compila-tots-esobat:
	@for dep in $(DEPARTAMENTS_ESOBAT); do \
		echo " ${LIGHTBLUE} [ Compilant: $$dep ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaESOBAT FAMILIA=$$dep compila-memories; \
	done

FAMILIES_FP = INF SCO

genera-tots-fp:
	@for fam in $(FAMILIES_FP); do \
		echo " ${LIGHTBLUE} [ Generant plantilles FP: $$fam ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaFP FAMILIA=$$fam generar-plantilles-memoria; \
	done

report-tots-fp:
	@for fam in $(FAMILIES_FP); do \
		echo " ${LIGHTYELLOW} [ Report FP: $$fam ] ${RESET}"; \
		$(MAKE) BASE_DIR=memoriaFP FAMILIA=$$fam report-memories; \
	done

compila-tots-fp:
	@for fam in $(FAMILIES_FP); do \
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
	@echo "    generar-plantilles-pccf-{ciclo}  Genera plantilles MD + Excel a plantilles_{FAMILIA}_{CICLO}/"
	@echo "    compila-pccf-{ciclo}             Compila PDFs des de les plantilles"
	@echo "    report-pccf-{ciclo}              Report de [###] pendents d'emplenar"
	@echo "    proyecto-{ciclo}                 Equival a generar-plantilles + compila (compatible)"
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
	@echo "    generar-plantilles-optatives  Genera Excel + PDs dels mòduls optatius compartits"
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
	@echo "  make proyecto-dam                           # Genera plantilles + compila"
	@echo "  make generar-plantilles-pccf-dam            # Només plantilles (per a docents)"
	@echo "  make compila-pccf-dam                       # Compila des de plantilles existents"
	@echo "  make report-pccf-dam                        # Què falta per emplenar?"
	@echo "  make CENTRO_EDUCATIVO=IESEPM proyecto-smx   # Escolarització diferent"
	@echo "  ./contenedor_lanza.sh \"make proyecto-dam\"   # Via Docker (recomanat)"
