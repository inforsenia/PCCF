\newpage

# Programación didáctica: Módulo {{ modulo.nombre }}

## Datos identificativos y contextualización del módulo. 

Es un módulo de {{ modulo.horas }} horas que se imparte en el Ciclo de Grado Superior de 
Técnico en Desarrollo de Aplicaciones Multiplataforma.

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

La formación del módulo contribuye a alcanzar los *Objetivos Generales del Ciclo* siguientes:

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
| 01     | UP01: Introducción a vim  | 08/09/2025| 10/10/2025|
| 02     | UP02: Más allá de :wq     | 11/10/2025| 21/10/2025|
| 03     | UP03: El poder de RegEx   | 11/10/2025| 21/10/2025|
| 04     | UP04: El camino del zen   | 22/10/2025| 20/12/2025|

## Metodología del proceso de enseñanza-aprendizaje

La metodología didáctica adoptada en esta programación se encuentra alineada con los principios y directrices establecidos en el Proyecto Curricular del Ciclo Formativo (PCCF), elaborado de forma colaborativa por el equipo docente del ciclo. Este documento marco recoge los enfoques metodológicos comunes que guían el proceso de enseñanza-aprendizaje en todos los módulos del ciclo, promoviendo una formación integral, activa y contextualizada del alumnado.

Se apuesta por metodologías activas, centradas en el estudiante, que fomentan el aprendizaje significativo, el trabajo cooperativo, la resolución de problemas y la aplicación práctica de los contenidos en contextos reales o simulados. Asimismo, se integran estrategias que favorecen la autonomía, la reflexión crítica y el desarrollo de competencias profesionales, personales y sociales.

Cualquier concreción metodológica específica, adaptada a las características del módulo o del grupo de estudiantes, se desarrollará en el diseño de las **Situaciones de Aprendizaje**, donde se detallarán las actividades, recursos y dinámicas concretas que se llevarán a cabo.

## Recursos

Los recursos didácticos utilizados en este módulo se seleccionan en coherencia con los criterios establecidos en el Proyecto Curricular del Ciclo Formativo (PCCF), que define los medios y herramientas comunes para facilitar el desarrollo de las competencias profesionales, personales y sociales del alumnado.

Se contempla el uso de recursos variados, tanto materiales como digitales, que favorecen un aprendizaje activo, contextualizado y accesible. Entre ellos se incluyen: equipamiento técnico específico del módulo, herramientas TIC, plataformas educativas, materiales audiovisuales, documentación profesional actualizada y recursos adaptados a las necesidades del grupo.

La concreción de los recursos específicos que se emplearán en cada unidad didáctica o actividad se detallará en las correspondientes **Situaciones de Aprendizaje**, en función de los objetivos, contenidos y metodologías aplicadas.

## Uso de espacios y equipamientos. 

El uso de los espacios y equipamientos necesarios para el desarrollo de este módulo se organiza conforme a lo establecido en el Proyecto Curricular del Ciclo Formativo (PCCF), donde se recogen los criterios comunes para la distribución, aprovechamiento y adecuación de los entornos formativos.

Se prioriza la utilización de espacios que reproduzcan contextos profesionales reales o simulados, favoreciendo así el aprendizaje significativo y la adquisición de competencias en condiciones similares a las del entorno laboral. Asimismo, se garantiza el acceso a los equipamientos técnicos y tecnológicos adecuados, asegurando su disponibilidad, mantenimiento y uso responsable, cumpliendo la normativa del Centro y de la Conselleria.

Las especificidades sobre el uso de espacios y equipamientos en cada actividad concreta se detallarán en las **Situaciones de Aprendizaje**, adaptándose a las necesidades del alumnado y a los objetivos de cada propuesta didáctica.

## Medidas de atención a la diversidad. 

Las medidas de atención a la diversidad contempladas en esta programación se fundamentan en los principios recogidos en el Proyecto Curricular del Ciclo Formativo (PCCF), que establece un marco común para garantizar una respuesta educativa inclusiva, equitativa y adaptada a las características del alumnado.

Se parte del reconocimiento de la diversidad como un valor y una oportunidad para el aprendizaje, promoviendo estrategias que favorezcan la participación, la motivación y el progreso de todos los estudiantes. Entre las medidas generales se incluyen la flexibilización metodológica, la adaptación de recursos, el uso de apoyos personalizados y la atención a distintos ritmos y estilos de aprendizaje.

Las adaptaciones específicas, tanto metodológicas como organizativas, se concretarán en las **Situaciones de Aprendizaje**, donde se detallarán las actuaciones necesarias para atender a las necesidades individuales del alumnado, siempre en coordinación con los servicios de orientación y el equipo docente.

## Evaluación del aprendizaje. 

@@@PCCF_200_ProcesoDeEvaluacion.md
@@@PCCF_201_TiposEvaluacion.md
@@@PCCF_202_Calificaciones.md

La ponderación de cada Resultado de Aprendizaje se indica en el Esquema General.

!!! OBLIGATORIO ]: A RELLENAR POR EL DOCENTE -> Cálculo de la calificación.

@@@PCCF_203_EvaluacionRA_FormacionEmpresa.md

!!! OBLIGATORIO ]: A RELLENAR POR EL DOCENTE -> Cálculo de la calificación de un RA Dualizado.

@@@PCCF_206_Recuperacion.md



### Convocatoria Ordinaria

1. Todo el alumnado tiene derecho a una Convocatoria Ordinaria, en el caso de que el alumnado haya superado todos los RAs 
   durante la *evaluación continua*, se establecerá su calificación como la de la Convocatoria Ordinaria.
2. Si hay RAs **no superados** durante la *evaluación continua*, el alumnado tiene derecho a una prueba que incluya dichos RAs con el objetivo 
   de comprobar que ha adquirido los Resultados de Aprendizaje descritos en el Módulo. Esta prueba se ajustará
   al calendario propuesto por el centro.

### Convocatoria Extraordinaria

La convocatoria extraordinaria del módulo se ajustará lo decidido de manera conjunta y ha sido 
descrito en el Proyecto Curricular de Ciclo Formativo.

## Actividades complementarias y extraescolares. 

A RELLENAR POR DOCENTE

## Criterios y procedimientos para la evaluación del desarrollo de la programación y de la práctica docente. 

La evaluación del propio proceso de *enseñanza-aprendizaje* contempladas en esta programación se fundamentan en los principios recogidos en el Proyecto Curricular del Ciclo Formativo (PCCF), que establece un marco común para garantizar una respuesta educativa inclusiva, equitativa y adaptada a las características del alumnado.

## Esquema General de {{modulo.nombre}}

NOTA : Aquí se generará de manera automática la tabla a partir del Excel compartido con los RA, CE y Horas Asignadas. 

NO RELLENAR.
