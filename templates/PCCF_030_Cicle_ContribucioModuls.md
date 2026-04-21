\newpage

# Contribució dels Mòduls a les Competències del Cicle {{ ciclo }}

{%- set modulos_con_competencias = [] -%}
{%- for codigo, modulo in modulos.items() if modulo.get('CompetenciasTitulo', []) -%}
  {%- if modulos_con_competencias.append((codigo, modulo)) -%}{%- endif -%}
{%- endfor -%}

## Competències Professionals

{%- for i in range(0, modulos_con_competencias|length, 10) %}
{%- set chunk = modulos_con_competencias[i:i+10] %}

### Taula {{ loop.index }}{% if modulos_con_competencias|length > 10 %} (Mòduls {{ i+1 }}-{{ [i+10, modulos_con_competencias|length]|min }}){% endif %}

| Competència |{% for codigo, modulo in chunk %} {{ codigo }} |{% endfor %}
|-------------|{% for codigo, modulo in chunk %}:---:|{% endfor %}
{%- for code in competencias_profesionales %}
| **{{ code }}** {{ cpps[code][:50] if code in cpps else '' }}... |{% for codigo, modulo in chunk %}{% if code in modulo.get('CompetenciasTitulo', []) %} X |{% else %}   |{% endif %}{% endfor %}
{%- endfor %}

{%- endfor %}

## Competències per a l'Ocupabilitat  

{%- for i in range(0, modulos_con_competencias|length, 10) %}
{%- set chunk = modulos_con_competencias[i:i+10] %}

### Taula {{ loop.index }}{% if modulos_con_competencias|length > 10 %} (Mòduls {{ i+1 }}-{{ [i+10, modulos_con_competencias|length]|min }}){% endif %}

| Competència |{% for codigo, modulo in chunk %} {{ codigo }} |{% endfor %}
|-------------|{% for codigo, modulo in chunk %}:---:|{% endfor %}
{%- for code in competencias_sociales %}
| **{{ code }}** {{ cpps[code][:50] if code in cpps else '' }}... |{% for codigo, modulo in chunk %}{% if code in modulo.get('CompetenciasTitulo', []) %} X |{% else %}   |{% endif %}{% endfor %}
{%- endfor %}

{%- endfor %}

### Llegenda de Mòduls

{% for codigo, modulo in modulos_con_competencias %}- **{{ codigo }}**: {{ modulo.nombre }}
{% endfor %}

**Notes:**
- **X** indica que el mòdul contribueix a desenvolupar aquesta competència
- Les competències professionals (a-s) estan relacionades amb les habilitats tècniques específiques del perfil professional  
- Les competències per a l'ocupabilitat (t-y) estan relacionades amb habilitats transversals i d'inserció laboral
- Només es mostren els mòduls que tenen competències assignades
{%- if modulos_con_competencias|length > 10 %}
- Les taules s'han dividit per facilitar la lectura en format PDF
{%- endif %}