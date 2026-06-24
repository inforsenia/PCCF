\newpage

# Programació didàctica: Mòdul optatiu {{ modulo.nombre }}

## Dades identificatives i contextualització del mòdul

És un mòdul de {{ modulo.horas }} hores que s'imparteix en el cicle formatiu corresponent.

Té una correspondència en Crèdits de {{ modulo.creditos }}.

{% if modulo.UnidadesCompetenciaAcreditadas|count > 0 %}

## Relació entre els estàndards de competència i els mòduls del cicle formatiu

| Unitat de Competència | Descripció |
|-----------------------|-------------|{% for uca in modulo.UnidadesCompetenciaAcreditadas %}
| {{ uca }} | {{ modulo.UnidadesCompetenciaAcreditadas[uca] }} |{% endfor %}
|<img width=200/>|<img width=500/>|

{% endif %}

## Resultats d'Aprenentatge

Els **Resultats d'Aprenentatge** relatius al mòdul de {{modulo.nombre}} són:

|Codi| Resultat d'Aprenentatge |
|------|--------------------------|{% for ra in modulo.ResultadosAprendizaje %}
| {{ ra }} | {{ modulo.ResultadosAprendizaje[ra].Resultado }} |{% endfor %}
|<img width=200/>|<img width=500/>|

{% if modulo.ObjetivosGenerales|count > 0 %}

## Objectius Generals

La formació del mòdul contribueix a aconseguir els *Objectius Generals del Cicle* següents:

