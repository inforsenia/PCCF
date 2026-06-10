# PROGRAMACIÓN DIDÁCTICA: DESARROLLO WEB EN ENTORNO CLIENTE (0612)



### Resumen de Unidades de Programación (Curso 2025-2026)

| Código | Título de la UP | Duración | Temporalización | RA asociados (Descripción breve) |
| :--- | :--- | :---: | :--- | :--- |
| **UP01** | **Introducción DWEC** | 7 h | 08/09/25 – 20/09/25 | **RA01:** Arquitecturas y tecnologías de programación cliente web |
| **UP02** | **JavaScript. Sintaxis** | 14 h | 21/09/25 – 21/10/25 | **RA02:** Sintaxis JavaScript y ejecución en navegadores |
| **UP03** | **JavaScript. Objetos** | 28 h | 22/10/25 – 12/11/25 | **RA03:** Objetos predefinidos del lenguaje |
| **UP04** | **JavaScript. BOM-DOM** | 28 h | 13/11/25 – 15/01/26 | **RA04:** Estructuras definidas por el usuario |
| **UP05** | **JavaScript. Interactuación con el usuario, eventos** | 28 h | 16/01/26 – 16/02/26 | **RA05:** Manejo de eventos <br> **RA06:** Modelo de objetos del documento (DOM) <br> **RA07:** Comunicación asíncrona (AJAX) |

*   La suma total de estas unidades es de **105 horas** impartidas en el centro, dentro de las 200 horas totales del módulo (14 h dualizadas).


---

## UP01: Introducción DWEC
### 1. Identificación
| Campo | Detalle |
| :--- | :--- |
| **Código** | UP01 |
| **Módulo** | Desarrollo Web en Entorno Cliente (0612) |
| **Duración** | **7 Horas** |
| **Temporalización** | Del **08/09/2025** al **20/09/2025** |

### 2. Fundamentación
**Resultado de Aprendizaje**
*   **RA01.** Selecciona las arquitecturas y tecnologías de programación sobre clientes web, identificando y analizando las capacidades y características de cada una.

**Criterios de Evaluación**
*   **a)** Se han caracterizado y diferenciado los modelos de ejecución de código en el servidor y en el cliente web.
*   **b)** Se han identificado las capacidades y mecanismos de ejecución de código de los navegadores web.
*   **c)** Se han identificado y caracterizado los principales lenguajes relacionados con la programación de clientes web.
*   **d)** Se han reconocido las particularidades de la programación de guiones y sus ventajas y desventajas sobre la programación tradicional.
*   **e)** Se han verificado los mecanismos de integración de los lenguajes de marcas con los lenguajes de programación de clientes web.
*   **f)** Se han reconocido y evaluado las herramientas de programación y prueba sobre clientes web.

**Competencias**
*   **Profesionales:** g), i), q).
*   **Ocupación:** p).

### 3. Organización
**Contenidos**
*   Modelos de ejecución: cliente vs. servidor. Arquitecturas web.
*   El navegador como entorno de ejecución: motor JavaScript, motor de renderizado.
*   Lenguajes de programación cliente: JavaScript, TypeScript, WebAssembly.
*   Programación de guiones (scripting): ventajas e inconvenientes frente a la programación tradicional.
*   Integración de scripts en HTML: etiqueta `<script>`, atributos `defer` y `async`.
*   Herramientas de desarrollo: DevTools del navegador, VS Code, extensiones de depuración.

**Metodología**
*   Uso de metodologías activas centradas en el estudiante mediante el **proyecto WebApp**. El alumnado actúa como equipo de desarrollo frontend que recibe el primer briefing de un cliente: antes de escribir código, analiza el ecosistema tecnológico disponible y elige las herramientas con las que trabajará durante todo el curso.

**Secuencia (Fases)**
*   **E1:** Arquitecturas web: ejecución en servidor vs. cliente; casos de uso reales.
*   **E2:** El navegador como máquina virtual: motor JS, DevTools y consola.
*   **E3:** Integración HTML + JavaScript: `<script>`, `defer`, `async`.
*   **E4:** Entrega: informe de selección tecnológica y configuración del entorno de desarrollo.

**Recursos**
*   Aula de informática, navegadores modernos (Chrome, Firefox), VS Code, DevTools, documentación MDN Web Docs, fichas de prácticas guiadas.

## 4. EVALUACIÓN Y ADAPTACIÓN

### Instrumentos de evaluación
La evaluación será continua y formativa, enfocada en la adquisición de competencias.
*   **Prácticas Obligatorias (100%):** Informe de selección tecnológica y configuración del entorno, evaluado con rúbrica.

