## Competències del cicle `{{ ciclo }}`

### Competencias Professionals

| Codi | Competència | Importància |
|--------|-------------|:---------:|{% if competencias_profesionales|length > 0 %}{% for code in competencias_profesionales %}
| {{ code }} | {{ cpps[code] if code in cpps else '' }} | {{ '★' * importancia.get(code, 2) }} |{% endfor %} {% else %} | - | No hi ha competències professionals definides | - | {% endif %}

### Competencias per a la ocupabilitat

| Codi | Competència | Importància |
|--------|-------------|:---------:|{% if competencias_sociales|length > 0 %}{% for code in competencias_sociales %}
| {{ code }} | {{ cpps[code] if code in cpps else '' }} | {{ '★' * importancia.get(code, 2) }} |{% endfor %} {% else %} | - | No hi ha competències per a la ocupabilitat definides | - | {% endif %}

**Llegenda**: ★ Baixa · ★★ Mitjana · ★★★ Alta