| Obj| Objectiu General del Cicle |
|----|----------------------------|{% for obj in modulo.ObjetivosGenerales %}
| {{ obj }} | {{ modulo.OG[obj] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}


{% if modulo.CompetenciasTitulo|count > 0 %}

## Competències del Títol

La formació del mòdul contribueix a aconseguir les *Competències del Títol* següents:

| Obj| Competència del Títol |
|----|----------------------------|{% for com in modulo.CompetenciasTitulo %}
| {{ com }} | {{ modulo.CPSS[com] }} |{% endfor %}
|<img width=100/>|<img width=500/>|

{% endif %}

## Seqüenciació de les Unitats de Programació

> **Instruccions per al docent:** Substituïu les marques `[###]` per la informació real del vostre mòdul. Si una secció no escau, indiqueu "No escau".

[###]

Es proposa aquesta taula orientativa

| Número | Títol                    | Inici    | Fi       |
|--------|--------------------------|----------|----------|
| 01     | [###] | [###] | [###] |

## Metodologia del procés d'ensenyament-aprenentatge

La metodologia didàctica adoptada en aquesta programació es troba alineada amb els principis i directrius establerts en el Projecte Curricular del Cicle Formatiu (PCCF), elaborat de forma col·laborativa per l'equip docent del cicle. Aquest document marc recull els enfocaments metodològics comuns que guien el procés d'ensenyament-aprenentatge en tots els mòduls del cicle, promovent una formació integral, activa i contextualitzada de l'alumnat.

S'aposta per metodologies actives, centrades en l'estudiant, que fomenten l'aprenentatge significatiu, el treball cooperatiu, la resolució de problemes i l'aplicació pràctica dels continguts en contextos reals o simulats. Així mateix, s'integren estratègies que afavoreixen l'autonomia, la reflexió crítica i el desenvolupament de competències professionals, personals i socials.

Qualsevol concreció metodològica específica, adaptada a les característiques del mòdul o del grup d'estudiants, es desenvoluparà en el disseny de les **Situacions d'Aprenentatge**, on es detallaran les activitats, recursos i dinàmiques concretes que es duran a terme.

## Recursos

Els recursos didàctics utilitzats en aquest mòdul se seleccionen en coherència amb els criteris establerts en el Projecte Curricular del Cicle Formatiu (PCCF), que defineix els mitjans i eines comunes per a facilitar el desenvolupament de les competències professionals, personals i socials de l'alumnat.

Es contempla l'ús de recursos variats, tant materials com digitals, que afavoreixen un aprenentatge actiu, contextualitzat i accessible. Entre ells s'inclouen: equipament tècnic específic del mòdul, eines TIC, plataformes educatives, materials audiovisuals, documentació professional actualitzada i recursos adaptats a les necessitats del grup.

La concreció dels recursos específics que s'empraran en cada unitat didàctica o activitat es detallarà en les corresponents **Situacions d'Aprenentatge**, en funció dels objectius, continguts i metodologies aplicades.

## Ús d'espais i equipaments

L'ús dels espais i equipaments necessaris per al desenvolupament d'aquest mòdul s'organitza conforme al que s'estableix en el Projecte Curricular del Cicle Formatiu (PCCF), on es recullen els criteris comuns per a la distribució, aprofitament i adequació dels entorns formatius.

Es prioritza la utilització d'espais que reprodueixin contextos professionals reals o simulats, afavorint així l'aprenentatge significatiu i l'adquisició de competències en condicions similars a les de l'entorn laboral. Així mateix, es garanteix l'accés als equipaments tècnics i tecnològics adequats, assegurant la seua disponibilitat, manteniment i ús responsable, complint la normativa del Centre i de la Conselleria.

Les especificitats sobre l'ús d'espais i equipaments en cada activitat concreta es detallaran en les **Situacions d'Aprenentatge**, adaptant-se a les necessitats de l'alumnat i als objectius de cada proposta didàctica.

## Mesures d'atenció a la diversitat

Les mesures d'atenció a la diversitat contemplades en aquesta programació es fonamenten en els principis recollits en el Projecte Curricular del Cicle Formatiu (PCCF), que estableix un marc comú per a garantir una resposta educativa inclusiva, equitativa i adaptada a les característiques de l'alumnat.

Es parteix del reconeixement de la diversitat com un valor i una oportunitat per a l'aprenentatge, promovent estratègies que afavoreixin la participació, la motivació i el progrés de tots els estudiants. Entre les mesures generals s'inclouen la flexibilització metodològica, l'adaptació de recursos, l'ús de suports personalitzats i l'atenció a diferents ritmes i estils d'aprenentatge.

Les adaptacions específiques, tant metodològiques com organitzatives, es concretaran en les **Situacions d'Aprenentatge**, on es detallaran les actuacions necessàries per a atendre les necessitats individuals de l'alumnat, sempre en coordinació amb els serveis d'orientació i l'equip docent.

## Avaluació de l'aprenentatge

La ponderació de cada Resultat d'Aprenentatge s'indica en l'Esquema General.

- **Càlcul de la qualificació**: [###]
- **Càlcul de la qualificació d'un RA dualitzat**: [###]

### Convocatòria Ordinària

1. Tot l'alumnat té dret a una Convocatòria Ordinària, en el cas que l'alumnat haja superat tots els RAs
   durant l'*avaluació contínua*, s'establirà la seua qualificació com la de la Convocatòria Ordinària.
2. Si hi ha RAs **no superats** durant l'*avaluació contínua*, l'alumnat té dret a una prova que incloga aquests RAs amb l'objectiu
   de comprovar que ha adquirit els Resultats d'Aprenentatge descrits en el Mòdul. Aquesta prova s'ajustarà
   al calendari proposat pel centre.

### Convocatòria Extraordinària

La convocatòria extraordinària del mòdul s'ajustarà al que es decidisca de manera conjunta i ha sigut
descrit en el Projecte Curricular del Cicle Formatiu.

## Activitats complementàries i extraescolars

[###]

## Criteris i procediments per a l'avaluació del desenvolupament de la programació i de la pràctica docent

L'avaluació del propi procés d'*ensenyament-aprenentatge* contemplades en aquesta programació es fonamenten en els principis recollits en el Projecte Curricular del Cicle Formatiu (PCCF), que estableix un marc comú per a garantir una resposta educativa inclusiva, equitativa i adaptada a les característiques de l'alumnat.

## Esquema General de {{modulo.nombre}}

NOTA : Ací es generarà de manera automàtica la taula a partir de l'Excel compartit amb els RA, CE i Hores Assignades.

NO OMPLIR.