### Adaptaciones
*   **Medidas según necesidades:** Las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
*   **DUA:** Se empleará el **Diseño Universal para el Aprendizaje** proporcionando materiales en múltiples formatos y permitiendo la flexibilización de tiempos en las tareas del proyecto.
---

## UP02: JAVASCRIPT. SINTAXIS
### 1. Identificación
| Campo | Detalle |
| :--- | :--- |
| **Código** | UP02 |
| **Módulo** | Desarrollo Web en Entorno Cliente (0612) |
| **Duración** | **14 Horas** |
| **Temporalización** | Del **21/09/2025** al **21/10/2025** |

### 2. Fundamentación
**Resultado de Aprendizaje**
*   **RA02.** Escribe sentencias simples, aplicando la sintaxis del lenguaje y verificando su ejecución sobre navegadores web.

**Criterios de Evaluación**
*   **a)** Se ha seleccionado un lenguaje de programación de clientes web en función de sus posibilidades.
*   **b)** Se han utilizado los distintos tipos de variables y operadores disponibles en el lenguaje.
*   **c)** Se han identificado los ámbitos de utilización de las variables.
*   **d)** Se han reconocido y comprobado las peculiaridades del lenguaje respecto a las conversiones entre distintos tipos de datos.
*   **e)** Se han utilizado mecanismos de decisión en la creación de bloques de sentencias.
*   **f)** Se han utilizado bucles y se ha verificado su funcionamiento.
*   **g)** Se han añadido comentarios al código.
*   **h)** Se han utilizado herramientas y entornos para facilitar la programación, prueba y documentación del código.

**Competencias**
*   **Profesionales:** g), q).
*   **Ocupación:** m), n).

### 3. Organización
**Contenidos**
*   Tipos de datos en JavaScript: primitivos (number, string, boolean, null, undefined, symbol, bigint) y objetos.
*   Variables: `var`, `let`, `const`. Ámbito léxico y de bloque.
*   Operadores: aritméticos, de comparación, lógicos, de asignación, ternario y de encadenamiento opcional.
*   Conversiones de tipo: implícitas (coerción) y explícitas. Particularidades de JavaScript.
*   Estructuras de control: `if/else`, `switch`, operador ternario.
*   Bucles: `for`, `while`, `do...while`, `for...of`, `for...in`.
*   Comentarios y buenas prácticas de estilo: JSDoc básico.
*   Herramientas: consola de DevTools, linting con ESLint, formateado con Prettier.

**Metodología**
*   Metodologías activas (WebApp). El equipo comienza a escribir los primeros módulos de lógica de la aplicación: validaciones, cálculos y transformaciones de datos, aplicando desde el principio estilo de código limpio y comentado.

**Secuencia (Fases)**
*   **E1:** Tipos de datos, variables y ámbitos: `var` vs. `let` vs. `const`.
*   **E2:** Operadores y coerción de tipos: las rarezas de JavaScript en la práctica.
*   **E3:** Estructuras de control y bucles: lógica de decisión en la app del proyecto.
*   **E4:** Herramientas: ESLint, Prettier y documentación con JSDoc.
*   **E5:** Entrega: módulo de lógica de negocio básico documentado y lintado.

**Recursos**
*   Aula de informática, VS Code, ESLint, Prettier, navegadores modernos, DevTools, documentación MDN Web Docs, fichas de prácticas.

## 4. EVALUACIÓN Y ADAPTACIÓN

### Instrumentos de evaluación
La evaluación será continua y formativa, enfocada en la adquisición de competencias.
*   **Examen Práctico (70%):** Resolución de ejercicios de sintaxis JavaScript en el navegador, evaluado con rúbrica.
*   **Prácticas Obligatorias (30%):** Módulo de lógica documentado y lintado.

### Adaptaciones
*   **Medidas según necesidades:** Las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
*   **DUA:** Se empleará el **Diseño Universal para el Aprendizaje** proporcionando cheatsheets de sintaxis JavaScript y permitiendo la flexibilización de tiempos en las entregas del proyecto.
---

## UP03: JAVASCRIPT. OBJETOS
### 1. Identificación
| Campo | Detalle |
| :--- | :--- |
| **Código** | UP03 |
| **Módulo** | Desarrollo Web en Entorno Cliente (0612) |
| **Duración** | **28 Horas** |
| **Temporalización** | Del **22/10/2025** al **12/11/2025** |

### 2. Fundamentación
**Resultado de Aprendizaje**
*   **RA03.** Escribe código, identificando y aplicando las funcionalidades aportadas por los objetos predefinidos del lenguaje.

