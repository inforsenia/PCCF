# PCCF

Proyectos Curriculares de la Familía de Informática del IES La Sénia - Paiporta.

En este Repositorio podrás encontrar las fuentes en formato Markdown de los diferentes
Proyectos Curriculares de la Familia de Informática, así como la posibilidad de generar
las diferentes hojas de cálculo de las Programaciones Didácticas de los Módulos
a partir de los contenidos del BOE que se leen desde diferentes JSON.

Se trata de un proyecto en desarrollo, que contiene toda la información de los 
diferentes ciclos.

## Ciclos Formativos

### Familia de Informática:

| Siglas | Nombre Completo | Nivel |
|--------|-----------------|-------|
| IIO | Informática y Oficina | Grado Básico |
| SMX    | Sistemas Microinformáticos y Redes | Grado Medio |
| DAW 	 | Desarrollo de Aplicaciones Web | Grado Superior |
| DAM    | Desarrollo de Aplicaciones Multiplataforma | Grado Superior |
| ASIR   | Admnistración de Sistemas Informáticos y Redes | Grado Superior |
| CEIABD | Curso de especialización de IA y BD | Curso de Especialización |

### Familia de Servicios a la comunidad:

| Siglas | Nombre Completo | Nivel |
|--------|-----------------|-------|
| APD | Atención a Personas en Situación de Dependencia | Grado Medio |
| EI    | Educación Infantil | Grado Superior |
| IS 	 | Integración Social | Grado Superior |


## Entorno y Desarrollo

Se recomienda usar `emacs`, un editor de texto para toda una vida, scite o `vim` y trabajar desde
Sistemas Operativos que promuevan el Software Libre y Abierto, como Ubuntu o Debian.

