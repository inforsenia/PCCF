# Unidades de programación: 190 Módulo Optativo - Introducción a la Programación (2025-2026)


### Resumen de Unidades de Programación (Curso 2025-2026)

| Código | Nombre de la UP | Duración (Horas Centro) | Temporalización | RAs Asociados |
| :--- | :--- | :--- | :--- | :--- |
| **UP01** | Introducción a la programación y Python | 5h | 10/09/2025 – 17/09/2025 | **RA01** |
| **UP02** | Python básico  | 9h | 19/09/2025 – 17/10/2025 | **RA03** |
| **UP03** | Funciones y programación modular en Python | 9h | 17/10/2025 – 7/11/2025 | **RA03**|
| **UP04** | Tratamiento de excepciones, ficheros | 5h | 7/11/2025 – 21/11/2025 | **RA3, RA5** |
| **UP05** | POO (Programación Orientada a Objetos) | 9h | 21/11/2025 – 12/12/2025 | **RA2 y RA4** |
| **UP06** | Acceso a BBDD | 9h | 12/12/2025 – 16/01/2026 | **RA05** |
| **UP07** | Estructuras de datos avanzadas. Intercambio de datos | 5h | 16/01/2026 - 30/01/2026 | **RA06** |
| **UP08** | Frameworks de Python: Django | 5h | 30/01/2026 - 13/02/2026 | **RA01** |
| **UP09** | Python en la administración de sistemas | 2h | 13/02/2026 - 13/02/2026 | **RA01** |



<!-- continuar -->
## UP01: Introducción a las aplicaciones Web. Conceptos y tecnologías previas
### 1. Identificación
*   **Código:** UP01 | **Módulo:** 0376
*   **Duración:** 10 horas.
*   **Temporalización:** 08/09/2025 – 26/09/2025.

### 2. Fundamentación (Real Decreto 1629/2009)

* **Resultado de Aprendizaje:** 
    * **RA1:** Instala servidores web, analizando sus características y configurando sus parámetros funcionales *(enfocado aquí en la preparación del entorno, control de versiones y virtualización ligera necesaria para el despliegue)*.
* **Criterios de Evaluación:**
    * **a)** Se han identificado las tecnologías de desarrollo y despliegue de aplicaciones web, así como la arquitectura cliente-servidor.
    * **b)** Se han utilizado sistemas de control de versiones para la gestión, seguimiento y documentación del código fuente del proyecto.
    * **c)** Se han configurado contenedores virtuales mediante tecnologías de virtualización ligera para preparar el entorno base de implantación.


* **Competencias:**
    * **Profesionales:** Configurar e implantar entornos de desarrollo y despliegue web aislados, garantizando la trazabilidad del código mediante sistemas de control de versiones descentralizados.
    * **Empleabilidad:** Capacidad de autoaprendizaje ante herramientas tecnológicas emergentes, rigor en la documentación técnica y destreza en la organización de flujos de trabajo colaborativos.

### 3. Organización
*   **Contenidos (Orden 36/2012):** 
    <!-- RELLENAR -->
*   **Teoría:** 
    * Conceptos básicos de la arquitectura web cliente-servidor.
    * Sistemas de control de versiones distribuidos (Git): estructura de repositorios, gestión de ramas, confirmaciones (`commits`), fusión (`merges`) y resolución manual de conflictos.
    * Introducción a la contenedorización y virtualización ligera (Docker) aplicada al aislamiento de microservicios.
    * Lenguajes de marcado y formatos de serialización de datos para configuración (Markdown y YAML).