**Criterios de Evaluación**
*   **a)** Se han identificado los objetos predefinidos del lenguaje.
*   **b)** Se han analizado los objetos referentes a las ventanas del navegador y los documentos web que contienen.
*   **c)** Se han escrito sentencias que utilicen los objetos predefinidos del lenguaje para cambiar el aspecto del navegador y el documento que contiene.
*   **d)** Se han generado textos y etiquetas como resultado de la ejecución de código en el navegador.
*   **e)** Se han escrito sentencias que utilicen los objetos predefinidos del lenguaje para interactuar con el usuario.
*   **f)** Se han utilizado las características propias del lenguaje en documentos compuestos por varias ventanas.
*   **g)** Se han utilizado mecanismos del navegador web para almacenar información y recuperar su contenido.
*   **h)** Se ha depurado y documentado el código.

**Competencias**
*   **Profesionales:** f), g), i), q).
*   **Ocupación:** m), n).

### 3. Organización
**Contenidos**
*   Objetos globales de JavaScript: `Math`, `Date`, `JSON`, `RegExp`.
*   Objetos del navegador (BOM): `window`, `navigator`, `screen`, `location`, `history`.
*   Interacción con el usuario: `alert`, `confirm`, `prompt`, `console`.
*   Generación dinámica de contenido: `document.write`, `innerHTML`, `textContent`.
*   Ventanas y marcos: `window.open`, `iframe`, comunicación entre ventanas.
*   Almacenamiento en el navegador: `localStorage`, `sessionStorage`, `cookies`.
*   Depuración con DevTools: breakpoints, watch expressions, call stack.
*   Documentación con JSDoc: tipos, parámetros y retornos.

**Metodología**
*   Metodologías activas (WebApp). El equipo amplía la app integrando objetos del navegador: persistencia de datos con localStorage, gestión de fechas y generación dinámica de contenido en función de las acciones del usuario.

**Secuencia (Fases)**
*   **E1:** Objetos globales: Math, Date y JSON en casos reales.
*   **E2:** BOM: window, location, history y almacenamiento en el navegador.
*   **E3:** Generación dinámica de contenido e interacción con el usuario.
*   **E4:** Depuración avanzada con DevTools y documentación JSDoc completa.
*   **E5:** Entrega: módulo de la app con persistencia local y documentación completa.

**Recursos**
*   Aula de informática, VS Code, navegadores modernos, DevTools, documentación MDN Web Docs, fichas de prácticas.

## 4. EVALUACIÓN Y ADAPTACIÓN

### Instrumentos de evaluación
La evaluación será continua y formativa, enfocada en la adquisición de competencias.
*   **Examen Práctico (70%):** Ejercicio con objetos predefinidos en el navegador, evaluado con rúbrica.
*   **Prácticas Obligatorias (30%):** Módulo de la app con localStorage y documentación JSDoc.

### Adaptaciones
*   **Medidas según necesidades:** Las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
*   **DUA:** Se empleará el **Diseño Universal para el Aprendizaje** proporcionando mapas de objetos del BOM y permitiendo la flexibilización de tiempos en las entregas del proyecto.
---

## UP04: JAVASCRIPT. BOM-DOM
### 1. Identificación
| Campo | Detalle |
| :--- | :--- |
| **Código** | UP04 |
| **Módulo** | Desarrollo Web en Entorno Cliente (0612) |
| **Duración** | **28 Horas** |
| **Temporalización** | Del **13/11/2025** al **15/01/2026** |

### 2. Fundamentación
**Resultado de Aprendizaje**
*   **RA04.** Programa código para clientes web analizando y utilizando estructuras definidas por el usuario.

**Criterios de Evaluación**
*   **a)** Se han clasificado y utilizado las funciones predefinidas del lenguaje.
*   **b)** Se han creado y utilizado funciones definidas por el usuario.
*   **c)** Se han reconocido las características del lenguaje relativas a la creación y uso de matrices (arrays).
*   **d)** Se han creado y utilizado matrices (arrays).
*   **e)** Se han utilizado operaciones agregadas para el manejo de información almacenada en colecciones.
*   **f)** Se han reconocido las características de orientación a objetos del lenguaje.
*   **g)** Se ha creado código para definir la estructura de objetos.
*   **h)** Se han creado métodos y propiedades.
*   **i)** Se ha creado código que haga uso de objetos definidos por el usuario.
*   **j)** Se han utilizado patrones de diseño de software.
*   **k)** Se ha depurado y documentado el código.

**Competencias**
*   **Profesionales:** f), g), q).
*   **Ocupación:** m), n).

