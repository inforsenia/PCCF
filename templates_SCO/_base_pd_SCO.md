\newpage

# Programació didàctica: Mòdul {{ modulo.nombre }}

## Datos identificativos y contextualización del módulo. 

{% block intro %}{% endblock %}

Tiene una correspondéncia en Créditos de {{ modulo.creditos}}.

### DOCENT

**Docent**: [###]

**correu-e**: [###]


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
[###]
{% endif %}

#### {{ct}}.5 Instrumentos y procedimientos de evaluación

{% if modulo.ContenidosTemasRA[ct].Evaluacion|count > 0 %}
{% for instrumento in modulo.ContenidosTemasRA[ct].Evaluacion %}
- {{instrumento}}
{% endfor %}
{% else %}
[###]
{% endif %}

{% endfor %}

## Secuenciación y temporización

| Evaluación | Temas | Sesiones | Horas |
|------------|-------|----------|-------|{% for ct in modulo.ContenidosTemasRA %}
| {% if modulo.ContenidosTemasRA[ct].Evaluacion_periodo %}{{modulo.ContenidosTemasRA[ct].Evaluacion_periodo}}{% else %}[###]{% endif %} | {{ct}} - {{modulo.ContenidosTemasRA[ct].Titulo}} | {% if modulo.ContenidosTemasRA[ct].Sesiones %}{{modulo.ContenidosTemasRA[ct].Sesiones}}{% else %}[###]{% endif %} | {% if modulo.ContenidosTemasRA[ct].Horas %}{{modulo.ContenidosTemasRA[ct].Horas}}{% else %}[###]{% endif %} |{% endfor %}
|<img width=150/>|<img width=300/>|<img width=150/>|<img width=150/>|

## Metodología

> **Instruccions per al docent:** Substituïu les marques `[###]` per la informació real del vostre mòdul. Si una secció no escau, indiqueu "No escau".

### Orientaciones pedagógicas

{% block orientaciones %}{% endblock %}

### Estrategias metodológicas

{% block estrategias_metodologicas %}{% endblock %}

### Recursos didácticos

{% block recursos_didacticos %}{% endblock %}

## Evaluación

### Criterios de evaluación generales

{% block criterios_evaluacion_generales %}{% endblock %}

### Instrumentos de evaluación

{% block instrumentos_evaluacion %}{% endblock %}

### Criterios de calificación

{% block criterios_calificacion %}{% endblock %}

### Recuperación

{% block recuperacion %}{% endblock %}

## Atención a la diversidad

{% block atencion_diversidad %}{% endblock %}

## Actividades complementarias

{% block actividades_complementarias %}{% endblock %}
