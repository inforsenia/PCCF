\newpage

# Programación didáctica: Módulo {{ modulo.nombre }}

## Datos identificativos y contextualización del módulo. 

Es un módulo de {{ modulo.horas }} horas que se imparte en el Ciclo de Grado Superior de 
Técnico Superior en Integración Social.

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

| Cód| Competencia del Título |
|----|------------------------|{% for ct in modulo.CompetenciasTitulo %}
| {{ ct }} | {{ modulo.CPSS[ct] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}

## Contenidos básicos

{% for ct in modulo.ContenidosTemasRA %}
### {{ct}} - {{modulo.ContenidosTemasRA[ct].Titulo}}

#### {{ct}}.1 Resultados de Aprendizaje asociados

{% for ra in modulo.ContenidosTemasRA[ct].RAs %}
- **{{ra}}**: {{modulo.ResultadosAprendizaje[ra].Resultado}}
{% endfor %}

#### {{ct}}.2 Criterios de evaluación del RA

{% for ra in modulo.ContenidosTemasRA[ct].RAs %}
- **{{ra}}**: {{modulo.ResultadosAprendizaje[ra].Resultado}}
{% for ce in modulo.ResultadosAprendizaje[ra].CriteriosEvaluacion %}
  - {{ce}} {{modulo.ResultadosAprendizaje[ra].CriteriosEvaluacion[ce]}}
{% endfor %}

{% endfor %}

#### {{ct}}.3 Contenidos

{% for contenido in modulo.ContenidosTemasRA[ct].Contenidos %}
- {{contenido}}
{% endfor %}

#### {{ct}}.4 Actividades de enseñanza y aprendizaje

{% if modulo.ContenidosTemasRA[ct].Actividades|count > 0 %}
{% for actividad in modulo.ContenidosTemasRA[ct].Actividades %}
- {{actividad}}
{% endfor %}
{% else %}
*Pendiente de desarrollar.*
{% endif %}

#### {{ct}}.5 Instrumentos y procedimientos de evaluación

{% if modulo.ContenidosTemasRA[ct].Evaluacion|count > 0 %}
{% for instrumento in modulo.ContenidosTemasRA[ct].Evaluacion %}
- {{instrumento}}
{% endfor %}
{% else %}
*Pendiente de desarrollar.*
{% endif %}

{% endfor %}

## Secuenciación y temporización

| Evaluación | Temas | Sesiones | Horas |
|------------|-------|----------|-------|{% for ct in modulo.ContenidosTemasRA %}
| {% if modulo.ContenidosTemasRA[ct].Evaluacion_periodo %}{{modulo.ContenidosTemasRA[ct].Evaluacion_periodo}}{% else %}Por determinar{% endif %} | {{ct}} - {{modulo.ContenidosTemasRA[ct].Titulo}} | {% if modulo.ContenidosTemasRA[ct].Sesiones %}{{modulo.ContenidosTemasRA[ct].Sesiones}}{% else %}Por determinar{% endif %} | {% if modulo.ContenidosTemasRA[ct].Horas %}{{modulo.ContenidosTemasRA[ct].Horas}}{% else %}Por determinar{% endif %} |{% endfor %}
|<img width=150/>|<img width=300/>|<img width=150/>|<img width=150/>|

## Metodología

### Orientaciones pedagógicas

El módulo de {{modulo.nombre}} es esencial en la formación del Técnico Superior en Integración Social, proporcionando las competencias necesarias para la intervención socioeducativa con colectivos en riesgo de exclusión social.

### Estrategias metodológicas

- **Metodología participativa**: Implicación activa del alumnado en su aprendizaje
- **Aprendizaje basado en proyectos**: Desarrollo de intervenciones sociales reales
- **Estudio de casos**: Análisis crítico de situaciones de exclusión social
- **Trabajo colaborativo**: Desarrollo de habilidades de trabajo en equipo
- **Reflexión crítica**: Análisis de la realidad social y las desigualdades

### Recursos didácticos

- Aula con equipamiento audiovisual
- Acceso a recursos bibliográficos especializados
- Plataformas digitales de gestión social
- Material de apoyo para dinámicas grupales
- Bases de datos de recursos sociales

## Evaluación

### Criterios de evaluación generales

La evaluación será continua y formativa, orientada al desarrollo de competencias profesionales para la intervención social.

### Instrumentos de evaluación

- Pruebas teórico-prácticas
- Diseño de proyectos de intervención social
- Análisis de casos prácticos
- Presentaciones y debates
- Trabajos de investigación social

### Criterios de calificación

- Exámenes teórico-prácticos: 55%
- Proyectos de intervención: 30%
- Participación y actitud: 15%

### Recuperación

Los alumnos que no superen el módulo en evaluación ordinaria tendrán derecho a una evaluación extraordinaria, adaptada a las competencias no alcanzadas.

## Atención a la diversidad

Se aplicarán medidas de atención a la diversidad siguiendo los principios de inclusión social que caracterizan la profesión, adaptando metodologías y recursos según las necesidades individuales.

## Actividades complementarias

- Visitas a entidades de acción social
- Conferencias de profesionales del tercer sector
- Talleres de sensibilización social
- Participación en actividades de voluntariado
- Jornadas de intercambio con organizaciones sociales