\newpage

# Programación didáctica: Módulo {{ modulo.nombre }}

## Datos identificativos y contextualización del módulo. 

Es un módulo de {{ modulo.horas }} horas que se imparte en el Curso de Especialización de Recursos y Servicios en la Nube.

Tiene una correspondéncia en Créditos de {{ modulo.creditos}}.


{% if modulo.UnidadesCompetenciaAcreditadas|count > 0 %}

## Relación entre los estándares de competencia y los módulos del ciclo formativo

| Unidad de Competencia | Descripción |
|-----------------------|-------------|{% for uca in modulo.UnidadesCompetenciaAcreditadas %}
| {{ uca }} | {{ modulo.UnidadesCompetenciaAcreditadas[uca] }} |{% endfor %}
|<img width=200/>|<img width=500/>|

{% endif %}

## Resultados de Aprendizaje

Los **Resultados de Aprendizaje** relativos al módulo de {{modulo.nombre}} son:

|Código| Resultado de Aprendizaje |
|------|--------------------------|{% for ra in modulo.ResultadosAprendizaje %}
| {{ ra }} | {{ modulo.ResultadosAprendizaje[ra].Resultado }} |{% endfor %}
|<img width=200/>|<img width=500/>|

{% if modulo.ObjetivosGenerales|count > 0 %}

## Objetivos Generales 

La formación del módulo contribuye a alcanzar los *Objetivos Generales del Curso* siguientes:

