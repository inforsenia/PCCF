# PCCF

Proyectos Curriculares de la Familía de Informática del IES La Sénia - Paiporta.

En este Repositorio podrás encontrar las fuentes en formato Markdown de los diferentes
Proyectos Curriculares de la Familia de Informática, así como la posibilidad de generar
las diferentes hojas de cálculo de las Programaciones Didácticas de los Módulos
a partir de los contenidos del BOE que se leen desde diferentes JSON.

Se trata de un proyecto en desarrollo, que contiene toda la información de los 
diferentes ciclos.

## Ciclos Formativos

| Siglas | Nombre Completo | Nivel |
|--------|-----------------|-------|
| SMX    | Sistemas Microinformáticos y Redes | Grado Medio |
| DAW 	 | Desarrollo de Aplicaciones Web | Grado Superior |
| DAM    | Desarrollo de Aplicaciones Multiplataforma | Grado Superior |
| ASIR   | Admnistración de Sistemas Informáticos y Redes | Grado Superior |

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

Se han añadido las listas de las Competencias Profesionales y Sociales.

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

```shell
# Crea el PDF de PCCF de SMX y lo abre mediante xdg-open.
make proyecto-smx
# Lo mismo para ASIR, DAM y DAW
make proyecto-asir
make proyecto-dam
make proyecto-daw

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
		 texlive-fonts-extra

sudo apt install python3-jinja2 \
		 python3-box
```
