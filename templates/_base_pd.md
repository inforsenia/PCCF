\newpage

# Programació didàctica: Mòdul {% if optativa %}optatiu {% endif %}{{ modulo.nombre }}

## Dades identificatives i contextualització del mòdul

És un mòdul de {{ modulo.horas }} hores que s'imparteix en {{ ciclo_contexto }}.

Té una correspondència en crèdits de {{ modulo.creditos}}.

### DOCENT

**Docent**: [###]

**correu-e**: [###]

{% if modulo.UnidadesCompetenciaAcreditadas|count > 0 %}

## Relació entre els estàndards de competència i els mòduls del cicle formatiu

| Unitat de competència | Descripció |
|-----------------------|-------------|{% for uca in modulo.UnidadesCompetenciaAcreditadas %}
| {{ uca }} | {{ modulo.UnidadesCompetenciaAcreditadas[uca] }} |{% endfor %}
|<img width=200/>|<img width=500/>|

{% endif %}

## Resultats d'aprenentatge

Els **resultats d'aprenentatge** relatius al mòdul de {{modulo.nombre}} són:

|Codi| Resultat d'aprenentatge |
|------|--------------------------|{% for ra in modulo.ResultadosAprendizaje %}
| {{ ra }} | {{ modulo.ResultadosAprendizaje[ra].Resultado }} |{% endfor %}
|<img width=200/>|<img width=500/>|

{% if modulo.ObjetivosGenerales|count > 0 %}

## Objectius generals

La formació del mòdul contribueix a assolir els *objectius generals del cicle* següents:

| Obj| Objectiu general del cicle |
|----|----------------------------|{% for obj in modulo.ObjetivosGenerales %}
| {{ obj }} | {{ modulo.OG[obj] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}


{% if modulo.CompetenciasTitulo|count > 0 %}

## Competències del títol

La formació del mòdul contribueix a assolir les *competències del títol* següents:

| Codi| Competència del títol |
|----|----------------------------|{% for com in modulo.CompetenciasTitulo %}
| {{ com }} | {{ modulo.CPSS[com] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}

## Seqüenciació de les unitats de programació

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

Les adaptacions específiques, tant metodològiques com organitzatives, es concretaran en la **programació d'aula**, on es detallaran les actuacions necessàries per a atendre les necessitats individuals de l'alumnat, sempre en coordinació amb els serveis d'orientació i l'equip docent.

## Avaluació de l'aprenentatge

La ponderació de cada resultat d'aprenentatge s'indica en l'Esquema general.

> Ací han d'aparéixer els instruments i les activitats concretes d'avaluació que s'empraran per a qualificar cada RA, en una taula amb les columnes: RA, instrument i percentatge.

[###]

### Primera convocatòria

1. Tot l'alumnat té dret a una primera convocatòria. Si l'alumne o l'alumna ha superat tots els RA durant l'*avaluació contínua*, esta qualificació serà la de la primera convocatòria.
2. Si hi ha RA **no superats** durant l'*avaluació contínua*, l'alumnat té dret a una prova que incloga eixos RA, amb l'objectiu de comprovar que ha adquirit els resultats d'aprenentatge descrits en el mòdul. Esta prova s'ajustarà al calendari proposat pel centre.

### Segona convocatòria

La segona convocatòria del mòdul s'ajustarà al que s'ha decidit de manera conjunta i s'ha descrit en el Projecte Curricular del Cicle Formatiu.

## Criteris i procediments per a l'avaluació del desenvolupament de la programació i de la pràctica docent

L'avaluació del propi procés d'*ensenyança-aprenentatge* contemplada en esta programació es fonamenta en els principis recollits en el Projecte Curricular del Cicle Formatiu (PCCF), que establix un marc comú per a garantir una resposta educativa inclusiva, equitativa i adaptada a les característiques de l'alumnat.

## Activitats complementàries i extraescolars

[###]

## Esquema general de {{modulo.nombre}}

NOTA: ací es generarà de manera automàtica la taula a partir de l'Excel compartit amb els RA, els CE i les hores assignades.

NO OMPLIR.