*   **Metodología:** Metodologías activas con tareas y actividades basadas en el proyecto [Terraformadores de Venus](https://inforsenia.github.io/Terraformadores).
*   **Secuencia (Fases):**
    * [Tarea 1 - Introducción a la documentación con Markdown](https://inforsenia.github.io/Terraformadores/v3/Markdown/Tarea1)
    * [Tarea 2 - Introducción a Git y GitHub](https://inforsenia.github.io/Terraformadores/v3/Git/Tarea1)
    * [Tarea 3 - Git. Trabajando con Ramas](https://inforsenia.github.io/Terraformadores/v3/Git/Tarea2)
    * [Tarea 4 - Introducción a Docker](https://inforsenia.github.io/Terraformadores/v3/Docker/Tarea1Docker)
    * [Tarea 5 - YAML. Sintaxis y estructuras de datos](https://inforsenia.github.io/Terraformadores/v3/YAML/Tarea1YAML)

    

### 4. Recursos Tecnológicos
*   **Base Tecnológica:** 
    * Docker
    * Entorno de Desarrollo Codium
    * git, GitHub, GitLab

### 5. Evaluación y Adaptación
*   **Instrumentos:** Tareas realizadas en el proyecto [Terraformadores de Venus](https://inforsenia.github.io/Terraformadores) (100%). Observación directa de la participación en las actividades y tareas. Evaluación de los entregables y documentación generada.
*   **Adaptaciones:** Aplicación de Diseño Universal para el Aprendizaje (DUA) y ritmos flexibles según necesidades detectadas. 

---

## UP02: Instalación y configuración de un entorno web
### 1. Identificación
*   **Código:** UP02 | **Módulo:** 0376
*   **Duración:** 16 horas.
*   **Temporalización:** 01/10/2025 – 31/10/2025.

### 2. Fundamentación (Real Decreto 1629/2009)
* **Resultado de Aprendizaje:**
    * **RA1:** Instala servidores web, analizando sus características y configurando sus parámetros funcionales.


* **Criterios de Evaluación:**
    * **a)** Se ha instalado el servidor web y sus módulos asociados en sistemas locales y entornos virtuales.
    * **b)** Se han configurado los parámetros funcionales del servidor (puertos de escucha, directorios base, hosts virtuales y niveles de seguridad).
    * **c)** Se han desplegado entornos web multi-servicio utilizando herramientas de orquestación de contenedores y plataformas de infraestructura en la nube.


* **Competencias:**
    * **Profesionales:** Desplegar, configurar y administrar servidores web y motores de bases de datos relacionales, garantizando la interconectividad de servicios tanto en infraestructuras locales como virtuales o cloud.
    * **Empleabilidad:** Adaptabilidad a plataformas de computación en la nube (Cloud Computing), optimización de recursos lógicos y capacidad de resolución autónoma de problemas de red y conectividad.



### 3. Organización

* **Contenidos (Orden 36/2012):**
    * Servidores web (Apache y Nginx): instalación, estructura de directorios, configuración de directivas y hosts virtuales.
    * Arquitectura multi-capa de servicios web (pila LAMP/WAMP): integración del servidor web, motor de datos y el intérprete de lenguaje de servidor.
    * Configuración y despliegue automatizado de entornos multi-contenedor mediante herramientas de orquestación (Docker Compose).
    * Despliegue de infraestructura web y aprovisionamiento en la nube bajo el modelo IaaS (Amazon Web Services - AWS).


*   **Metodología:** Metodologías activas con tareas y actividades basadas en el proyecto [Terraformadores de Venus](https://inforsenia.github.io/Terraformadores).
*   **Secuencia (Fases):**
    * Tarea 1: LAMP Básico. Instalación y configuración de Apache, MySQL/MariaDB y PHP como servicios en una máquina local.
    * Tarea 2: LAMP con Docker en una máquina local. Instalación y configuración de Apache, MySQL/MariaDB y PHP como servicios en contenedores Docker.
    * Tarea 3: LAMP en AWS en una máquina: Instalación y configuración de Apache, MySQL/MariaDB y PHP como servicios en una máquina virtual en la nube de AWS.

### 4. Recursos Tecnológicos
*    Docker, Entorno de Desarrollo Codium, git, GitHub, GitLab, Nginx, Apache, MySQL, MariaDB, PostgreSQL, PHP.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Tareas realizadas en el proyecto [Terraformadores de Venus](https://inforsenia.github.io/Terraformadores) (100%). Observación directa de la participación en las actividades y tareas. Evaluación de los entregables y documentación generada.
*   **Adaptaciones:** Aplicación de Diseño Universal para el Aprendizaje (DUA) y ritmos flexibles según necesidades detectadas. 

---

## UP03: PROGRAMACIÓN BÁSICA DE APLICACIONES CON PHP
### 1. Identificación
*   **Código:** UP03 | **Módulo:** 0376
*   **Duración:** 12 horas.
*   **Temporalización:** 01/11/2025 – 21/11/2025.

### 2. Fundamentación (Real Decreto 1629/2009)

* **Resultado de Aprendizaje:**
    * **RA5:** Programa scripts de servidor, analizando la sintaxis del lenguaje y las tecnologías integradas.


* **Criterios de Evaluación:**
    * **a)** Se ha reconocido la estructura básica de un script de servidor, sus etiquetas de integración y las herramientas de depuración de código.
    * **b)** Se han utilizado variables, constantes, operadores y tipos de datos simples en la resolución de problemas lógicos y aritméticos.
    * **c)** Se han empleado estructuras de control condicionales y bucles de repetición para guiar el flujo de ejecución del programa.
    * **d)** Se han desarrollado funciones de usuario y manipulado arrays asociativos para procesar y validar los datos enviados a través de formularios web.


* **Competencias:**
    * **Profesionales:** Desarrollar scripts de programación del lado del servidor para procesar peticiones HTTP, capturar datos de formularios web y ejecutar la lógica de negocio básica de una aplicación.
    * **Empleabilidad:** Pensamiento analítico y resolución de problemas algorítmicos, rigor lógico y atención al detalle en la traza y depuración de errores lógicos de software.



### 3. Organización

* **Contenidos (Orden 36/2012):**
    * Introducción a los lenguajes de programación del lado del servidor: características y bloques de código integrados en código de marcas.
    * Sintaxis básica del lenguaje (PHP): tipos de datos, variables, constantes y operadores aritmético-lógicos.
    * Estructuras de control de flujo: bifurcaciones condicionales y bucles iterativos.
    * Estructuras de datos complejas: arrays indexados, arrays asociativos y funciones de manipulación.
    * Captura y tratamiento de la información de entrada: procesamiento seguro de formularios web utilizando métodos de transferencia HTTP.
*   **Teoría:**  
    Lenguaje PHP Básico. Sintaxis básica y avanzada. Tipos de datos, variables, constantes, operadores, estructuras de control, funciones, arrays.
*   **Metodología:** Metodologías activas con tareas y actividades
*   **Secuencia (Fases):**
    * Tarea 1: Boletin de ejercicios de PHP. Sintaxis básica y avanzada. Tipos de datos, variables, constantes, operadores, estructuras de control, funciones, arrays, arrays asociativos, manejo de formularios y validación de datos.
    * Tarea 2: Programa PHP completo. Desarrollo de un programa básico y completo en PHP que integre todos los conceptos aprendidos en la tarea 1. Manejo de formularios, validación de datos, arrays y funciones.

### 4. Recursos Tecnológicos
*    PHP, Docker, Entorno de Desarrollo Codium, git, GitHub, GitLab, Nginx, Apache.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Prueba objetiva (100%).
*   **Adaptaciones:** Flexibilización de tiempos y materiales de apoyo en Aules.

---

## UP04: NOCIONES AVANZADAS SOBRE EL LENGUAJE PHP
### 1. Identificación
*   **Código:** UP04 | **Módulo:** 0376
*   **Duración:** 12 horas.
*   **Temporalización:** 25/11/2025 – 12/12/2025.

### 2. Fundamentación (Real Decreto 1629/2009)

* **Resultado de Aprendizaje:**
    * **RA6:** Desarrolla aplicaciones web dinámicas con acceso a bases de datos, utilizando técnicas de programación seguras.


* **Criterios de Evaluación:**
    * **a)** Se han aplicado los principios del paradigma de la programación orientada a objetos (clases, objetos, métodos y propiedades) en scripts de servidor.
    * **b)** Se ha establecido la conexión entre la aplicación web y el gestor de bases de datos utilizando capas de abstracción seguras (PDO).
    * **c)** Se han desarrollado scripts interactivos capaces de realizar operaciones completas de manipulación de datos (CRUD: altas, bajas, modificaciones y consultas).
    * **d)** Se han implementado mecanismos de control de estado y acceso (sesiones y cookies) aplicando criterios estrictos de validación y sanitización de datos.