[![Emacs](https://img.shields.io/badge/Emacs-%237F5AB6.svg?&logo=gnu-emacs&logoColor=white)](https://www.gnu.org/software/emacs/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=white)](#)

## Herramientas

[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![Bash](https://img.shields.io/badge/Bash-4EAA25?logo=gnubash&logoColor=fff)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![Haskell](https://img.shields.io/badge/Haskell-3776AB?logo=haskell&logoColor=fff)](#)

---
## Filosofía

[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://fsfe.org/)

---

## Proyectos Curriculares de Ciclos Formativos

Los Proyectos Curriculares (PCCF), se construyen usando varios niveles de construcción, la parte común a todos
los PCCFs se obtienen a partir de los ficheros que provienen de `/src/`,

**Pipeline bifàsica (PCCF)**:
1. **Generació de plantilles** (`make generar-plantilles-pccf-dam`): copia `PD_*.md` a `plantilles_{FAMILIA}_{CICLO}/` + genera `libro_{CICLO}.xlsx`.
2. **El docent ompli** les PDs (canvia `_BORRADOR` a `_OK`) i l'excel.
3. **Report** (`make report-pccf-dam`): mostra estat BORRADOR/OK, `[###]` pendents, i coherència de l'excel.
4. **Compilació** (`make compila-pccf-dam`): genera el `PCCF_{CENTRO}_{CICLO}.pdf` i el `Programaciones_{CENTRO}_{CICLO}.pdf`.

`make proyecto-dam` fa (1) + (4) en un sol pas (compatible cap enrere).

**Mòduls optatius compartits** (`make generar-plantilles-optatives`):
- Els mòduls optatius de centre (MOPCOMPROF, MOPANGPROF, INP, IPR) es gestionen desde `optatives/optatives.json` (compartit entre tots els cicles).
- `make generar-plantilles-optatives` genera `optatives/libro_optatives.xlsx` i `optatives/plantilles/PD_*_BORRADOR.md`.
- `make report-optatives` mostra l'estat BORRADOR/OK i `[###]` pendents.
- Durant la compilació (`make compila-pccf-{CICLO}`), les PDs dels optatius que corresponguen al cicle es copien automàticament des de `optatives/plantilles/`.

---

## Programaciones Didácticas

### Creación del fichero

Las Programaciones Didácticas de cada módulo se construyen en varias "etapas". 

Por un lado tenemos la generación 
automática de ficheros a partir de las plantillas Jinja2, que se generan en `plantilles_{FAMILIA}_{CICLO}/` (fitxers `PD_*_BORRADOR.md`).

Y por otra parte podemos crear un fichero con el mismo nombre en la carpeta del Ciclo correspondiente (`src_ASIR/`,`src_SMX/`,`src_DAW/`,`src_DAM/`). En ese caso, la generació automàtica no sobreescriurà el fitxer i usarà el que el/la docente haya establecido.

A més, el/la docent pot editar directament el fitxer `PD_*_BORRADOR.md` dins `plantilles_{FAMILIA}_{CICLO}/` i, quan estiga complet, canviar-li el nom a `PD_*_OK.md`.

### Completado de la plantilla

La plantilla del módulo elegido incluye una serie de mensajes y de marcas que deben ser revisados por parte 
del docente:

#### A RELLENAR POR DOCENTE

En algunas secciones encontraréis el texto: `A RELLENAR POR DOCENTE`, donde deberéis rellenar
con lo que se pide en cada una de las secciones.

#### Imports del PCCF

Como se ve en las diferentes plantillas, si se desea incluir alguno de los ficheros que conforman el texto refundido de los PCCFs, es tan sencillo
como poner el nombre del fichero con tres `@` delante, y el *compilador* se encarga de introducir el texto 
en la Programación Didáctica del Módulo.

Ejemplo:

```markdown
...

A continuación los valores del Software Libre reflejados 
en el PCCF, que se muestran en esta Programación Didáctica con 
el fin de aportar más claridad.

@@@PCCF_009_SoftwareLibre.md

...

```
### Hoja de Cálculo

La Hoja de Cálculo Compartida en el repositorio del Departamento ha de ser rellenada con los pesos y 
secuenciaciones de horas adecuadas. Cuando todo el departamento haya rellenado la hoja de cálculo con sus 
pesos y horas, se construirán las diferentes Programaciones Didácticas estableciendo como última página del PDF
la hoja respectiva de su módulo. 

Se han añadido las listas de las Competencias Profesionales y Sociales con su nivel de importancia (estrellas ★).

### Documentos generados automáticamente

El sistema genera automáticamente varios documentos a partir de los datos del JSON:

- **PCCF_033_ImportanciaCompetencies.md**: Tabla con todas las competencias del ciclo y su nivel de importancia (★, ★★, ★★★)
- **PCCF_030_ContribucioModuls.md**: Tablas que muestran qué módulos contribuyen a desarrollar cada competencia (profesionales y de ocupabilidad)

Estos documentos se generan **durante la compilación** (`make compila-pccf-{CICLO}`) en una carpeta temporal `.compila/` dins `plantilles_{FAMILIA}_{CICLO}/` i s'integren automàticament en el PCCF final. La carpeta `.compila/` es neteja automàticament després de la compilació.

Si es vol tindre una còpia permanent d'estos fitxers, es poden copiar a `src_{FAMILIA}_{CICLO}/`.

### Mòduls Optatius Compartits

Els mòduls optatius de centre (MOPCOMPROF, MOPANGPROF, INP, IPR) es defineixen una sola vegada a `optatives/optatives.json` i es compartixen entre tots els cicles que els oferten.

**Característiques**:
- Dades úniques (RAs, CEs, hores) al JSON centralitzat
- Excel compartit: `optatives/libro_optatives.xlsx`
- PDs compartides a `optatives/plantilles/PD_{CODI}_{MODUL}_{ESTAT}.md`
- `ObjetivosGenerales` i `CompetenciasTitulo` buits al JSON (no apliquen a un cicle específic)

**Generació**:
```sh
make generar-plantilles-optatives   # genera Excel + PDs
make report-optatives               # report d'estat
```

**Integració en la compilació**: `make compila-pccf-{CICLO}` detecta quins optatius corresponen al cicle (segons el camp `grups` del JSON) i copia les PDs des de `optatives/plantilles/` cap a `.compila/` temporal dins `plantilles_{FAMILIA}_{CICLO}/`.

---

## Memòries del Departament

Sistema per a generar i compilar les memòries finals de curs dels mòduls adscrits al Departament.
Suporta FP (cicles formatius) i ESO/BAT.

### Estructura

```
memoriaFP/                   # Plantilles i config FP
  ├── memories_INF.json      # Config FP: SMX, DAM, CEIABD, FPBIIO
  ├── memories_SCO.json      # Config FP: APD, EI, IS
  ├── plantilla_memoria.md   # Template Jinja2 per a memòria individual FP
  └── portada_memoria_compilada.md

memoriaESOBAT/               # Plantilles i config ESO/BAT (17 departaments)
  ├── memories_ANGLES.json
  ├── memories_BIOLOGIA_GEOLOGIA.json
  ├── memories_DIBUIX.json
  ├── memories_ECONOMIA.json
  ├── memories_EDUCACIO_FISICA.json
  ├── memories_FILOSOFIA.json
  ├── memories_FISICA_QUIMICA.json
  ├── memories_FRANCES.json
  ├── memories_GEOGRAFIA_HISTORIA.json
  ├── memories_INFORMATICA.json
  ├── memories_LLATI.json
  ├── memories_LLENGUA_CASTELLANA.json
  ├── memories_LLENGUA_VALENCIANA.json
  ├── memories_MATEMATIQUES.json
  ├── memories_MUSICA.json
  ├── memories_RELIGIO.json
  ├── memories_TECNOLOGIA.json
  ├── plantilla_memoria.md   # Template amb opcions ☐
  └── portada_memoria_compilada.md

memories_FP/                 # Plantilles .md individuals FP (gitignored)
  ├── INF/
  │   └── 25_26_1SMXA_AOF_BORRADOR.md
  └── SCO/

memories_ESOBAT/             # Plantilles .md individuals ESO/BAT (gitignored)
  ├── ANGLES/
  ├── MATEMATIQUES/
  └── ... (17 departaments)

PDFS/                        # PDF compilat i report (gitignored)
  └── Memories_INF_IESEPM_25_26.pdf
```

### Patró de noms dels fitxers

**FP**: `{CURS_ACAD}_{CURS}{CICLE}[{GRUP}]_{MODUL}_{ESTAT}.md`
```
25_26_1SMXA_AOF_BORRADOR.md
25_26_1DAM_SEMI_SI_BORRADOR.md
25_26_CEIABD_MIA_BORRADOR.md
```

**ESO/BAT**: `{CURS_ACAD}_{CURS_CODI}[_{GRUP}]_{MATERIA}_{ESTAT}.md`
```
25_26_1ESOA_ANGLES_BORRADOR.md              # 1ESO, grup A
25_26_4ESOD_MATA_BORRADOR.md                # 4ESO, grup D, Matemàtiques A
25_26_3ESO_G1_COMPCOM_BORRADOR.md           # 3ESO, grup G1, Competència Comunicativa
25_26_1BATA_ANGLESI_BORRADOR.md             # 1BAT, grup A
25_26_3PDC_PDC_ANGLES3PDC_BORRADOR.md       # 3PDC, grup PDC
25_26_4ESO_4APLI_TEC4APLI_BORRADOR.md       # 4t ESO Aplicades
```

### Flux de treball

1. **Generar plantilles**: cada mòdul/grup té un fitxer `*_BORRADOR.md`
2. **El docent ompli** el seu fitxer i canvia `_BORRADOR` per `_OK`
3. **Compilar**: l'script llig els `*_OK.md`, genera un PDF amb índex + report de mancances

```bash
# FP: generar les plantilles per a INF
make FAMILIA=INF generar-plantilles-memoria

# FP: compilar memòries completades
make FAMILIA=INF compilar-memories

# ESO/BAT: tot el procés per a ANGLES
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories

# ESO/BAT: només compilar
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES compila-memories

# Tots els departaments ESO/BAT de cop
make genera-tots-esobat                         # generar plantilles
make report-tots-esobat                         # report (sense compilar)
make compila-tots-esobat                        # compilar tots

# Totes les famílies FP de cop
make genera-tots-fp                             # generar plantilles
make report-tots-fp                             # report
make compila-tots-fp                            # compilar
```

### Via Docker wrapper

```sh
# FP
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM FAMILIA=INF memories"

# ESO/BAT (un departament)
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES compila-memories"

# ESO/BAT (tots els departaments)
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT genera-tots-esobat"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT compila-tots-esobat"

# FP (INF + SCO)
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM genera-tots-fp"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM compila-tots-fp"
```

### Report de l'estat de les memòries

El report es genera a `PDFS/0_YYYYMMDD_hhmm_report_memories_{ESOBAT|FP}/{FAMILIA}.txt` i detecta:

| Detecció | Descripció |
|----------|------------|
| **BORRADOR** | Mòduls pendents de completar (fitxer `_BORRADOR.md`) |
| **FALTA** | No hi ha cap fitxer `.md` per a eixa matèria/grup |
| **DUPLICAT** | Existeixen `_OK.md` i `_BORRADOR.md` per al mateix mòdul |
| **INCOMPLET** | Fitxer `_OK.md` amb `[###]` pendents o estadístiques inconsistents |
| **ZERO_STATS** | Aprovats=0 i suspensos=0 (dades no omplides) |
| **CHECKBOX_FORMAT** | Caselles marcades amb espais de més: `[ x ]`, `[x ]` en lloc de `[x]` |
| **SENSE_SUFIX** | Fitxer sense `_OK.md` ni `_BORRADOR.md` |
| **BORR_TRUNCAT** | Fitxer acaba en `_BORR.md` en lloc de `_BORRADOR.md` |
| **Stats inc.** | aprovats+suspensos > avaluats, total > final, avaluats > final, final > inici |

El report inclou al final una **llegenda** amb tots estos codis i el seu significat (llegible des de `tools/report_legend.txt`).

---

## Descripción de las utilidades

En la carpeta ~/tools~ podemos encontrar una serie de utilidades que se ha desarrollado para la generación de los diferentes
Markdowns y las hojas de cálculo.

También hay pequeñas utilidades (`tricky-tools`) que se han utilizado para ir construyendo los diferentes JSON que definen los
datos de los Ciclos Formativos.

#### `tools/preparar_excel.py`

Convierte el Excel autogenerado (`plantilles_{FAMILIA}_{CICLO}/libro_{CICLO}.xlsx`) a su versión para `excels_{FAMILIA}/`,
renombrando automáticamente las hojas (de nombre completo a códigos cortos como `SI`, `BBDD`, `PRG`, etc.).

```sh
python3 tools/preparar_excel.py -c DAM -f INF
python3 tools/preparar_excel.py -c SMX -f INF
python3 tools/preparar_excel.py -c APD -f SCO
```

Opciones: `-i` para especificar un Excel de entrada diferente, `--no-backup` para no crear respaldo.

#### `tools/analizar_json.py`

Analiza todos los archivos JSON de los ciclos y genera un reporte con los campos
faltantes (ObjetivosGenerales, CompetenciasTitulo, ImportanciaCompetencias, etc.).

Se ejecuta automáticamente al final de `make todos`/`make todos-inf`/`make todos-sco`,
o manualmente:

```sh
make report
# o directamente:
python3 tools/analizar_json.py
```

El reporte se guarda en `PDFS/reporte_analisis.txt`.

#### `tools/generar_plantilles_memoria.py`

Genera les plantilles Markdown de les memòries del Departament a partir del fitxer de configuració `memoria_INF/config_memories.json` i la plantilla Jinja2 `memoria/plantilla_memoria.md`.

```sh
make generar-plantilles-memoria
```

Les plantilles es generen a `memories_md/` amb el patró `{CURS}_{CICLE}[_{GRUP}]_{MODUL}_BORRADOR.md`.

#### `tools/compilar_memories.py`

Compila les memòries completades (`*_OK.md`) en un únic PDF amb índex, i genera un report de l'estat de totes les memòries.

```sh
make compilar-memories
```

El PDF es genera a `PDFS/Memories_{FAMILIA}_{CENTRE}_{CURS}.pdf` i el report a `PDFS/0_YYYYMMDD_hhmm_report_memories_{ESOBAT|FP}/{FAMILIA}.txt`.

Detecta:
- Mòduls en estat **BORRADOR** (pendents de completar)
- Mòduls **FALTA** (no hi ha fitxer ni BORRADOR ni OK)
- Mòduls **DUPLICAT** (OK i BORRADOR per al mateix mòdul)
- Mòduls **OK** que encara contenen marcadors `[###]` o `[...]`
- Caselles `[x]` amb format incorrecte (`[ x ]`, `[x ]`, etc.)
- Estadístiques inconsistents (sumes que no quadren)
- El report inclou llegenda explicativa al final

**Gràfic resum**: Al final del PDF s'inserta un gràfic de barres apilades en pàgina apaisada que ocupa l'ample complet (`width=1.0\linewidth`) amb `\newgeometry{top=10mm, bottom=10mm}` abans del landscape per a maximitzar l'espai horitzontal, centrat verticalment amb `\vspace*{\fill}`. Figsize: `max(10, num_bars*1.2), 5` (ample per defecte per a evitar gràfics massa alts amb pocs mòduls). Usa path absolut en `\includegraphics{}` per a evitar errors de lualatex. Funciona tant per a FP com per a ESO/BAT. Quan totes les estadístiques contenen `[###]`, mostra l'etiqueta "No hi ha dades completes".

#### `tools/report_memories.py`

Genera només el report de l'estat de les memòries (sense compilar el PDF). Útil per a una verificació ràpida.

```sh
make report-memories
```

El report es guarda a `PDFS/0_YYYYMMDD_hhmm_report_memories_{ESOBAT|FP}/{FAMILIA}.txt` amb la mateixa informació que `compilar-memories` però sense demanar confirmació ni generar PDF.

#### `tools/json2optatives.py`

Genera l'Excel compartit (`optatives/libro_optatives.xlsx`) i les PDs (`optatives/plantilles/PD_*_BORRADOR.md`) a partir del JSON `optatives/optatives.json`.

```sh
make generar-plantilles-optatives
```

Les PDs es generen amb Jinja2 a partir de la plantilla `templates/PCCF_PD_Plantilla_MODULO_OPTATIVA.md`. No sobreescriu PDs existents (BORRADOR/OK).

#### `tools/copy_optatives_pd.py`

Copía les PDs dels mòduls optatius des de `optatives/plantilles/` cap al directori temporal de compilació d'un cicle. Utilitzat automàticament per `make compila-pccf-{CICLO}`.

```sh
python3 tools/copy_optatives_pd.py --cicle DAM --familia INF --plantilles-dir plantilles_INF_DAM
```

#### `tools/report_optatives.py`

Genera un report de l'estat de les PDs optatives: fitxers en BORRADOR vs OK, detecció de `[###]` pendents.

```sh
make report-optatives
```

## Construyendo Proyectos en Local

Usando `Makefile` se han preparado una serie de reglas para faciliar la *compilación* a PDF de los diferentes Proyectos
Curriculares de Ciclo Formativo.

Este `Makefile` se utiliza también por parte de las Acciones de GitHub para la **Construcción Automática** de los diferentes proyectos cuando se hacen contribuciones.

Algunos de los `targets` disponibles están listados a continuación, con el propósito de generar los PDFs y las diferentes
hojas de cálculo.

No todos los `targets` tienen las mismas opciones y estan en construcción, así que se no se espera que tengan los mismos
mensajes de salida, ni el mismo formato (colores) ^_^.

### Usage de los targets

Se muestran algunos usages de `targets` a modo de ejemplo, pero lo mejor siempre : *Use the source, Luke!*:

#### Opción 1: Usar el valor por defecto (SENIA):

```bash

# Crea el PDF de PCCF de SMX
make proyecto-smx
# Lo mismo para ASIR, DAM y DAW
make proyecto-asir
make proyecto-dam
make proyecto-daw

```

#### Opción 2: Especificar un centro diferente:

```bash
make CENTRO_EDUCATIVO=MIESCUELA proyecto-smx
make CENTRO_EDUCATIVO='COLEGIO XYZ' proyecto-dam
```

#### Opción 3: Usar en línea de comandos (persistente para la sesión):

```bash
export CENTRO_EDUCATIVO=NUEVOCENTRO
make proyecto-ceiabd
make proyecto-daw
```

#### Opción 4: Pipeline bifàsica (pas a pas):

```bash
# Fase 1: Generar plantilles (PDs + Excel) — mai sobreescriu treball docent
make generar-plantilles-pccf-dam

# Comprovar l'estat: què falta omplir, què està OK
make report-pccf-dam

# Fase 2: Compilar PDFs (PCCF + Programaciones)
make compila-pccf-dam
```

### Opción 5: Ver ayuda:

```bash
make help
```

```bash
Targets disponibles:
  PCCF (bifàsica):
    generar-plantilles-pccf-dam  Fase 1: generar PDs + Excel a plantilles_*/
    report-pccf-dam              Report: BORRADOR/OK + [###] + Excel coherència
    compila-pccf-dam             Fase 2: compilar PCCF + Programaciones PDF
    proyecto-dam                 Fases 1+2 en un sol pas
  Optatius compartits:
    generar-plantilles-optatives  Generar Excel + PDs per a optatives a optatives/
    report-optatives              Report d'estat de les PDs optatives
  Familia INF:
    proyecto-smx       Generar proyecto para SMX
    proyecto-asir      Generar proyecto para ASIR
    proyecto-daw       Generar proyecto para DAW
    proyecto-dam       Generar proyecto para DAM
    proyecto-ceiabd    Generar proyecto para CEIABD
    proyecto-fpbiio    Generar proyecto para FPBIIO
  Familia SCO:
    proyecto-apd       Generar proyecto para APD
    proyecto-ei        Generar proyecto para EI
    proyecto-is        Generar proyecto para IS
  Conjunto:
    todos              Generar todos los proyectos
    todos-inf          Generar todos los proyectos INF
    todos-sco          Generar todos los proyectos SCO
  Memòries:
    generar-plantilles-memoria  Generar plantilles MD de memòria (també: genera-memories)
    genera-memories             Alias de generar-plantilles-memoria
    compilar-memories           Compilar memòries OK en PDF + report
    report-memories             Report de l'estat de les memòries (sense PDF)
    compila-memories            Report + compila tot (OK i BORRADOR)
    memories                    Tot el procés (genera + compila)
    (per defecte FAMILIA=INF, BASE_DIR=memoriaFP)
    (per a ESO/BAT: make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES ...)
    genera-tots-esobat          Generar plantilles de TOTS els departaments ESO/BAT
    report-tots-esobat          Report de TOTS els departaments ESO/BAT
    compila-tots-esobat         Compilar memòries de TOTS els departaments ESO/BAT
    genera-tots-fp              Generar plantilles de TOTES les famílies FP (INF + SCO)
    report-tots-fp              Report de TOTES les famílies FP
    compila-tots-fp             Compilar memòries de TOTES les famílies FP
    clean              Limpiar archivos generados
    files              Crear estructura de directorios
    dependences        Instalar dependencias

Ejemplos:
  make proyecto-smx                 # Usa 'SENIA' por defecto
  make proyecto-asir                # Genera solo ASIR
  make todos                        # Genera todos los ciclos
  make generar-plantilles-pccf-dam  # Fase 1: plantilles (PDs + Excel)
  make report-pccf-dam              # Report d'estat
  make compila-pccf-dam             # Fase 2: PDFs
  make report-tots-pccf             # Report de TOTS els cicles
  make generar-plantilles-optatives # Optatius: Excel + PDs compartides
  make report-optatives             # Report d'estat dels optatius
  make generar-plantilles-memoria   # Genera plantilles de memòria
  make compilar-memories            # Compila memòries en PDF
  make CENTRO_EDUCATIVO=MIESCUELA proyecto-dam
  make CENTRO_EDUCATIVO=IESEPM todos
  make genera-tots-esobat           # Plantilles de TOTS els departaments ESO/BAT
```

## Dependencias

Para instalar las dependencias necesarias, se adjunta una serie de comandos par su ejecución en sistemas basados en Debian.

Estas dependencias también están definidas en el Makefile para ser instalados dentro del entorno
de ~chroot~ de las GitHub Actions.

```shell
sudo apt install make pandoc \
	     texlive-extra-utils \
		 texlive-lang-spanish \
		 texlive-latex-extra \
		 texlive-fonts-extra \
		 libreoffice \
         poppler-utils

sudo apt install python3-jinja2 \
		 python3-box \
         python3-numpy \
         python-openpyxl-doc \
         python-pandas-doc \
         python3-pandas

```

## Contenedor

Para simplificar el trabajo y la gestión de dependencias en diferentes equipos existen una serie de ficheros para crear un contenedor Docker y lanzar los scripts desde allí:

```sh
contenedor_build.sh
contenedor_lanza.sh
contenedor_limpia.sh
docker-compose.yml
Dockerfile
```

Para lanzar (diferentes modos):

```bash
# Sesión interactiva con bash (modo por defecto)
./contenedor_lanza.sh

# Ejecutar un comando específico y salir
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM proyecto-daw"

# Iniciar en segundo plano
./contenedor_lanza.sh -d

# Acceder con un comando específico
./contenedor_lanza.sh --command "ls -la"

# Mostrar ayuda
./contenedor_lanza.sh --help
```
