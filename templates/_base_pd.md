\newpage

# Programació didàctica: Mòdul {% if optativa %}optatiu {% endif %}{{ modulo.nombre }}

## Dades identificatives, marc normatiu i contextualització del mòdul

És un mòdul de {{ modulo.horas }} hores que s'imparteix en {{ ciclo_contexto }}.

Té una correspondència en crèdits de {{ modulo.creditos}}.

### DOCENT

**Docent**: [###]

**correu-e**: [###]

### Marc normatiu

Esta programació s'ajusta a la normativa següent:

- Llei orgànica 3/2022, de 31 de març, d'ordenació i integració de la Formació Professional.
- Reial decret 659/2023, de 18 de juliol, pel qual es desenvolupa l'ordenació del Sistema de Formació Professional.
{% if ciclo_curriculum %}- {{ ciclo_curriculum }}.
{% endif %}- Orde 8/2025, de 22 d'abril, de la Conselleria d'Educació, Cultura, Universitats i Ocupació, per la qual es regula l'avaluació del procés d'ensenyança-aprenentatge en cicles formatius i cursos d'especialització.
- Resolució d'instruccions d'inici de curs per als centres que imparteixen Formació Professional (graus D i E) vigent per al curs acadèmic.

El reial decret del títol{% if not ciclo_curriculum %}, el decret autonòmic de currículum{% endif %} i la resta de normativa específica del cicle es recullen en el Projecte Curricular del Cicle Formatiu (PCCF).

## Relació entre els estàndards de competència i els mòduls del cicle formatiu

{% if modulo.UnidadesCompetenciaAcreditadas|count > 0 %}
Este mòdul està associat als estàndards de competència següents:

| Estàndard de competència | Descripció |
|-----------------------|-------------|{% for uca in modulo.UnidadesCompetenciaAcreditadas %}
| {{ uca }} | {{ modulo.UnidadesCompetenciaAcreditadas[uca] }} |{% endfor %}
|<img width=200/>|<img width=500/>|
{% else %}
No escau: este mòdul no té estàndards de competència associats.
{% endif %}

## Contribució dels resultats d'aprenentatge a les competències

Els resultats d'aprenentatge del mòdul, juntament amb els seus criteris d'avaluació, són els referents de l'avaluació i contribueixen a assolir els objectius generals i les competències professionals, personals i socials del títol que s'indiquen a continuació.

### Resultats d'aprenentatge

Els **resultats d'aprenentatge** relatius al mòdul de {{modulo.nombre}} són:

|Codi| Resultat d'aprenentatge |
|------|--------------------------|{% for ra in modulo.ResultadosAprendizaje %}
| {{ ra }} | {{ modulo.ResultadosAprendizaje[ra].Resultado }} |{% endfor %}
|<img width=200/>|<img width=500/>|

{% if modulo.ObjetivosGenerales|count > 0 %}

### Objectius generals

La formació del mòdul contribueix a assolir els *objectius generals del cicle* següents:

| Obj| Objectiu general del cicle |
|----|----------------------------|{% for obj in modulo.ObjetivosGenerales %}
| {{ obj }} | {{ modulo.OG[obj] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}


{% if modulo.CompetenciasTitulo|count > 0 %}

### Competències del títol

La formació del mòdul contribueix a assolir les *competències del títol* següents:

| Codi| Competència del títol |
|----|----------------------------|{% for com in modulo.CompetenciasTitulo %}
| {{ com }} | {{ modulo.CPSS[com] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}

## Esquema general i seqüenciació de les unitats de programació

L'esquema general del mòdul (RA, criteris d'avaluació, hores i ponderació de cada RA) es genera automàticament a partir de l'Excel compartit i s'inclou al final d'esta programació.

> **Instruccions per al docent:** Substituïu les marques `[###]` per la informació real del vostre mòdul. Si una secció no escau, indiqueu "No escau".

[###]

Es proposa esta taula orientativa:

| Número | Títol                     | Trimestre |
|--------|---------------------------|-----------|
| 01     | [###] | [###] |

## Metodologia del procés d'ensenyança-aprenentatge

La metodologia didàctica adoptada en esta programació està alineada amb els principis i directrius establits en el Projecte Curricular del Cicle Formatiu (PCCF), elaborat de manera col·laborativa per l'equip docent del cicle. Este document marc recull els enfocaments metodològics comuns que guien el procés d'ensenyança-aprenentatge en tots els mòduls del cicle, i promou una formació integral, activa i contextualitzada de l'alumnat.

S'aposta per metodologies actives, centrades en l'alumnat, que fomenten l'aprenentatge significatiu, el treball cooperatiu, la resolució de problemes i l'aplicació pràctica dels continguts en contextos reals o simulats. Així mateix, s'integren estratègies que afavorixen l'autonomia, la reflexió crítica i el desenvolupament de competències professionals, personals i socials.

Qualsevol concreció metodològica específica, adaptada a les característiques del mòdul o del grup d'alumnes, es desenvoluparà en la **programació d'aula**, on es detallaran les activitats, els recursos i les dinàmiques concretes que es duran a terme.

## Recursos

Els recursos didàctics utilitzats en este mòdul se seleccionen en coherència amb els criteris establits en el Projecte Curricular del Cicle Formatiu (PCCF), que definix els mitjans i les ferramentes comuns per a facilitar el desenvolupament de les competències professionals, personals i socials de l'alumnat.

Es contempla l'ús de recursos variats, tant materials com digitals, que afavorixen un aprenentatge actiu, contextualitzat i accessible. Entre ells s'inclouen: equipament tècnic específic del mòdul, ferramentes TIC, plataformes educatives, materials audiovisuals, documentació professional actualitzada i recursos adaptats a les necessitats del grup.

La concreció dels recursos específics que s'empraran en cada unitat didàctica o activitat es detallarà en la **programació d'aula**, en funció dels objectius, els continguts i les metodologies aplicades.

## Ús d'espais i equipaments

L'ús dels espais i equipaments necessaris per al desenvolupament d'este mòdul s'organitza d'acord amb el que s'establix en el Projecte Curricular del Cicle Formatiu (PCCF), on es recullen els criteris comuns per a la distribució, l'aprofitament i l'adequació dels entorns formatius.

Es prioritza la utilització d'espais que reproduïsquen contextos professionals reals o simulats, i s'afavorix així l'aprenentatge significatiu i l'adquisició de competències en condicions semblants a les de l'entorn laboral. Així mateix, es garantix l'accés als equipaments tècnics i tecnològics adequats, i se n'assegura la disponibilitat, el manteniment i l'ús responsable, d'acord amb la normativa del centre i de la Conselleria.

Les especificitats sobre l'ús d'espais i equipaments en cada activitat concreta es detallaran en la **programació d'aula**, i s'adaptaran a les necessitats de l'alumnat i als objectius de cada proposta didàctica.

## Mesures d'atenció a la diversitat

Les mesures d'atenció a la diversitat contemplades en esta programació es fonamenten en els principis recollits en el Projecte Curricular del Cicle Formatiu (PCCF), que establix un marc comú per a garantir una resposta educativa inclusiva, equitativa i adaptada a les característiques de l'alumnat.

Es parteix del reconeixement de la diversitat com un valor i una oportunitat per a l'aprenentatge, i es promouen estratègies que afavorisquen la participació, la motivació i el progrés de tot l'alumnat. Entre les mesures generals s'inclouen la flexibilització metodològica, l'adaptació de recursos, l'ús de suports personalitzats i l'atenció a diferents ritmes i estils d'aprenentatge.

D'acord amb el Decret 104/2018, de 27 de juliol, i l'Orde 20/2019, de 30 d'abril, les adaptacions d'accés i metodològiques no suposen la modificació dels resultats d'aprenentatge ni dels criteris d'avaluació, que continuen sent els referents de l'avaluació.

Les adaptacions específiques, tant metodològiques com organitzatives, es concretaran en la **programació d'aula**, on es detallaran les actuacions necessàries per a atendre les necessitats individuals de l'alumnat, sempre en coordinació amb els serveis d'orientació i l'equip docent.

## Avaluació de l'aprenentatge

L'avaluació és contínua i té com a referents els resultats d'aprenentatge i els criteris d'avaluació del mòdul. La qualificació del mòdul és numèrica, entre 1 i 10 sense decimals, i es considera superat amb una qualificació igual o superior a 5 (Orde 8/2025, art. 5). La ponderació de cada resultat d'aprenentatge s'indica en l'Esquema general.

Al principi de curs es realitza una avaluació inicial que permet adaptar esta programació a les característiques del grup, segons el que establix el PCCF.

### Instruments i criteris de qualificació

> Ací han d'aparéixer els instruments i les activitats concretes d'avaluació que s'empraran per a qualificar cada RA, en una taula amb les columnes: RA, instrument i percentatge.

[###]

### Formació en empresa (RA dualitzats)

La valoració del tutor o tutora dual de l'empresa (superat / no superat) sobre els RA desenvolupats en l'empresa s'integra en la qualificació d'eixos RA segons els criteris següents. Els RA no superats en l'empresa es recuperen en el centre educatiu. Els RA i les hores de formació en empresa consten en l'Esquema general (columnes REQUISIT FE i HORES DUAL).

> Indiqueu com s'integra la valoració de l'empresa en la qualificació dels RA dualitzats i com es recuperen. Si el mòdul no té RA dualitzats, indiqueu "No escau".

[###]

### Pèrdua de l'avaluació contínua

Els criteris de pèrdua del dret a l'avaluació contínua per faltes d'assistència (Orde 8/2025, art. 7) i el procediment d'avaluació aplicable en eixe cas es recullen en el PCCF.

### Primera convocatòria

1. Tot l'alumnat té dret a una primera convocatòria. Si l'alumne o l'alumna ha superat tots els RA durant l'*avaluació contínua*, esta qualificació serà la de la primera convocatòria.
2. Si hi ha RA **no superats** durant l'*avaluació contínua*, l'alumnat té dret a una prova que incloga eixos RA, amb l'objectiu de comprovar que ha adquirit els resultats d'aprenentatge descrits en el mòdul. Esta prova s'ajustarà al calendari proposat pel centre.

### Programa de recuperació

L'alumnat amb RA no superats disposa d'un programa de recuperació i, si no supera el mòdul en la primera convocatòria, d'un programa formatiu específic per a preparar la segona convocatòria.

> Indiqueu les activitats de recuperació, el moment en què es realitzaran i els criteris d'avaluació que s'aplicaran.

[###]

### Segona convocatòria

La segona convocatòria del mòdul s'ajustarà al que s'ha decidit de manera conjunta i s'ha descrit en el Projecte Curricular del Cicle Formatiu.

## Criteris i procediments per a l'avaluació del desenvolupament de la programació i de la pràctica docent

L'avaluació del propi procés d'*ensenyança-aprenentatge* contemplada en esta programació es fonamenta en els principis recollits en el Projecte Curricular del Cicle Formatiu (PCCF), que establix un marc comú per a garantir una resposta educativa inclusiva, equitativa i adaptada a les característiques de l'alumnat.

El desenvolupament de la programació es revisa periòdicament en les reunions de departament, tenint en compte, entre altres indicadors, el grau de compliment de la seqüenciació prevista, els resultats de l'alumnat per RA i l'adequació de la metodologia, els recursos i els instruments d'avaluació. Al final de curs, estos aspectes es valoren en la memòria del departament i les propostes de millora s'incorporen a la programació del curs següent.

Els criteris de qualificació de l'alumnat es recullen en l'apartat *Avaluació de l'aprenentatge*.

## Activitats complementàries i extraescolars

[###]

## Contribució al Projecte intermodular

D'acord amb {% if ciclo_curriculum %}l'article 5 del Decret 114/2025 i {% endif %}els criteris establits en el PCCF, el Projecte intermodular integra resultats d'aprenentatge de diversos mòduls del cicle.

> Indiqueu quins RA d'este mòdul s'integren en el Projecte intermodular i com es coordina amb l'equip docent. Si no escau, indiqueu "No escau".

[###]

## Esquema general de {{modulo.nombre}}

NOTA: ací es generarà de manera automàtica la taula a partir de l'Excel compartit amb els RA, els CE i les hores assignades.

NO OMPLIR.