### 3. Organización
**Contenidos**
*   Funciones: declaración, expresión, arrow functions, parámetros por defecto, rest y spread.
*   Closures y ámbito léxico. Funciones de orden superior.
*   Arrays: creación, acceso y métodos funcionales (`map`, `filter`, `reduce`, `find`, `forEach`).
*   Desestructuración de arrays y objetos. Spread operator.
*   Programación orientada a objetos en JavaScript: prototipos y clases (ES6+).
*   Definición de clases: constructor, métodos, herencia con `extends`, `super`.
*   Módulos ES6: `import` / `export`. Organización del código en ficheros.
*   Patrones de diseño básicos: Module, Singleton, Observer.
*   Depuración y documentación: JSDoc avanzado, generación con TypeDoc.

**Metodología**
*   Metodologías activas (WebApp). El equipo refactoriza la app para aplicar POO y módulos ES6: cada funcionalidad se encapsula en clases bien definidas, reutilizables y documentadas.

**Secuencia (Fases)**
*   **E1:** Funciones avanzadas: closures, arrow functions y funciones de orden superior.
*   **E2:** Arrays y operaciones funcionales: map, filter, reduce en la app real.
*   **E3:** POO en JavaScript: clases, herencia y encapsulación.
*   **E4:** Módulos ES6 y patrones de diseño: refactorización de la app del proyecto.
*   **E5:** Entrega: app modular con clases, documentación TypeDoc y código limpio.

**Recursos**
*   Aula de informática, VS Code, Node.js (para módulos ES6), TypeDoc, navegadores modernos, documentación MDN Web Docs, fichas de prácticas.

## 4. EVALUACIÓN Y ADAPTACIÓN

### Instrumentos de evaluación
La evaluación será continua y formativa, enfocada en la adquisición de competencias.
*   **Examen Práctico (70%):** Supuesto de programación con funciones, arrays y POO, evaluado con rúbrica.
*   **Prácticas Obligatorias (30%):** App refactorizada con clases, módulos ES6 y documentación.

### Adaptaciones
*   **Medidas según necesidades:** Las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
*   **DUA:** Se empleará el **Diseño Universal para el Aprendizaje** proporcionando diagramas UML de las clases del proyecto y plantillas de módulos ES6, y permitiendo la flexibilización de tiempos en las entregas.
---

## UP05: JAVASCRIPT. INTERACTUACIÓN CON EL USUARIO, EVENTOS
### 1. Identificación
| Campo | Detalle |
| :--- | :--- |
| **Código** | UP05 |
| **Módulo** | Desarrollo Web en Entorno Cliente (0612) |
| **Duración** | **28 Horas** (RA05: 10 h · RA06: 10 h · RA07: 8 h) |
| **Temporalización** | Del **16/01/2026** al **16/02/2026** |

### 2. Fundamentación
**Resultados de Aprendizaje**
*   **RA05.** Desarrolla aplicaciones web interactivas integrando mecanismos de manejo de eventos.
*   **RA06.** Desarrolla aplicaciones web analizando y aplicando las características del modelo de objetos del documento.
*   **RA07.** Desarrolla aplicaciones web dinámicas, reconociendo y aplicando mecanismos de comunicación asíncrona entre cliente y servidor.

**Criterios de Evaluación**
*   **RA05. a)** Se han reconocido las posibilidades del lenguaje de marcas relativas a la captura de los eventos producidos.
*   **RA05. b)** Se han identificado las características del lenguaje de programación relativas a la gestión de los eventos.
*   **RA05. c)** Se han diferenciado los tipos de eventos que se pueden manejar.
*   **RA05. d)** Se ha creado código que capture y utilice eventos.
*   **RA05. e)** Se han reconocido las capacidades del lenguaje relativas a la gestión de formularios web.
*   **RA05. f)** Se han validado formularios web utilizando eventos.
*   **RA05. g)** Se han utilizado expresiones regulares para facilitar los procedimientos de validación.
*   **RA05. h)** Se ha probado y documentado el código.
*   **RA06. a)** Se ha reconocido el modelo de objetos del documento de una página web.
*   **RA06. b)** Se han identificado los objetos del modelo, sus propiedades y métodos.
*   **RA06. c)** Se ha creado y verificado un código que acceda a la estructura del documento.
*   **RA06. d)** Se han creado nuevos elementos de la estructura y modificado elementos ya existentes.
*   **RA06. e)** Se han asociado acciones a los eventos del modelo.
*   **RA06. f)** Se han identificado las diferencias que presenta el modelo en diferentes navegadores.
*   **RA06. g)** Se han programado aplicaciones web de forma que funcionen en navegadores con diferentes implementaciones del modelo.
*   **RA06. h)** Se han independizado las tres capas de implementación (contenido, aspecto y comportamiento) en aplicaciones web.
*   **RA07. a)** Se han evaluado las ventajas e inconvenientes de utilizar mecanismos de comunicación asíncrona entre cliente y servidor web.
*   **RA07. b)** Se han analizado los mecanismos disponibles para el establecimiento de la comunicación asíncrona.
*   **RA07. c)** Se han utilizado los objetos relacionados.
*   **RA07. d)** Se han identificado sus propiedades y sus métodos.
*   **RA07. e)** Se ha utilizado comunicación asíncrona en la actualización dinámica del documento web.
*   **RA07. f)** Se han utilizado distintos formatos en el envío y recepción de información.
*   **RA07. g)** Se han programado aplicaciones web asíncronas de forma que funcionen en diferentes navegadores.
*   **RA07. h)** Se han clasificado, analizado y utilizado librerías y frameworks que faciliten la incorporación de las tecnologías de actualización dinámica.
*   **RA07. i)** Se han creado, probado y documentado aplicaciones web que utilicen estas librerías y frameworks.

