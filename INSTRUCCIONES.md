# Instruccions d'us

## Afegir un nou cicle 

### 1. Crear el nou arxiu `rd-xxxx.json`
 
Pots fer servir alguna IA ([DeepSeek.com](https://www.deepseek.com/)) passant-li com a context el `json` d'un altre cicle i el `pdf` amb el currículum per a que emplene els valors del `json` però no alterar les claus. Inclús pots demanar que traduisca els valors al Valencià.
 
#### 1.1 Importància de les competències
 
Per a que la taula de competències (arxiu `PCCF_033_*_ImportanciaCompetencies.md`) mostre el nivell d'importància amb estrelles (★), cal afegir el diccionari `ImportanciaCompetencias` al final del JSON:
 
```json
"ImportanciaCompetencias": {
    "a": 3,
    "b": 2,
    "c": 1
}
```
 
- **3**: ★★★ (Molt important)
- **2**: ★★ (Importància mitja)
- **1**: ★ (Menys important)
 
Si una competència no es troba al diccionari, es mostrarà amb **2 estrelles (★★)** per defecte.

### 2. Generar la plantilla de les PD's per als mòduls del nou cicle

A la carpeta `templates_XXX` (XXX correspon a la família) hem de clonar l'arxiu `PCCF_PD_Plantilla_MODULO_CEIABD.md` i crear un per al nou cicle `PCCF_PD_Plantilla_MODULO_FPBIIO.md`

### 3. Crear estructura de carpeta per al nou cicle `src_INF_FPBIIO`:

Podem clonar la carpeta d'un altre cicle, per exemple `src_INF_CEIABD` i anomenar-la `src_INF_FPBIIO`:

Dins de la carpeta trobarem la següent estructura:

| Ruta i/o fitxer                              | Descripció                                                   |
| -------------------------------------------- | ------------------------------------------------------------ |
| `imgs/FPBIIO_horario.png`                    | Este fitxer hauria de contindre la taula d'hores del cicle per a insertar-lo als documents |
| `PCCF_000_FPBIIO_Portada.md`                 | Plantilla per a la portada del PCCF de FPBIIO.<br />Especificar nom del cicle, centre, curs, portada, etc. |
| `PCCF_001_IdentificacioFPBIIO.md`            | Plantilla per al primer punt del PCCF (Identificació)        |
| `PCCF_006_MarcoNormativoEspecificoFPBIIO.md` | Marc normatiu específic del PCCF de FPBIIO                   |
| `PCCF_110_AdecuacionYArreglo_FPBIIO.md`      | Context socioeconomic i competència general del cicle, el fitxer |
| `PCCF_033_FPBIIO_ImportanciaCompetencies.md`            | Es generarà a la carpeta PDFS originalment, una vegada ens agrade com es genera, el podem moure ací i s'utilitzarà este en lloc de generar un de nou. |
| `PCCF_030_FPBIIO_ContribucioModuls.md`            | Es generarà automàticament. Conté dues taules que mostren quins mòduls contribueixen a desenvolupar cada competència (professionals i d'ocupabilitat). |
| `PCCF_150_OrganizacionDistribucion.md`       | En esta plantilla s'utilitza la imatge de `imgs/FPBIIO_horario.png` |
| `PD_000_FPBIIO_Introduccion.md`              | Plantilla per a la portada de les PD dels mòduls de FPBIIO.<br />Especificar nom del cicle, centre, curs, portada, etc. |

> El nom dels fitxers concrets no importa, però si importa l'ordre en el que es llisten, perquè serà l'ordre en el que es juntaran per a generar el pdf final. Per això és important que per exemple la portada mantinga el nom `PCCF_000_*.md`
>
> A més d'estos fitxers, s'hauran d'afegir tots els que siguen específics d'este cicle. Els arxius comuns es troben a la ruta `src_INF/`. 

### 4. Llançar el projecte per primera vegada per a el nou cicle:

Llançar el make per al projecte del nou cicle:

```sh
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM proyecto-fpbiio"
```

### 5. Resultat final

Si el procés funciona correctament (i no es veu cap error pel mig) vorem al final:

```bash
========================================
  SESIÓN FINALIZADA
========================================
```

I tindrem 3 noves carpetes (o si ja existien s'afegiran a elles els nous arxius):

| Ruta                                    | Descripció                                                   |
| --------------------------------------- | ------------------------------------------------------------ |
| `PDFS/PDs_FPBIIO/`                      | Esta carpeta conté un PDF amb la PD de cadascún dels mòduls  |
| `PDFS/libro_autogenerado_FPBIIO.xlsx`   | Excel genèric generat a partir de la informació del rd-fpbiio.json i que posteriorment utilitzarà cada docent per a ajustar les ponderacions de cada RA i designar els CE o RA que van a FEE. |
| `PDFS/PCCF_IESEPM_FPBIIO.pdf`           | PCCF preeliminar del cicle corresponent en PDF               |
| `PDFS/Programaciones_IESEPM_FPBIIO.pdf` | PDF amb totes les PD's de tots els mòduls del cicle          |
| `PDFS/PCCF_033_FPBIIO_ImportanciaCompetencies.md`       | Sols en cas que l'arxiu no es trobe a la carpeta `src_INF_FPBIIO` |
| `PDFS/PCCF_030_FPBIIO_ContribucioModuls.md`       | Document generat automàticament amb taules de contribució de mòduls a competències |

### 6. Afegir el nou cicle a l'script `pccf_utils.py`

Al final de l'script, fem una còpia del que fa referència a CEIABD:

```python
# CEIABD
if hoja.startswith("Models d"): hoja = "MIA"
if hoja.startswith("Sistemes d"): hoja = "SAA"
if hoja.startswith("Programació d"): hoja = "PIA"
if hoja.startswith("Sistemes de"): hoja = "SBD"
if hoja.startswith("Big Data"): hoja = "BDA"
```

i ho adaptem a FPBIIO, podem mirar les pestanyes de l'excel que s'ha generat en `PDFS/libro_autogenerado_FPBIIO.xlsx` i canviar-ho per les sigles del mòdul:

```python
# FPBIIO
if hoja.startswith("Montatge i manteniment"): hoja = "MME"
if hoja.startswith("Operacions auxiliars"): hoja = "OA"
if hoja.startswith("Ofimàtica"): hoja = "OAD"
if hoja.startswith("Instal·lació i manteniment"): hoja = "IMXTD"
if hoja.startswith("Ciències aplicades 1"): hoja = "CA1"
if hoja.startswith("Ciències aplicades 2"): hoja = "CA2"
if hoja.startswith("Comunicació i societat 1"): hoja = "CS1"
if hoja.startswith("Comunicació i societat 2"): hoja = "CS2"
```

> Important:
>
> Com que els mòduls `Ciències aplicades I` i `Ciències aplicades II` comencen amb les mateixes lletres i es confonen, ho hem solucionat reanomenant el mòdul al rd-fpbiio per `Ciències aplicades 1` i `Ciències aplicades 2` respectivament. El mateix per als mòduls de `Comunicació i societat I i II`.

### Taula de correspondència de sigles per mòdul

A continuació es detalla la correspondència entre el nom complet del mòdul (com s'autogenera la pestanya de l'excel) i les sigles curtes que cal establir com a nom de la pestanya perquè el script el reconega com a revisat i s'incloga al Plan de Formación:

| Cicle / Família | Nom del mòdul a l'Excel | Sigles de la pestanya |
| :--- | :--- | :---: |
| **Comuns / Optatives** | Llenguatges de marques i sistemes de gestió d'informació | **LM** |
| | Sostenibilitat aplicada al sistema productiu | **SOS** |
| | Itinerari personal per a l'ocupabilitat I | **IPO1** |
| | Itinerari personal per a l'ocupabilitat II | **IPO2** |
| | Digitalització aplicada als sectors productius | **DIG** |
| | Anglés Professional | **ANG** |
| | Anglés oral en entorns professionals | **AOEP** |
| | Comunicació professional | **COM** |
| | Projecte intermodular | **PI** |
| | Introducció al Núvol Públic | **NVL** |
| **SMX** | Muntatge i manteniment d'equips | **MME** |
| | Sistemes operatius monopast | **SOM** |
| | Aplicacions ofimàtiques | **AOF** |
| | Sistemes operatius en xarxa | **SOX** |
| | Seguretat informàtica | **SIN** |
| | Serveis en xarxa | **SEX** |
| | Aplicacions web | **AW** |
| | Xarxes locals | **XL** |
| **DAM / DAW** | Entorns de desenvolupament | **ED** |
| | Sistemes Informàtics | **SI** |
| | Bases de Dades | **BBDD** |
| | Programació | **PRG** |
| **DAM** | Desenvolupament d'interfícies | **DI** |
| | Accés a dades | **AD** |
| | Programació de serveis i processos | **PSP** |
| | Programació multimèdia i dispositius mòbils | **PMDM** |
| | Sistemes de gestió empresarial | **SGE** |
| **CEIABD** | Models d'intel·ligència artificial | **MIA** |
| | Sistemes d'aprenentatge automàtic | **SAA** |
| | Programació d'intel·ligència artificial | **PIA** |
| | Sistemes de big data | **SBD** |
| | Big Data aplicat | **BDA** |
| **FPBIIO** | Montatge i manteniment de sistemes i components | **MMEB** |
| | Operacions auxiliars per a la configuració i l'explotació | **OA** |
| | Ofimàtica i arxiu de documents | **OAD** |
| | Instal·lació i manteniment de xarxes per a la transmissió | **IMXTD** |
| | Ciències aplicades I / Ciències aplicades 1 | **CA1** |
| | Ciències aplicades II / Ciències aplicades 2 | **CA2** |
| | Comunicació i societat I / Comunicació i societat 1 | **CS1** |
| | Comunicació i societat II / Comunicació i societat 2 | **CS2** |
| **APD** | Organització de l'atenció a les persones en situació de dependència | **OAPD** |
| | Destreses socials | **DS** |
| | Característiques i necessitats de les persones en situació de dependència | **CNP** |
| | Atenció i suport psicosocial | **ASP** |
| | Suport a la comunicació | **SC** |
| | Suport domiciliari | **SD** |
| | Atenció sanitària | **AS** |
| | Atenció higiènica | **AH** |
| | Teleassistència | **TEL** |
| | Primers auxilis | **PA** |
| **EI** | Didàctica de l'educació infantil | **DEI** |
| | Autonomia personal i salut infantil | **APSI** |
| | El joc infantil i la seua metodologia | **JOC** |
| | Expressió i comunicació | **EC** |
| | Desenvolupament cognitiu i motor | **DCM** |
| | Desenvolupament socioafectiu | **DSA** |
| | Habilitats socials | **HHSS** |
| | Intervenció amb famílies i atenció a menors en risc social | **IFAM** |
| | Projecte d'atenció a la infància | **PAI** |
| **IS** | Context de la intervenció social | **CIS** |
| | Inserció sociolaboral | **ISL** |
| | Atenció a les unitats de convivència | **AUC** |
| | Mediació comunitària | **MC** |
| | Suport a la intervenció educativa | **SIE** |
| | Promoció de l'autonomia personal | **PAP** |
| | Sistemes augmentatius i alternatius de la comunicació | **SAAC** |
| | Metodologia de la intervenció social | **MIS** |

## Procediment per a generar correctament les PD's i PCCF de cada cicle

### 1. Revisar el contingut de l'excel

Una vegada generat l'excel (`make proyecto-FPBIIO`), el trobarem a `PDFS/libro_autogenerado_FPBIIO.xlsx`. Cada docent ha de revisar el contingut per al seu mòdul:

1. A la columna `C` s'indicarà el pes de cada RA en percentatge (tots junts hauran de sumar 100%)
2. *La columna `D` no tinc clar per a que s'utilitza*
3. A la columna `F` s'han d'indicar les hores destinades a cada CE (l'excel sumarà el total per a cada RA, o bé indicar directament el total de RA i no especificar res a les hores del CE)
4. A la columna `H` s'indicarà "si", "SI" o "X" si el CE és un requeriment per a la FEE
5. A la columna `I` S'indicarà les hores destinades de cada CE/RA a les FEE (en la fila 5 de la mateixa columna apareixerà el total d'hores enviades a DUAL). Esta columna és important perquè generarà l'arxiu: `PCCF_222_PlanFormativo.md` generant una taula en markdown per a cada mòdul, indicant els RA que tenen hores assignades a la FEE.
6. A la columna `J` s'indicaran els continguts de cada RA

### 2. Preparar l'excel per al seu ús

Una vegada tots els docents han completat la revisió, cal renombrar les pestanyes de cada mòdul a les sigles curtes corresponents (segons la taula de correspondència) i moure l'excel a la carpeta `excels_{FAMILIA}/`. Per a fer-ho automàticament, utilitza el script `tools/preparar_excel.py`:

```sh
# Per a DAM (família INF)
python3 tools/preparar_excel.py -c DAM -f INF

# Per a SMX (família INF)
python3 tools/preparar_excel.py -c SMX -f INF

# Per a APD (família SCO)
python3 tools/preparar_excel.py -c APD -f SCO
```

El script:
1. Llig l'excel des de `PDFS/libro_autogenerado_{CICLO}.xlsx` (o des d'una ruta personalitzada amb `-i`)
2. Renombra automàticament cada pestanya a les sigles curtes
3. El guarda a `excels_{FAMILIA}/libro_{CICLO}.xlsx`
4. Crea una còpia de seguretat del destí si ja existia

> **Nota:** Si alguna pestanya no es renombra (perquè el nom no coincideix amb cap patró), caldrà afegir-la a `tools/pccf_utils.py` a la funció `get_hoja_label()`.

### Generació de PD's:

La generació final de les PD's es basa en el contingut de la carpeta `src_CICLE` corresponent al cicle, tots els fitxers de dita carpeta (excepte els de les PCCF) es junten en una carpeta (temp) que després s'uniran en un únic document PDF per cada PD, i un altre que juntarà totes les PD's.

Si a la carpeta `src_FAMILIA_MODUL` trobem el fitxer corresponent a la PD del mòdul s'utilitzarà per a la generació del PDF, sino s'utilitzarà el genèric de la carpeta `temp_CICLE`.

## Memòries del Departament

Sistema per a generar i compilar les memòries finals de curs dels mòduls adscrits al departament. Suporta tant FP (cicles formatius) com ESO/BAT.

### Estructura

```
memoriaFP/                 # Plantilles i config per a FP
  ├── memories_*.json       # Config per departament (ANGLES, FOL, INF, SCO)
  ├── plantilla_memoria.md  # Template Jinja2 per a memòria individual FP
  ├── plantilla_annex.md
  └── portada*.md

memoriaESOBAT/             # Plantilles i config per a ESO/BAT
  ├── memories_*.json       # Config per departament (ANGLES, MATEMATIQUES...)
  ├── plantilla_memoria.md  # Template Jinja2 (amb opcions ☐)
  ├── plantilla_annex.md
  └── portada*.md

memories_FP/               # Plantilles .md generades per a FP (gitignored)
  ├── INF/
  ├── SCO/
  ├── FOL/
  └── ANGLES/

memories_ESOBAT/           # Plantilles .md generades per a ESO/BAT (gitignored)
  ├── ANGLES/
  └── MATEMATIQUES/

PDFS/                      # PDF compilats i reports (gitignored)
```

### Patró de noms dels fitxers

**FP**: `{CURS_ACAD}_{CURS}{CICLE}[{GRUP}]_{MODUL}_{ESTAT}.md`
```
25_26_1SMXA_AOF_BORRADOR.md
25_26_1DAM_SEMI_SI_BORRADOR.md
25_26_CEIABD_MIA_BORRADOR.md
```

**ESO/BAT**: `{CURS_ACAD}_{CURS}{ETAPA}[{GRUP}]_{MATERIA}_{ESTAT}.md`
```
25_26_1ESOA_ANGLES_BORRADOR.md
25_26_4ESOD_MATA_BORRADOR.md
25_26_1BATA_ANGLESI_BORRADOR.md
```

### Ús

**FP** (per defecte):
```sh
make FAMILIA=INF generar-plantilles-memoria
make FAMILIA=INF compila-memories
make FAMILIA=INF report-memories
```

**ESO/BAT** (cal `BASE_DIR=memoriaESOBAT`):

Via make (recomanat):
```sh
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES generar-plantilles-memoria
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES compila-memories
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES report-memories
make BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories                     # tot el procés
```

Via Docker:
```sh
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES memories"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES compila-memories"
./contenedor_lanza.sh "make CENTRO_EDUCATIVO=IESEPM BASE_DIR=memoriaESOBAT FAMILIA=ANGLES report-memories"
```

`BASE_DIR=memoriaFP` (per defecte) o `BASE_DIR=memoriaESOBAT`.

### Generació del PCCF:

La generació final del PCCF es basa en el contingut de les carpetes `src` i `src_FAMILIA_CICLE` corresponent al cicle, tots els fitxers de dites carpetes (excepte els de les PD) es junten en una carpeta (temp) que després s'uniran en un únic document PDF.