* **Competencias:**
    * **Profesionales:** Desarrollar aplicaciones web dinámicas conectadas de forma robusta y segura a sistemas de gestión de bases de datos relacionales, garantizando la persistencia de los datos y blindando el software contra ataques maliciosos.
    * **Empleabilidad:** Compromiso con la seguridad de la información y la protección de datos, diseño técnico estructurado y visión integradora de sistemas multi-tecnología.



### 3. Organización

* **Contenidos (Orden 36/2012):**
    * Programación Orientada a Objetos avanzada del lado del servidor (clases, instanciación, métodos y encapsulamiento).
    * Mecanismos de conectividad con gestores de bases de datos relacionales mediante objetos de datos de PHP (PDO).
    * Desarrollo práctico de operaciones persistentes (CRUD) sobre tablas relacionales.
    * Gestión del estado en entornos web desinteresados: configuración y administración de sesiones de usuario y cookies.
    * Programación web segura: técnicas de validación en servidor, sanitización de cadenas y uso obligatorio de sentencias preparadas para mitigar inyecciones SQL y ataques XSS.

*   **Teoría:**  
    * El lenguaje PHP Avanzado. Sintaxis avanzada. Programación orientada a objetos, clases. Manejo de excepciones y errores. Manejo de sesiones y cookies. Seguridad en aplicaciones web con PHP.