**Competencias**
*   **Profesionales:** f), g), i), q).
*   **Ocupación:** k), m), n), p).

### 3. Organización
**Contenidos**

*RA05 – Eventos*
*   Modelo de eventos del DOM: captura, target y burbujeo.
*   `addEventListener` y `removeEventListener`. Delegación de eventos.
*   Tipos de eventos: ratón, teclado, formulario, foco, carga, drag & drop.
*   Gestión de formularios web: acceso a campos, envío y cancelación.
*   Validación con eventos: `input`, `change`, `submit`, `blur`.
*   Expresiones regulares en JavaScript: patrones de validación comunes.

*RA06 – DOM*
*   El árbol DOM: nodos, elementos, atributos y texto.
*   Selección de elementos: `querySelector`, `querySelectorAll`, `getElementById`.
*   Manipulación del DOM: `createElement`, `appendChild`, `removeChild`, `innerHTML`, `classList`.
*   Modificación de estilos: `style`, `classList.add/remove/toggle`.
*   Separación de capas: HTML (contenido), CSS (aspecto) y JS (comportamiento).
*   Compatibilidad entre navegadores: polyfills y detección de características.

*RA07 – AJAX y asincronía*
*   Programación asíncrona en JavaScript: callbacks, Promises y async/await.
*   Fetch API: peticiones GET, POST, PUT, DELETE. Cabeceras y opciones.
*   Formatos de datos: JSON y FormData.
*   Actualización dinámica del DOM con datos del servidor.
*   CORS: origen cruzado y cabeceras necesarias.
*   Librerías y frameworks: Axios, introducción a React/Vue como consumidores de APIs.

**Metodología**
*   Metodologías activas (WebApp). Sprint final: el equipo completa la app añadiendo interactividad completa mediante eventos y DOM, consumo de una API REST real con Fetch/Axios y actualización dinámica de la interfaz, culminando con la presentación del proyecto.

**Secuencia (Fases)**
*   **E1 (RA05):** Eventos del DOM: captura, delegación y formularios con validación por expresiones regulares.
*   **E2 (RA06):** Manipulación del DOM: selección, creación y modificación de nodos. Separación de capas.
*   **E3 (RA07):** Asincronía: Promises, async/await y Fetch API con una API REST real.
*   **E4 (RA07):** Formatos de datos, CORS y uso de Axios. Actualización dinámica del DOM.
*   **E5:** Presentación final del proyecto WebApp completo: eventos, DOM y AJAX integrados.

**Recursos**
*   Aula de informática, VS Code, navegadores modernos, DevTools, APIs REST públicas (JSONPlaceholder, OpenWeather), Axios, documentación MDN Web Docs, fichas de prácticas.

## 4. EVALUACIÓN Y ADAPTACIÓN

### Instrumentos de evaluación
La evaluación será continua y formativa, enfocada en la adquisición de competencias.
*   **Examen Práctico (70%):** Supuesto integrador con eventos, DOM y AJAX, evaluado con rúbrica.
*   **Prácticas Obligatorias (30%):** Proyecto WebApp completo con eventos, manipulación del DOM y consumo de API, incluye presentación oral.

### Adaptaciones
*   **Medidas según necesidades:** Las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
*   **DUA:** Se empleará el **Diseño Universal para el Aprendizaje** proporcionando plantillas de código con la estructura de eventos y Fetch preconfigurada, y permitiendo la flexibilización de tiempos en la entrega y presentación final del proyecto.