| Obj| Objetivo General del Ciclo |
|----|----------------------------|{% for obj in modulo.ObjetivosGenerales %}
| {{ obj }} | {{ modulo.OG[obj] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}

{% if modulo.CompetenciasTitulo|count > 0 %}

## Competencias del Título 

La formación del módulo contribuye a alcanzar las *Competencias del Título* siguientes:

| Obj| Competencia del Título |
|----|----------------------------|{% for com in modulo.CompetenciasTitulo %}
| {{ com }} | {{ modulo.CPSS[com] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}

## Secuenciación de las Unidades de Programación. 

A RELLENAR POR DOCENTE

Se propone esta tabla

| Número | Título                    | Inicio    | Fin       |
|--------|---------------------------|-----------|-----------|
| 01     | UP01: Vim en la Nube  | 08/09/2025| 10/10/2025|
| 02     | UP02: Más allá de :wq en la Nube     | 11/10/2025| 21/10/2025|
| 03     | UP03: El poder de RegEx en la Nube  | 11/10/2025| 21/10/2025|
| 04     | UP04: El camino del zen en la Nube  | 22/10/2025| 20/12/2025|

## Metodología del proceso de enseñanza-aprendizaje

La metodología didáctica adoptada en esta programación se encuentra alineada con los principios y directrices establecidos en el Proyecto Curricular del Curso de Especialización (PCCE), elaborado de forma colaborativa por el equipo docente del curso. Este documento marco recoge los enfoques metodológicos comunes que guían el proceso de enseñanza-aprendizaje en todos los módulos del curso, promoviendo una formación integral, activa y contextualizada del alumnado.

Se apuesta por metodologías activas, centradas en el estudiante, que fomentan el aprendizaje significativo, el trabajo cooperativo, la resolución de problemas y la aplicación práctica de los contenidos en contextos reales o simulados. Asimismo, se integran estrategias que favorecen la autonomía, la reflexión crítica y el desarrollo de competencias profesionales, personales y sociales.

Cualquier concreción metodológica específica, adaptada a las características del módulo o del grupo de estudiantes, se desarrollará en el diseño de las **Situaciones de Aprendizaje**, donde se detallarán las actividades, recursos y dinámicas concretas que se llevarán a cabo.

## Recursos

Los recursos didácticos utilizados en este módulo se seleccionan en coherencia con los criterios establecidos en el Proyecto Curricular del Curso de Especialización (PCCE), que define los medios y herramientas comunes para facilitar el desarrollo de las competencias profesionales, personales y sociales del alumnado.

Se contempla el uso de recursos variados, tanto materiales como digitales, que favorecen un aprendizaje activo, contextualizado y accesible. Entre ellos se incluyen: equipamiento técnico específico del módulo, herramientas TIC, plataformas educativas, materiales audiovisuales, documentación profesional actualizada y recursos adaptados a las necesidades del grupo.

La concreción de los recursos específicos que se emplearán en cada unidad didáctica o actividad se detallará en las correspondientes **Situaciones de Aprendizaje**, en función de los objetivos, contenidos y metodologías aplicadas.

## Uso de espacios y equipamientos. 

El uso de los espacios y equipamientos necesarios para el desarrollo de este módulo se organiza conforme a lo establecido en el Proyecto Curricular del Curso de Especialización (PCCE), donde se recogen los criterios comunes para la distribución, aprovechamiento y adecuación de los entornos formativos.

Se prioriza la utilización de espacios que reproduzcan contextos profesionales reales o simulados, favoreciendo así el aprendizaje significativo y la adquisición de competencias en condiciones similares a las del entorno laboral. Asimismo, se garantiza el acceso a los equipamientos técnicos y tecnológicos adecuados, asegurando su disponibilidad, mantenimiento y uso responsable, cumpliendo la normativa del Centro y de la Conselleria.

Las especificidades sobre el uso de espacios y equipamientos en cada actividad concreta se detallarán en las **Situaciones de Aprendizaje**, adaptándose a las necesidades del alumnado y a los objetivos de cada propuesta didáctica.

## Medidas de atención a la diversidad. 

Las medidas de atención a la diversidad contempladas en esta programación se fundamentan en los principios recogidos en el Proyecto Curricular del Curso de Especialización (PCCE), que establece un marco común para garantizar una respuesta educativa inclusiva, equitativa y adaptada a las características del alumnado.

Se parte del reconocimiento de la diversidad como un valor y una oportunidad para el aprendizaje, promoviendo estrategias que favorezcan la participación, la motivación y el progreso de todos los estudiantes. Entre las medidas generales se incluyen la flexibilización metodológica, la adaptación de recursos, el uso de apoyos personalizados y la atención a distintos ritmos y estilos de aprendizaje.

Las adaptaciones específicas, tanto metodológicas como organizativas, se concretarán en las **Situaciones de Aprendizaje**, donde se detallarán las actuaciones necesarias para atender a las necesidades individuales del alumnado, siempre en coordinación con los servicios de orientación y el equipo docente.

## Evaluación del aprendizaje. 

@@@PCCF_200_ProcesoDeEvaluacion.md

### Tipos de evaluación 

La evaluación de un módulo será realizada por el profesor titular del correspondiente módulo profesional y, en su caso, teniendo en cuenta el informe de la empresa tras la Formación en Empresa.

Durante el curso se llevarán a cabo varias sesiones de evaluación, que serán las siguientes:

- **Parcial**: se realizarán un mínimo de dos por curso (primer y segundo trimestre). Incluyen calificaciones numéricas orientativas sobre la progresión del alumnado.
- **Formación en Empresa (FE)**: antes del inicio de la FE. Evalúa la situación e idoneidad del alumnado para realizar esta fase.
- **Ordinaria**: al final del curso. Se decide la promoción y titulación del alumnado.
- **Extraordinaria**: destinada a la recuperación de módulos no superados.

En cada sesión de evaluación, el tutor elaborará un acta que refleje los acuerdos y decisiones adoptadas de forma colegiada con el equipo docente.

### Calificaciones 

El alumnado podrá obtener las siguientes calificaciones:

* **Escala del 1 al 10 sin decimales**: el redondeo o truncamiento de los decimales será a discreción del profesor que evalúa el módulo.
* **Resultados de Aprendizaje (RA) en empresa**: serán calificados por la empresa como **“superado”** o **“no superado”**. En caso de “no superado”, el módulo podrá ser calificado por el profesor como **aprobado** o **suspenso**. Si se califica como suspenso, el informe deberá reflejar los RA en empresa que han sido superados y los que no.
* **Nota final del Curso**: se calculará como la **media aritmética** de los módulos, excluyendo las convalidaciones sin nota.
* **Mención honorífica**: se otorga a quienes obtienen un **10 en un módulo**, con un máximo del **10% del grupo**.
* **Matrícula de honor**: se concede a quienes obtienen una **nota final de Ciclo igual o superior a 9** teniendo en cuenta el límite establecido por la normativa.

- **Calificaciones parciales**: cada docente incluirá un comentario explicativo sobre la calificación parcial obtenida por el alumnado, indicando que esta es **provisional** y tiene carácter **orientativo** respecto al estado del proceso de aprendizaje.

La ponderación de cada Resultado de Aprendizaje se indica en el Esquema General.

!!! OBLIGATORIO ]: A RELLENAR POR EL DOCENTE -> Cálculo de la calificación.

### Evaluación por RA

Cada módulo se divide en **Unidades de Programación** que agrupan Resultados de Aprendizaje y sus criterios de evaluación. A cada RA se le asigna un **peso evaluativo** y una **carga horaria** proporcional. 

Las Unidades de Programación/Situaciones de Aprendizaje deben: 

- Estar alineadas con las competencias del curso de especialización. 
- Incluir actividades significativas y metodologías activas. 
- Incorporar competencias para la empleabilidad (trabajo en equipo, comunicación, etc.). 
- Incluir los contenidos necesarios alineados con los CE para conseguir los RA. 

El equipo docente se compromente a facilitar en Aules un seguimiento del progreso de los RA por parte del alumnado.

### Formación en empresa 

En el caso de que el alumnado no supere los Resultados de Aprendizaje, se elaborará un programa educativo especifico
para la recuperación de los RA no superados. Este programa se llevará a cabo en el periodo que el alumnado debería estar realizando la Formación en Empresa y **antes de la Convocatoria Ordinaria**.

Cuando un estudiante de **no se incorpore a Formación en Empresa (FE)** por causa 
justificada y acreditada, permanecerá en el centro educativo realizando actividades complementarias, 
extraescolares y/o de refuerzo que le permitan acercarse al ámbito socio-laboral. 

La fase de Formación en Empresa podrá acogerse a las condiciones que cada empresa 
tenga establecidas con respecto al **teletrabajo**, de acuerdo con la normativa reguladora del mismo.

### Superación de los RA's asociados a la FE

Respecto a la evaluación, el tutor recabará el parecer de los instructores, que compartirá con los profesores del equipo docente. 

Además, se reservarán unos días a final de curso, finalizado el período de Formación en Empresa, para que el alumnado muestre el trabajo realizado en la empresa al profesorado, y pueda responder a las cuestiones que se le planteen desde cada módulo. Permitiendo una vía para que quede constancia de que cada estudiante ha adquirido todos los conocimientos requeridos en los diversos módulos. 

Para superar un RA dualizado se debe **superar tanto la parte impartida en el centro como la realizada en la empresa**. Se considerará *superado cuando la nota de cada una de las partes sea igual o mayor a 5*.


!!! OBLIGATORIO ]: A RELLENAR POR EL DOCENTE -> Cálculo de la calificación de un RA Dualizado.