*   **Metodología:** Metodologías activas con tareas y actividades
*   **Secuencia (Fases):**
    * Tarea 1: POO en PHP. Ejercicios básicos.
    * Tarea 2: Acceso a datos. CRUD en PHP. Desarrollo de un programa PHP con acceso a base de datos MySQL/MariaDB. Creación de tablas, inserción, actualización y eliminación de datos. Manejo de consultas y resultados.

### 4. Recursos Tecnológicos
*    PHP, Docker, Entorno de Desarrollo Codium, git, GitHub, GitLab, Nginx, Apache, MySQL, MariaDB, PostgreSQL.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Prueba objetiva (100%).
*   **Adaptaciones:** Flexibilización de tiempos y materiales de apoyo en Aules.

---

## UP05: Introducción a la integración continua y despliegue continuo
### 1. Identificación
*   **Código:** UP05 | **Módulo:** 0376
*   **Duración:** 12 horas.
*   **Temporalización:** 16/12/2025 – 23/01/2026.

### 2. Fundamentación (Real Decreto 1629/2009)

* **Resultado de Aprendizaje:** 
    * **RA1:** Instala servidores web, analizando sus características y configurando sus parámetros funcionales.

* **Criterios de Evaluación:**
    * **a)** Se han analizado los conceptos fundamentales de la Integración Continua y el Despliegue Continuo (CI/CD) dentro del ciclo de vida del software.
    * **b)** Se ha instalado, configurado y administrado un servidor de automatización (Jenkins) y su infraestructura distribuidora de nodos de ejecución.
    * **c)** Se han desarrollado flujos de despliegue automatizados mediante archivos de configuración (`Jenkinsfile`), integrando etapas secuenciales de descarga de código, copia física de producción y pruebas automáticas de conectividad (`health check`).


* **Competencias:**
    * **Profesionales:** Automatizar por completo el ciclo de puesta en producción de aplicaciones web mediante herramientas de integración continua, minimizando la manipulación manual de ficheros y controlando la calidad del servicio.
    * **Empleabilidad:** Mentalidad y cultura DevOps, enfoque proactivo hacia la eficiencia y la automatización de procesos industriales repetitivos, y resiliencia en la resolución de fallos críticos de despliegue en cadena.



### 3. Organización

* **Contenidos (Orden 36/2012):**
    * Fundamentos de Integración Continua (CI) y Despliegue Continuo (CD). El flujo de entrega de software.
    * Servidores de automatización (Jenkins): instalación, gestión del espacio de trabajo (`workspace`), plugins esenciales y arquitectura distribuida máster-nodo.
    * Configuración de pipelines declarativos a través de scripts de control (`Jenkinsfile`): etapas (`stages`), tareas (`steps`) y bloques condicionales pos-ejecución (`post-actions`).
    * Mecanismos automatizados de monitorización básica del estado del servicio y auditoría de conectividad (`health checks` mediante comandos nativos como `curl`).

*   **Teoría:**  
    Introducción a la integración continua y despliegue continuo. Conceptos y herramientas. Configuración de pipelines de integración continua y despliegue continuo con Jenkins. Automatización de pruebas y despliegues. Monitoreo y notificaciones.
