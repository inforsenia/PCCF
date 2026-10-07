\newpage

# Programació didàctica: Mòdul {% if optativa %}optatiu {% endif %}{{ modulo.nombre }}

> **Instruccions per al docent:**
>
> 1. Substituïu les marques `[###]` per la informació real del vostre mòdul. **Heu de llevar els claudàtors sencers** (`[###]` → text real), no només les #. Si un apartat no escau, indiqueu "No escau".
> 2. Només heu d'omplir els apartats que porten `[###]`. La resta del text és comú a tot el cicle (ve del PCCF i de la normativa) i no s'ha de modificar.
> 3. Cada apartat que heu d'omplir porta davant una nota com esta que explica què s'hi espera, amb un exemple.
> 4. Quan la programació estiga completada, canvieu `_BORRADOR` per `_OK` al nom del fitxer.
>    Exemple: `PD_DAM_0485_Programacio_BORRADOR.md` → `PD_DAM_0485_Programacio_OK.md`
> 5. No modifiqueu la resta del nom del fitxer (el sistema l'usa per identificar el cicle i el mòdul).
> 6. Recordeu que en Markdown **un sol salt de línia concatena el text** (com si fóra un espai). Per a separar paràgrafs, deixeu **una línia en blanc**. Per a llistar elements, feu servir una **llista amb vinyetes** (`- element`). Les taules s'escriuen amb `|`: quan un apartat porta una taula, la nota mostra una taula d'exemple i davall teniu la taula buida per omplir; substituïu els `[###]` de cada cel·la i afegiu o esborreu files copiant-ne una sencera.
> 7. **No utilitzeu encapçalaments ( #, ##, ### ) ni blocs de notes ( > )** al vostre contingut, perquè podrien interferir amb la compilació del document final.
> 8. Les hores, els RA, els criteris d'avaluació i les ponderacions **no s'escriuen ací**: s'editen a l'Excel compartit del cicle (`libro_{CICLE}.xlsx`, la fulla del vostre mòdul) i el Quadre Resum s'afig sol al final de la programació.
> 9. Si ompliu el camp **correu-e** de l'apartat DOCENT, rebreu per correu els avisos de les marques pendents d'esta programació.
> 10. Este bloc d'instruccions i totes les notes ( > ) **s'esborraran automàticament** en compilar el PDF final.

## Dades identificatives, marc normatiu i contextualització del mòdul

És un mòdul de {{ modulo.horas }} hores que s'imparteix en {{ ciclo_contexto }}.

Té una correspondència en crèdits de {{ modulo.creditos}}.

### DOCENT

> Indiqueu el nom i cognoms del docent i el correu on vol rebre els avisos d'esta programació. Si el mòdul l'imparteixen diversos docents, separeu-los per comes, **en el mateix ordre** en tots dos camps. Al PDF apareixeran com una llista, un docent per línia amb el seu correu.
>
> Exemple: `**Docent**: Anna Pérez Gil, Joan Martí Soler` i `**correu-e**: a.perezgil@edu.gva.es, j.martisoler@edu.gva.es`

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

> Expliqueu breument com s'organitzen les unitats de programació: criteri de seqüenciació i relació amb els RA. Després completeu la taula amb una fila per unitat: número, títol, RA que treballa i trimestre (1r, 2n o 3r). Afegiu o esborreu files segons les unitats que tingueu.
>
> Exemple de paràgraf: "El mòdul s'organitza en 6 unitats que van de menys a més complexitat. Les unitats 1 i 2 treballen el RA1; la 3, el RA2 i el RA3; i les unitats 4 a 6, la resta de RA."
>
> Exemple de taula:
>
> | Número | Títol                            | RA       | Trimestre |
> |--------|----------------------------------|----------|-----------|
> | 01     | Introducció a la programació     | RA1      | 1r        |
> | 02     | Estructures de control           | RA1      | 1r        |
> | 03     | Programació orientada a objectes | RA2, RA3 | 2n        |

[###]

| Número | Títol | RA    | Trimestre |
|--------|-------|-------|-----------|
| 01     | [###] | [###] | [###]     |
| 02     | [###] | [###] | [###]     |
| 03     | [###] | [###] | [###]     |

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

> Completeu la taula amb els instruments i les activitats concretes d'avaluació que s'empraran per a qualificar cada RA: una fila per instrument, amb el RA, l'instrument i el percentatge. Els percentatges de cada RA han de sumar 100 %. El pes de cada RA en la nota del mòdul no s'escriu ací: és la ponderació de l'Excel. Afegiu o esborreu files segons calga.
>
> Exemple de taula:
>
> | RA  | Instrument d'avaluació   | Percentatge |
> |-----|--------------------------|-------------|
> | RA1 | Prova pràctica           | 60 %        |
> | RA1 | Pràctiques de laboratori | 40 %        |
> | RA2 | Projecte en grup         | 100 %       |

| RA    | Instrument d'avaluació | Percentatge |
|-------|------------------------|-------------|
| [###] | [###]                  | [###]       |
| [###] | [###]                  | [###]       |
| [###] | [###]                  | [###]       |

{% if dualitza %}
### Formació en empresa (RA dualitzats)

La valoració del tutor o tutora dual de l'empresa (superat / no superat) sobre els RA desenvolupats en l'empresa s'integra en la qualificació d'eixos RA segons els criteris següents. Els RA no superats en l'empresa es recuperen en el centre educatiu. La taula següent, generada a partir de l'Excel del mòdul (columnes REQUISIT FE (C/E) i HORES DUAL), recull els criteris d'avaluació que es desenvolupen en l'empresa (compartits amb el centre o sols en l'empresa) i les hores de formació en empresa.

> La taula dels RA dualitzats no s'escriu ací: ix sola de l'Excel (REQUISIT FE: C = compartit, E = sols empresa; i HORES DUAL). Indiqueu com s'integra la valoració de l'empresa en la qualificació dels RA dualitzats i com es recuperen.
>
> Exemple: "Els RA compartits es qualifiquen al centre. Si el tutor dual valora un RA com a no superat, l'alumne haurà de fer una pràctica de recuperació al centre abans de l'avaluació final. Els RA que només es desenvolupen en l'empresa es qualifiquen amb un 5 si l'empresa els valora com a superats; si no, es recuperen al centre amb una prova pràctica."

[###]

{% endif %}
### Pèrdua de l'avaluació contínua

Els criteris de pèrdua del dret a l'avaluació contínua per faltes d'assistència (Orde 8/2025, art. 7) i el procediment d'avaluació aplicable en eixe cas es recullen en el PCCF.

### Primera convocatòria

1. Tot l'alumnat té dret a una primera convocatòria. Si l'alumne o l'alumna ha superat tots els RA durant l'*avaluació contínua*, esta qualificació serà la de la primera convocatòria.
2. Si hi ha RA **no superats** durant l'*avaluació contínua*, l'alumnat té dret a una prova que incloga eixos RA, amb l'objectiu de comprovar que ha adquirit els resultats d'aprenentatge descrits en el mòdul. Esta prova s'ajustarà al calendari proposat pel centre.

### Programa de recuperació

L'alumnat amb RA no superats disposa d'un programa de recuperació i, si no supera el mòdul en la primera convocatòria, d'un programa formatiu específic per a preparar la segona convocatòria.

> Indiqueu les activitats de recuperació, el moment en què es realitzaran i els criteris d'avaluació que s'aplicaran.
>
> Exemple: "Per a cada RA no superat, l'alumne lliurarà les pràctiques pendents i farà una prova pràctica a la fi de cada trimestre. La qualificació del RA recuperat seguirà els mateixos instruments i percentatges que en l'avaluació contínua."

[###]

{% if pla_pendents %}
### Pla de pendents

L'alumnat que promociona a segon curs amb este mòdul pendent disposa d'un pla de recuperació que li permet superar-lo sense assistir a les classes ordinàries. El pla s'informa a l'alumnat a l'inici del curs i té com a referents els resultats d'aprenentatge i els criteris d'avaluació no superats.

> Indiqueu les activitats i els treballs que haurà de realitzar l'alumnat, el calendari de lliuraments i proves, el seguiment previst (horari d'atenció, tutories, plataforma), i els instruments i criteris de qualificació.
>
> Exemple: "L'alumne disposarà a Aules d'un curs amb les pràctiques de cada RA no superat, amb lliuraments a final d'octubre, gener i març, i una prova pràctica a l'abril. Tindrà una hora setmanal de tutoria amb el docent. Les pràctiques valdran el 40 % i la prova, el 60 %."

[###]

{% endif %}
### Segona convocatòria

La segona convocatòria del mòdul s'ajustarà al que s'ha decidit de manera conjunta i s'ha descrit en el Projecte Curricular del Cicle Formatiu.

## Criteris i procediments per a l'avaluació del desenvolupament de la programació i de la pràctica docent

L'avaluació del propi procés d'*ensenyança-aprenentatge* contemplada en esta programació es fonamenta en els principis recollits en el Projecte Curricular del Cicle Formatiu (PCCF), que establix un marc comú per a garantir una resposta educativa inclusiva, equitativa i adaptada a les característiques de l'alumnat.

El desenvolupament de la programació es revisa periòdicament en les reunions de departament, tenint en compte, entre altres indicadors, el grau de compliment de la seqüenciació prevista, els resultats de l'alumnat per RA i l'adequació de la metodologia, els recursos i els instruments d'avaluació. Al final de curs, estos aspectes es valoren en la memòria del departament i les propostes de millora s'incorporen a la programació del curs següent.

Els criteris de qualificació de l'alumnat es recullen en l'apartat *Avaluació de l'aprenentatge*.

## Activitats complementàries i extraescolars

> Indiqueu les activitats complementàries i extraescolars previstes per al mòdul, amb una data aproximada i els RA amb què es relacionen. Si no n'hi ha cap de prevista, indiqueu "No escau".
>
> Exemple: "- Visita al centre de dades d'una empresa del sector (2n trimestre, RA3 i RA4). - Xarrada d'una professional sobre ciberseguretat (novembre, RA5)."

[###]

## Contribució al Projecte intermodular

D'acord amb {% if ciclo_curriculum %}l'article 5 del Decret 114/2025 i {% endif %}els criteris establits en el PCCF, el Projecte intermodular integra resultats d'aprenentatge de diversos mòduls del cicle.

> Indiqueu quins RA d'este mòdul s'integren en el Projecte intermodular i com es coordina amb l'equip docent. Si no escau, indiqueu "No escau".
>
> Exemple: "Els RA3 i RA5 d'este mòdul s'integren en el Projecte intermodular. L'alumnat dissenya la base de dades del projecte. El seguiment es fa en les reunions quinzenals de l'equip docent, i la nota d'eixos RA té en compte el lliurament corresponent del projecte."

[###]

## Esquema general de {{modulo.nombre}}

> NOTA: ací es generarà de manera automàtica la taula a partir de l'Excel compartit amb els RA, els CE i les hores assignades. NO OMPLIR.