### Recuperación

Para el alumnado que **no haya superado algún módulo o RA** se establecerá un **programa de recuperación individual** que se diseñará de forma diferenciada según periodos:

Los RA o módulos no superados en la **evaluación ordinaria**: se podrán recuperar en la **convocatoria extraordinaria** .

### Convocatoria Ordinaria

1. Todo el alumnado tiene derecho a una Convocatoria Ordinaria, en el caso de que el alumnado haya superado todos los RAs durante la *evaluación continua*, se establecerá su calificación como la de la Convocatoria Ordinaria.
2. Si hay RAs **no superados** durante la *evaluación continua*, el alumnado tiene derecho a una prueba que incluya dichos RAs con el objetivo de comprobar que ha adquirido los Resultados de Aprendizaje descritos en el Módulo. Esta prueba se ajustará al calendario propuesto por el centro.

### Convocatoria Extraordinaria

La convocatoria extraordinaria del módulo se ajustará lo decidido de manera conjunta y ha sido 
descrito en el Proyecto Curricular del Curso de Especialización.

## Actividades complementarias y extraescolares. 

A RELLENAR POR DOCENTE

## Criterios y procedimientos para la evaluación del desarrollo de la programación y de la práctica docente. 

La evaluación del propio proceso de *enseñanza-aprendizaje* contempladas en esta programación se fundamentan en los principios recogidos en el Proyecto Curricular del Curso de Especialización (PCCE), que establece un marco común para garantizar una respuesta educativa inclusiva, equitativa y adaptada a las características del alumnado.

## Esquema General de {{modulo.nombre}}

NOTA : Aquí se generará de manera automática la tabla a partir del Excel compartido con los RA, CE y Horas Asignadas. 

NO RELLENAR.