*   **Metodología:** Metodologías activas con tareas y actividades
*   **Secuencia (Fases):**
    * Tarea 1: Introducción a la integración continua con Jenkins. Instalación y configuración de Jenkins. Creación de jobs bñasicos.
    * Tarea 2: Job de integración continua con Jenkins. Configuración de un job de integración continua para un proyecto PHP. Automatización de desplijegue.
    * Tarea 3: Pipeline de integración continua y despliegue continuo con Jenkins. Configuración de un pipeline completo para un proyecto PHP. Automatización de despliegues.
    * Tarea 4: Creación de nodos en Jenkins. Configuración de nodos para la ejecución de jobs y pipelines. Distribución de cargas y escalabilidad.
    * Tarea final: Proyecto final de integración continua y despliegue continuo. Desarrollo de un proyecto completo con integración continua y despliegue continuo utilizando Jenkins.

### 4. Recursos Tecnológicos
*   **Herramientas:** Jenkins, Docker, Entorno de Desarrollo Codium, PHP, git, GitHub, GitLab, Nginx, Apache, MySQL, MariaDB, PostgreSQL.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Tareas realizadas en Aules (100%). Observación directa de la participación en las actividades y tareas. Evaluación de los entregables y documentación generada.
*   **Adaptaciones:** Aplicación de Diseño Universal para el Aprendizaje (DUA) y ritmos flexibles según necesidades detectadas. 


---

## UP06: Implantación y administración de gestores de contenidos
### 1. Identificación
*   **Código:** UP06 | **Módulo:** 0376
*   **Duración:** 16 horas.
*   **Temporalización:** 24/01/2026 – 13/02/2026.

### 2. Fundamentación (Real Decreto 1629/2009)

* **Resultado de Aprendizaje:**
    * **RA2:** Instala gestores de contenidos, analizando sus características y adaptándolos a las especificaciones recibidas.
    * **RA3:** Gestiona gestores de contenidos, configurando sus parámetros y garantizando la integridad de la información.
    * **RA7:** *(O el código de RA complementario que use vuestro decreto autonómico para la auditoría y mantenimiento de portales web).*


* **Criterios de Evaluación:**
    * **a)** Se han analizado los requerimientos técnicos y se ha realizado la instalación de sistemas de gestión de contenidos (CMS) sobre la infraestructura web.
    * **b)** Se han adaptado e instalado extensiones, complementos (`plugins`) y temas para personalizar la apariencia y la funcionalidad del gestor de contenidos.
    * **c)** Se han configurado y administrado los perfiles de usuario, estableciendo roles, permisos y políticas de control de acceso al sistema.
    * **d)** Se han planificado y ejecutado operaciones periódicas de mantenimiento correctivo, actualizaciones del núcleo corporativo y políticas de copias de seguridad de los datos.


* **Competencias:**
    * **Profesionales:** Desplegar, parametrizar y administrar gestores de contenidos web (CMS), garantizando la seguridad del portal, el control granular de usuarios y la integridad de las bases de datos asociadas mediante copias de seguridad sistemáticas.
    * **Empleabilidad:** Orientación al cliente y al usuario final, capacidad organizativa en planes de mantenimiento preventivo y rigor técnico en la protección y salvaguarda de activos digitales.



### 3. Organización

* **Contenidos (Orden 36/2012):**
    * Sistemas de gestión de contenidos (CMS): tipologías, arquitectura interna, requisitos del sistema y criterios de selección (WordPress, Joomla, Drupal).
    * Procesos de implantación y despliegue del CMS: configuración del instalador, conexión de la base de datos y estructura de ficheros en el servidor.
    * Técnicas de personalización y extensibilidad: instalación y administración avanzada de módulos, componentes, complementos y plantillas estéticas.
    * Gestión de usuarios: control de accesos, creación de roles, asignación de privilegios y moderación del entorno corporativo.
    * Tareas de administración del sistema: actualización del núcleo y componentes, monitorización de la seguridad del sitio y automatización de procesos de copia de seguridad (`backup`) y restauración catastrófica.


*   **Teoría:**  
    Introducción a los gestores de contenidos (CMS). Instalación y configuración de gestores de contenidos. Administración y gestión de contenidos. Seguridad y mantenimiento de gestores de contenidos.
