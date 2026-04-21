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

---

## Programaciones Didácticas

### Creación del fichero

Las Programaciones Didácticas de cada módulo se construyen en varias "etapas". 

Por un lado tenemos la generación 
automática ficheros a partir de las plantillas de los diferentes Ciclos Formativos que se generan en `./temp/` y 
que son usadas por el *compilador* **Pandoc** en la siguiente etapa.

Y por otra parte podemos crear un fichero con el mismo nombre que el que se genera automáticamente, pero 
ya en la carpeta del Ciclo correspondiente (`src_ASIR/`,`src_SMX/`,`src_DAW/`,`src_DAM/`). En ese caso, el constructor
de las programaciones didácticas no generará el fichero automático y usará el que el/la docente haya establecido.

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

Estos documentos se generan en la carpeta `src_{FAMILIA}_{CICLO}/` y se integran automáticamente en el PCCF final.

---

## Descripción de las utilidades

En la carpeta ~/tools~ podemos encontrar una serie de utilidades que se ha desarrollado para la generación de los diferentes
Markdowns y las hojas de cálculo.

También hay pequeñas utilidades (`tricky-tools`) que se han utilizado para ir construyendo los diferentes JSON que definen los
datos de los Ciclos Formativos.

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

### Opción 4: Ver ayuda:

```bash
make help
```

```bash
Targets disponibles:
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
    clean              Limpiar archivos generados
    files              Crear estructura de directorios
    dependences        Instalar dependencias

Ejemplos:
  make proyecto-smx                 # Usa 'SENIA' por defecto
  make proyecto-asir                # Genera solo ASIR
  make todos                        # Genera todos los ciclos
  make CENTRO_EDUCATIVO=MIESCUELA proyecto-dam
  make CENTRO_EDUCATIVO=IESEPM todos
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
