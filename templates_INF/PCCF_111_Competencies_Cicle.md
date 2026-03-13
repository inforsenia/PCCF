\newpage

# Competències del cicle `{{ ciclo }}`

## Competencies Professionals

| Codi | Competència | Importància |
|--------|-------------|:---------:|{% if competencias_profesionales|length > 0 %}{% for code in competencias_profesionales %}
| {{ code }} | {{ cpps[code] if code in cpps else '' }} | {{ '$\star$' * importancia.get(code, 2) }} |{% endfor %} {% else %} | - | No hi ha competències professionals definides | - | {% endif %}

## Competencies per a la ocupabilitat

| Codi | Competència | Importància |
|--------|-------------|:---------:|{% if competencias_sociales|length > 0 %}{% for code in competencias_sociales %}
| {{ code }} | {{ cpps[code] if code in cpps else '' }} | {{ '$\star$' * importancia.get(code, 2) }} |{% endfor %} {% else %} | - | No hi ha competències per a la ocupabilitat definides | - | {% endif %}

**Llegenda**: $\star$ Baixa · $\star$$\star$ Mitjana · $\star$$\star$$\star$ Alta