*   **Metodología:** Metodologías activas con tareas y actividades
*   **Secuencia (Fases):**
    * Tarea 1: Instalación y configuración de un gestor de contenidos (WordPress, Joomla, Drupal). Instalación y configuración de un gestor de contenidos en un entorno local o en la nube. Configuración de temas y plugins. Creación de usuarios y roles.
    * Tarea 2: Administración y gestión de contenidos. Creación y edición de contenidos. Gestión de medios y archivos. Configuración de menús y widgets. Gestión de comentarios y usuarios.
    * Tarea 3: Seguridad y mantenimiento de gestores de contenidos. Configuración de copias de seguridad y actualizaciones. Gestión de permisos y roles. Monitoreo y auditoría de seguridad.

### 4. Recursos Tecnológicos
*   **Herramientas:** WordPress, Joomla, Drupal, Docker, Nginx, Apache, MySQL, MariaDB, PostgreSQL, PHP, git, GitHub, GitLab.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Tareas realizadas en el proyecto [Terraformadores de Venus](https://inforsenia.github.io/Terraformadores) (100%). Observación directa de la participación en las actividades y tareas. Evaluación de los entregables y documentación generada.
*   **Adaptaciones:** Aplicación de Diseño Universal para el Aprendizaje (DUA) y ritmos flexibles según necesidades detectadas. 


---

## UP07: Implantación de aplicaciones de ofimática web

### 1. Identificación
*   **Código:** UP07 | **Módulo:** 0376
*   **Duración:** 0,5 horas.
*   **Temporalización:** 13/02/2026.

### 2. Fundamentación (Real Decreto 1629/2009)

* **Resultado de Aprendizaje:**
    * **RA4:** Instala y configura aplicaciones de ofimática web, garantizando su funcionalidad y la integración con otras aplicaciones.


* **Criterios de Evaluación:**
    * **a)** Se han identificado las características, tipologías y ventajas operativas de las plataformas de ofimática web y soluciones de almacenamiento en la nube privada.
    * **b)** Se ha implantado una solución integrada de ofimática web en un servidor corporativo asegurando la accesibilidad a los recursos.
    * **c)** Se han integrado servidores de edición de documentos en tiempo real y configurado las directivas de uso compartido seguro y cuotas de almacenamiento de los usuarios.


* **Competencias:**
    * **Profesionales:** Desplegar y administrar suites de ofimática web colaborativa y soluciones de almacenamiento virtual alojadas en servidores propios, integrando herramientas de productividad remota y asegurando la soberanía del dato empresarial.
    * **Empleabilidad:** Fomento del trabajo colaborativo en entornos corporativos, visión estratégica en soluciones tecnológicas centralizadas y optimización de flujos de productividad digital empresarial.



### 3. Organización

* **Contenidos (Orden 36/2012):**
    * Modelos de servicios en la nube aplicados al almacenamiento virtual (*cloud storage*) y la productividad ofimática web.
    * Instalación y configuración de suites de ofimática web auto-alojadas (*self-hosted* como Nextcloud).
    * Integración y acoplamiento de servidores de procesamiento de documentos y edición colaborativa en tiempo real (OnlyOffice o Collabora Online).
    * Administración avanzada de recursos compartidos: cuotas de almacenamiento en disco, gestión de enlaces públicos de descarga, permisos de edición y control de accesos corporativos.
    
*   **Teoría:**  
    Implantación de aplicaciones de ofimática web. Instalación y configuración de aplicaciones de ofimática web (Nextcloud, OnlyOffice, Collabora Online). Integración con gestores de contenidos y servicios en la nube.
*   **Metodología:** Clase magistral breve con una demostración y una actividad práctica.
*   **Secuencia (Fases):**
    * Tarea 1 - Instalación y configuración de una aplicación de ofimática web (Nextcloud, OnlyOffice, Collabora Online).

### 4. Recursos Tecnológicos
*   **Base Tecnológica:** Office 365, Nextcloud,Apache.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Observación directa de la participación en las actividades y tareas. Evaluación de los entregables y documentación generada.
*   **Adaptaciones:** Flexibilización de tiempos y materiales de apoyo en Aules.
