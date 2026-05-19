\newpage

# Contribució dels Mòduls a les Competències del Cicle {{ ciclo }}

## Competències Professionals

| Competència |{% for codigo, modulo in modulos.items() if modulo.get('CompetenciasTitulo', []) %} {{ codigo }} |{% endfor %}
|-------------|{% for codigo, modulo in modulos.items() if modulo.get('CompetenciasTitulo', []) %}:---:|{% endfor %}
{%- for code in competencias_profesionales %}
| **{{ code }}** {{ cpps[code][:50] if code in cpps else '' }}... |{% for codigo, modulo in modulos.items() if modulo.get('CompetenciasTitulo', []) %}{% if code in modulo.get('CompetenciasTitulo', []) %} X |{% else %}   |{% endif %}{% endfor %}
{%- endfor %}

## Competències per a l'Ocupabilitat  

| Competència |{% for codigo, modulo in modulos.items() if modulo.get('CompetenciasTitulo', []) %} {{ codigo }} |{% endfor %}
|-------------|{% for codigo, modulo in modulos.items() if modulo.get('CompetenciasTitulo', []) %}:---:|{% endfor %}
{%- for code in competencias_sociales %}
| **{{ code }}** {{ cpps[code][:50] if code in cpps else '' }}... |{% for codigo, modulo in modulos.items() if modulo.get('CompetenciasTitulo', []) %}{% if code in modulo.get('CompetenciasTitulo', []) %} X |{% else %}   |{% endif %}{% endfor %}
{%- endfor %}

### Llegenda de Mòduls

{% for codigo, modulo in modulos.items() if modulo.get('CompetenciasTitulo', []) %}- **{{ codigo }}**: {{ modulo.nombre }}
{% endfor %}

**Notes:**
- **X** indica que el mòdul contribueix a desenvolupar aquesta competència
- Les competències professionals (a-s) estan relacionades amb les habilitats tècniques específiques del perfil professional  
- Les competències per a l'ocupabilitat (t-y) estan relacionades amb habilitats transversals i d'inserció laboral
- Només es mostren els mòduls que tenen competències assignades