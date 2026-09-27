# PROGRAMACIÓN DIDÁCTICA: DESPLIEGUE DE APLICACIONES WEB (0614)

### Resumen de Unidades de Programación (Curso 2026-2027)

| Código | Título de la UP | 
| :--- | :--- | 
| **UP01** | **Arquitecturas web y servidores web** | 
| **UP02** | **Seguridad en servidores web** | 
| **UP03** | **Contenedores y servidores de aplicaciones** |
| **UP04** | **Servicios de red y transferencia de archivos** | 
| **UP05** | **Documentación e Integración continua** | 


*   La suma total de estas unidades es de **100 horas**, correspondientes íntegramente al periodo de formación realizado en el centro educativo fuera del periodo dual.


---

## UP01: Arquitecturas web y servidores web

### 1. Identificación

| Campo | Detalle |
| :--- | :--- |
| **Código** | UP01 |
| **Módulo** | Despliegue de aplicaciones web (0614) |
| **Duración** | **9 Horas** |
| **Temporalización** | Del **14/09/2026** al **28/09/2026** |

### 2. Fundamentación

**Resultado de Aprendizaje**

* **RA01.** Implanta arquitecturas web analizando y aplicando criterios de funcionalidad.

**Criterios de Evaluación**

* **a)** Se han analizado aspectos generales de arquitecturas web, sus características, ventajas e inconvenientes.
* **b)** Se han descrito los fundamentos y protocolos en los que se basa el funcionamiento de un servidor web.
* **c)** Se ha realizado la instalación y configuración básica de servidores web.
* **f)** Se han realizado pruebas de funcionamiento de los servidores web y de aplicaciones y de tecnologías de virtualización en la nube y en contenedores.
* **g)** Se ha analizado la estructura y recursos que componen una aplicación web.
* **h)** Se han descrito los requerimientos del proceso de implantación de una aplicación web.
* **i)** Se han documentado los procesos de instalación y configuración realizados sobre los servidores web, de aplicaciones y sobre tecnologías de virtualización en la nube y en contenedores.

**Competencias**

* **Profesionales:** a), b), c), j), n), ñ), q).
* **Ocupación:** c), d), o), p), r).

### 3. Organización

**Contenidos**

* Introducción al despliegue de aplicaciones web: concepto de despliegue, servidores y servicios necesarios para publicar una aplicación web.
* Arquitecturas web: modelo cliente-servidor y evolución de las arquitecturas web.
* Arquitecturas de una capa, dos capas y tres capas.
* Servidores web y servidores de aplicaciones: funciones, características y diferencias.
* Principales servidores web: Apache HTTP Server, Nginx y otros servidores de referencia.
* Protocolo HTTP: funcionamiento de una comunicación cliente-servidor.
* Peticiones y respuestas HTTP: métodos, cabeceras, códigos de estado y contenido.
* URL, recursos web y puertos.
* Instalación de Apache HTTP Server en Ubuntu Server.
* Estructura de directorios y principales archivos de configuración de Apache.
* Directiva `DocumentRoot`: localización y publicación de los recursos de una aplicación web.
* Módulos de Apache: concepto, activación, desactivación y función de los principales módulos.
* Sitios web y *Virtual Hosts*: concepto y utilidad.
* Creación y configuración básica de un *Virtual Host*.
* Estructura de los directorios `sites-available` y `sites-enabled`.
* Activación y desactivación de sitios mediante `a2ensite` y `a2dissite`.
* Comprobación de la configuración de Apache mediante `apache2ctl`.
* Gestión del servicio Apache mediante `systemctl`.
* Registros de Apache: *access log* y *error log*.
* Pruebas de funcionamiento: acceso desde el propio servidor y desde otros equipos de la red.
* Documentación de los procesos de instalación, configuración, pruebas y resolución de incidencias.

**Metodología**

* Metodologías activas centradas en el alumnado. El aprendizaje se organiza en torno a **prácticas guiadas de instalación, configuración y administración de un servidor web**, donde el estudiante construye progresivamente un entorno de despliegue funcional en Ubuntu Server. Los conceptos teóricos se introducen de forma vinculada a las necesidades que aparecen durante las prácticas, favoreciendo la experimentación, la resolución de problemas y la documentación de los procedimientos realizados.

**Secuencia de actividades**

* **A1:** Introducción al despliegue de aplicaciones web. Identificación de los elementos que intervienen en una arquitectura web y análisis de los modelos cliente-servidor, dos capas y tres capas.
* **A2:** Funcionamiento de la Web. Análisis del proceso completo de una petición HTTP desde el cliente hasta el servidor y estudio de URL, métodos HTTP, códigos de respuesta, cabeceras y puertos.
* **A3:** Preparación del servidor Ubuntu Server. Configuración básica del entorno de trabajo, actualización del sistema, identificación de la dirección IP y comprobación de la conectividad de red.
* **A4:** Instalación de Apache HTTP Server. Instalación del servidor, gestión del servicio mediante `systemctl`, comprobación de su funcionamiento y primer acceso desde un navegador web.
* **A5:** Configuración básica de Apache. Análisis de la estructura de configuración, modificación del `DocumentRoot` y publicación de recursos HTML.
* **A6:** Módulos y sitios virtuales. Identificación de módulos de Apache, activación y desactivación de módulos y creación de un *Virtual Host* para publicar una aplicación web independiente.
* **A07:** Proyecto práctico de despliegue. Instalación y configuración completa de Apache, creación de un sitio web mediante un *Virtual Host*, publicación de la aplicación, realización de pruebas de funcionamiento y análisis de los registros generados.
* **A08:** Documentación del despliegue. Elaboración de una guía técnica con los pasos realizados, archivos de configuración modificados, comandos utilizados, pruebas realizadas y principales incidencias encontradas y resueltas.

**Recursos**

* Equipos del aula de informática y máquinas virtuales con Ubuntu Server.
* Servidor web Apache HTTP Server.
* Navegadores web para la realización de pruebas desde los equipos cliente.
* Terminal y herramientas de administración de Ubuntu Server: `systemctl`, `apache2ctl`, `ss`, `curl`, `ip` y herramientas de análisis de logs.
* Aula virtual (Aules) para la distribución de materiales, actividades y documentación.


### 4. Evaluación y adaptación

**Instrumentos de evaluación**

La evaluación será continua y formativa, enfocada en la adquisición de los criterios de evaluación del RA01 y el RA02.

* **Rúbricas de prácticas (40%):** valoración sistemática de la documentación y resultado generados en cada actividad, atendiendo a la corrección técnica, la funcionalidad y configuración conrrectas y la claridad de la documentación.
* **Pruebas objetivas (60%):** prueba teórico-práctica al finalizar el RA para verificar el cumplimiento de los criterios de evaluación.

**Adaptaciones**

* **Medidas según necesidades:** las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
* **DUA:** se empleará el **Diseño Universal para el Aprendizaje**, proporcionando materiales en múltiples formatos y permitiendo la flexibilización de tiempos en las actividades prácticas.

---

## UP02: Seguridad en servidores web

### 1. Identificación

| Campo | Detalle |
| :--- | :--- |
| **Código** | UP02 |
| **Módulo** | Despliegue de aplicaciones web (0614) |
| **Duración** | **12 Horas** |
| **Temporalización** | Del **05/10/2026** al **02/11/2026** |

### 2. Fundamentación

**Resultado de Aprendizaje**

* **RA02.** Implanta aplicaciones web en servidores web, evaluando y aplicando criterios de configuración para su funcionamiento seguro.

**Criterios de Evaluación**

* **a)** Se han reconocido los parámetros de administración más importantes del servidor web.
* **b)** Se ha ampliado la funcionalidad del servidor mediante la activación y configuración de módulos.
* **c)** Se han creado y configurado sitios virtuales.
* **d)** Se han configurado los mecanismos de autenticación y control de acceso del servidor.
* **e)** Se han obtenido e instalado certificados digitales.
* **f)** Se han establecido mecanismos para asegurar las comunicaciones entre el cliente y el servidor.
* **g)** Se ha elaborado documentación relativa a la configuración, administración segura y recomendaciones de uso del servidor.
* **h)** Se han realizado los ajustes necesarios para la implantación de aplicaciones en el servidor web.
* **j)** Se han instalado, configurado y utilizado conjuntos de herramientas de gestión de logs, permitiendo su monitorización, consolidación y análisis en tiempo real.

**Competencias**

* **Profesionales:** a), b), c), j), n), ñ), q).
* **Ocupación:** c), d), o), p), r).

### 3. Organización

**Contenidos**

* Seguridad en servidores web: principios básicos de confidencialidad, integridad, autenticación y control de acceso.
* Usuarios y grupos del sistema: creación, modificación y gestión de usuarios para la administración del servidor.
* Permisos y propietarios de archivos y directorios: `chmod`, `chown` y `chgrp`.
* Permisos de los recursos publicados por el servidor web y relación con el usuario del servicio Apache (`www-data`).
* Autenticación y autorización: diferencias y relación entre ambos conceptos.
* Mecanismos de autenticación disponibles en Apache.
* Autenticación HTTP Basic.
* Ficheros de usuarios y contraseñas para la autenticación.
* Configuración de acceso mediante directivas `Require`.
* Control de acceso a directorios y recursos web.
* Restricción del acceso a determinados recursos mediante usuarios y grupos.
* Certificados digitales: finalidad, estructura y utilización en las comunicaciones seguras.
* Conceptos fundamentales de criptografía aplicada a las comunicaciones web.
* TLS: establecimiento de una comunicación segura entre cliente y servidor.
* HTTPS: funcionamiento y relación entre HTTP y TLS.
* Configuración de HTTPS en Apache mediante el módulo correspondiente.
* Certificados autofirmados para entornos de desarrollo y pruebas.
* Configuración de un sitio web HTTPS mediante *Virtual Host*.
* Redirección de peticiones HTTP hacia HTTPS.
* Configuración de puertos 80 y 443 en el servidor web.
* Configuración segura básica del servidor web: reducción de información innecesaria, permisos adecuados y revisión de módulos y configuración.
* Comprobación de la configuración y sintaxis de Apache.
* Pruebas de autenticación y autorización desde un cliente web.
* Pruebas de acceso HTTP y HTTPS mediante navegador y herramientas de línea de comandos.
* Análisis de los códigos de respuesta relacionados con autenticación y autorización.
* Análisis básico de los registros de Apache para detectar accesos correctos, accesos rechazados y errores de configuración.
* Documentación de la configuración de seguridad y de las pruebas realizadas.

**Metodología**

* Metodologías activas centradas en el alumnado. El aprendizaje se organiza en torno a **prácticas guiadas de securización de un servidor web Apache**. Partiendo del servidor configurado en la unidad anterior, el alumnado introduce progresivamente mecanismos de autenticación, control de acceso y comunicaciones cifradas mediante HTTPS. Las actividades se plantean mediante la configuración de diferentes escenarios de acceso y la posterior realización de pruebas para comprobar qué usuarios pueden acceder a cada recurso y mediante qué protocolo.

**Secuencia de actividades**

* **A1:** Usuarios, grupos y permisos. Creación de usuarios y grupos en Ubuntu Server y configuración de propietarios y permisos sobre los recursos publicados por Apache.
* **A2:** Autenticación básica en Apache. Creación de un directorio protegido mediante autenticación HTTP Basic y configuración de los fichero ficheros de usuarios y grupos y contraseñas.
* **A3:** Certificados digitales y TLS. Análisis del funcionamiento de los certificados digitales y del establecimiento de una comunicación TLS entre cliente y servidor.
* **A4:** Configuración de HTTPS en Apache. Activación de los módulos necesarios, creación o instalación de un certificado para el entorno de prácticas y configuración de un *Virtual Host* HTTPS.
* **A5:** Redirección HTTP → HTTPS. Configuración del servidor para redirigir automáticamente las peticiones recibidas mediante HTTP hacia HTTPS y comprobación del funcionamiento desde el navegador.
* **A6:** Práctica global de securización. Configuración de un servidor Apache que publique una aplicación web, protegiendo determinados recursos mediante autenticación y autorización y estableciendo HTTPS como mecanismo de comunicación segura.
* **A7:** Documentación de la configuración. Elaboración de una guía técnica que recoja los usuarios y permisos configurados, mecanismos de autenticación, certificados, configuración HTTPS, redirecciones, pruebas realizadas y resultados obtenidos.

**Recursos**

* Equipos del aula de informática y máquinas virtuales con Ubuntu Server.
* Servidor web Apache HTTP Server.
* Navegadores web para las pruebas de autenticación, autorización y HTTPS.
* Terminal y herramientas de administración de Ubuntu Server: `chmod`, `chown`, `chgrp`, `systemctl`, `apache2ctl`, `openssl`, `curl` y herramientas de análisis de logs.
* Aula virtual (Aules) para la distribución de materiales, actividades y documentación.
* Servidor y aplicación web desarrollados en la UD01 como punto de partida para las prácticas de securización.

### 4. Evaluación y adaptación

**Instrumentos de evaluación**

La evaluación será continua y formativa, enfocada en la adquisición de los criterios de evaluación del RA02.
* **Rúbricas de prácticas (40%):** valoración sistemática de la documentación y resultado generados en cada actividad, atendiendo a la corrección técnica, la funcionalidad y configuración conrrectas y la claridad de la documentación.
* **Pruebas objetivas (60%):** prueba teórico-práctica al finalizar el RA para verificar el cumplimiento de los criterios de evaluación.

**Adaptaciones**

* **Medidas según necesidades:** las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
* **DUA:** se empleará el **Diseño Universal para el Aprendizaje**, proporcionando materiales en múltiples formatos y permitiendo la flexibilización de tiempos en las actividades prácticas.

---

## UP03: Contenedores y servidores de aplicaciones

### 1. Identificación

| Campo | Detalle |
| :--- | :--- |
| **Código** | UP03 |
| **Módulo** | Despliegue de aplicaciones web (0614) |
| **Duración** | **15 Horas** |
| **Temporalización** | Del **09/11/2026** al **14/12/2026** |

### 2. Fundamentación

**Resultados de Aprendizaje**

* **RA01.** Implanta arquitecturas web analizando y aplicando criterios de funcionalidad.
* **RA03.** Implanta aplicaciones web en servidores de aplicaciones, evaluando y aplicando criterios de configuración para su funcionamiento seguro.

**Criterios de Evaluación**

* **RA01 - e)** Se ha realizado la instalación y configuración básica de tecnologías de virtualización de servidores en la nube y en contenedores.
* **RA01 - f)** Se han realizado pruebas de funcionamiento de los servidores web y de aplicaciones y de tecnologías de virtualización en la nube y en contenedores.
* **RA01 - g)** Se ha analizado la estructura y recursos que componen una aplicación web.
* **RA01 - h)** Se han descrito los requerimientos del proceso de implantación de una aplicación web.
* **RA01 - i)** Se han documentado los procesos de instalación y configuración realizados sobre los servidores web, de aplicaciones y sobre tecnologías de virtualización en la nube y en contenedores.
* **RA03 - a)** Se han descrito los componentes y el funcionamiento de los servicios proporcionados por el servidor de aplicaciones.
* **RA03 - b)** Se han identificado los principales archivos de configuración y de bibliotecas compartidas.
* **RA03 - c)** Se ha configurado el servidor de aplicaciones para cooperar con el servidor web.
* **RA03 - e)** Se han configurado y utilizado los componentes web del servidor de aplicaciones.
* **RA03 - f)** Se han realizado los ajustes necesarios para el despliegue de aplicaciones sobre el servidor.
* **RA03 - g)** Se han realizado pruebas de funcionamiento y rendimiento de la aplicación web desplegada.
* **RA03 - i)** Se han utilizado tecnologías de virtualización en el despliegue de servidores de aplicaciones en la nube y en contenedores.

**Competencias**

* **Profesionales:** a), b), c), j), n), ñ), q).
* **Ocupación:** c), d), o), p), r).

### 3. Organización

**Contenidos**

* Concepto de virtualización: características, ventajas y aplicaciones en el despliegue de servicios.
* Virtualización mediante máquinas virtuales y virtualización mediante contenedores.
* Diferencias entre máquinas virtuales y contenedores.
* Docker: conceptos básicos y arquitectura.
* Imágenes y contenedores: creación, descarga, ejecución, parada y eliminación.
* Puertos y publicación de servicios de un contenedor.
* Redes Docker: comunicación entre contenedores.
* Volúmenes: persistencia de datos en contenedores.
* Variables de entorno y configuración de contenedores.
* Dockerfile: estructura y creación de imágenes propias.
* Docker Compose: definición y gestión de aplicaciones formadas por varios servicios.
* Ficheros compose.yaml: servicios, imágenes, puertos, redes, volúmenes y variables de entorno.
* Ciclo básico de despliegue mediante Docker Compose: docker compose up, comprobación de servicios y docker compose down.
* Análisis de los servicios desplegados y de las relaciones existentes entre ellos.

* Servidores de aplicaciones: concepto, finalidad y diferencias respecto a un servidor web.
* Componentes básicos de un servidor de aplicaciones.
* Arquitectura de una aplicación desplegada sobre un servidor de aplicaciones.
* Configuración básica del servidor de aplicaciones.
* Despliegue de aplicaciones web en un servidor de aplicaciones.
* Servidor web y servidor de aplicaciones: funciones y comunicación entre ambos.
* Proxy inverso: concepto, funcionamiento y utilidad en una arquitectura web.
* Configuración de un servidor web para actuar como intermediario entre el cliente y el servidor de aplicaciones.
* Comunicación entre servicios mediante redes de contenedores.
* Configuración de puertos y direccionamiento de servicios.
* Variables de entorno para la configuración de aplicaciones desplegadas.
* Pruebas de funcionamiento de la aplicación desplegada.
* Comprobación de conectividad entre contenedores y servicios.
* Análisis básico de logs de los servicios desplegados.
* Comprobación básica del rendimiento y comportamiento de la aplicación desplegada.
* Documentación del proceso de despliegue y configuración.

**Metodología**

* Metodologías activas centradas en el alumnado. El aprendizaje se organiza en torno a **prácticas progresivas de despliegue mediante contenedores**. Se parte de conceptos sencillos de virtualización y contenedores para llegar rápidamente a la ejecución de una aplicación mediante Docker Compose. Posteriormente, el alumnado analiza la arquitectura resultante y configura la comunicación entre un servidor web y un servidor de aplicaciones.

* El objetivo de la primera parte no es dominar Docker como tecnología, sino **comprender los elementos que intervienen en un despliegue mediante contenedores** y ser capaz de interpretar un fichero compose.yaml, poner en funcionamiento los servicios definidos y comprobar su comunicación.

* En la segunda parte se introduce el servidor de aplicaciones a partir de un escenario práctico, relacionándolo con los conocimientos adquiridos sobre Apache en las unidades anteriores. De esta forma, el alumnado comprende la separación entre servidor web, servidor de aplicaciones y aplicación desplegada.

**Secuencia de actividades**

* **A1:** Primeros pasos con Docker. Instalación y comprobación de Docker. Ejecución de un primer contenedor y análisis de su ciclo de vida.
* **A2:** Imágenes, contenedores y puertos. Descarga de imágenes, creación y eliminación de contenedores y publicación de un servicio mediante un puerto del equipo anfitrión.
* **A3:** Redes, volúmenes y variables de entorno. Creación de una aplicación sencilla formada por varios contenedores y análisis de la comunicación entre ellos, la persistencia de datos y la configuración mediante variables de entorno.
* **A4:** Dockerfile y Docker Compose. Creación de una imagen sencilla mediante un Dockerfile y definición de una aplicación formada por varios servicios mediante un fichero compose.yaml.
* **A5:** Despliegue mediante Docker Compose. Ejecución de docker compose up -d, comprobación del estado de los servicios, análisis de los contenedores creados y comprensión de la arquitectura desplegada.
* **A6:** Configuración y despliegue de una aplicación. Instalación o despliegue de un servidor de aplicaciones y configuración de una aplicación web sencilla sobre él.
* **A7:** Integración entre servidor web y servidor de aplicaciones. Análisis del flujo de una petición desde el navegador hasta el servidor web y desde este hasta el servidor de aplicaciones.
* **A08:** Práctica global de despliegue. Creación de una arquitectura formada por servidor web, servidor de aplicaciones y aplicación web, utilizando contenedores para facilitar el despliegue y configuración de los servicios.
* **A09:** Documentación del despliegue. Elaboración de una guía técnica en la que se describan los contenedores, imágenes, redes, puertos, volúmenes, variables de entorno, configuración del servidor de aplicaciones y comunicación con el servidor web.

**Recursos**

* Equipos del aula de informática y máquinas virtuales con Ubuntu Server.
* Docker Engine y Docker Compose.
* Imágenes Docker necesarias para las prácticas.
* Servidor web Apache HTTP Server.
* Servidor de aplicaciones utilizado durante la unidad.
* Aplicación web de prueba para realizar los despliegues.
* Terminal y herramientas de administración de Docker: docker, docker compose, docker ps, docker images, docker logs y docker exec.
* Navegador web y herramientas como curl para realizar pruebas de funcionamiento.
* Editor de texto para la creación de Dockerfile y ficheros compose.yaml.
* Aula virtual (Aules) para la distribución de materiales, actividades y documentación.

### 4. Evaluación y adaptación

**Instrumentos de evaluación**
La evaluación será continua y formativa, enfocada en la adquisición de los criterios de evaluación de las partes del RA01 y el RA03 trabajadas.
* **Rúbricas de prácticas (40%):** valoración sistemática de la documentación y resultado generados en cada actividad, atendiendo a la corrección técnica, la funcionalidad y configuración conrrectas y la claridad de la documentación.
* **Pruebas objetivas (60%):** prueba teórico-práctica al finalizar el RA para verificar el cumplimiento de los criterios de evaluación.

**Adaptaciones**

* **Medidas según necesidades:** las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
* **DUA:** se empleará el **Diseño Universal para el Aprendizaje**, proporcionando materiales en múltiples formatos y permitiendo la flexibilización de tiempos en las actividades prácticas.

---

## UP04: Servicios de red y transferencia de archivos

### 1. Identificación

| Campo | Detalle |
| :--- | :--- |
| **Código** | UP04 |
| **Módulo** | Despliegue de aplicaciones web (0614) |
| **Duración** | **9 Horas** |
| **Temporalización** | Del **21/12/2026** al **18/01/2027** |

### 2. Fundamentación

**Resultados de Aprendizaje**

* **RA04.** Administra servidores de transferencia de archivos, evaluando y aplicando criterios de configuración que garanticen la disponibilidad del servicio.
* **RA05.** Verifica la ejecución de aplicaciones web comprobando los parámetros de configuración de servicios de red.

**Criterios de Evaluación**

**RA04 - Criterios de evaluación**

* **a)** Se han instalado y configurado servidores de transferencia de archivos.
* **b)** Se han creado usuarios y grupos para el acceso remoto al servidor.
* **c)** Se ha comprobado el acceso al servidor, tanto en modo activo como en modo pasivo.
* **d)** Se han realizado pruebas con clientes en línea de comandos y clientes en modo gráfico.
* **e)** Se ha utilizado el protocolo seguro de transferencia de archivos.
* **f)** Se han configurado y utilizado servicios de transferencia de archivos integrados en servidores web.
* **g)** Se ha elaborado documentación relativa a la configuración y administración del servicio de transferencia de archivos.
* **h)** Se han utilizado tecnologías de virtualización en el despliegue de servidores de transferencia de archivos en la nube y en contenedores.

**RA05 - Criterios de evaluación**

* **a)** Se ha descrito la estructura, nomenclatura y funcionalidad de los sistemas de nombres jerárquicos.
* **b)** Se han identificado las necesidades de configuración del servidor de nombres en función de los requerimientos de ejecución de las aplicaciones web desplegadas.
* **c)** Se ha identificado la función, elementos y estructuras lógicas del servicio de directorio.
* **d)** Se ha analizado la configuración y personalización del servicio de directorio.
* **e)** Se ha analizado la capacidad del servicio de directorio como mecanismo de autenticación centralizada de los usuarios en una red.
* **f)** Se han especificado los parámetros de configuración en el servicio de directorios adecuados para el proceso de validación de usuarios de la aplicación web.
* **g)** Se ha elaborado documentación relativa a las adaptaciones realizadas en los servicios de red.
* **h)** Se han utilizado tecnologías de virtualización en el despliegue de servidores de directorios en la nube y en contenedores.

**Competencias**

* **Profesionales:** a), b), c), j), n), ñ), q).
* **Ocupación:** c), d), o), p), r).

### 3. Organización

**Contenidos**

* **Transferencia de archivos**: finalidad de los servicios de transferencia de archivos en el despliegue y mantenimiento de aplicaciones web.
* Protocolo FTP: características, funcionamiento y principales componentes.
* Servidor FTP: instalación y configuración básica.
* Usuarios y grupos para el acceso al servicio de transferencia.
* Permisos sobre los archivos y directorios utilizados para la transferencia.
* Modos de funcionamiento de FTP: modo activo y modo pasivo.
* Clientes FTP: utilización desde línea de comandos y mediante herramientas gráficas.
* Transferencia de archivos: subida, descarga y comprobación de los archivos transferidos.
* Protocolos seguros de transferencia: FTPS y SFTP. Diferencias conceptuales con FTP.
* Utilización de servicios de transferencia de archivos en el proceso de despliegue de una aplicación web.

* **DNS**: finalidad del sistema de nombres de dominio y su importancia en el acceso a aplicaciones web.
* Sistema jerárquico de nombres: raíz, dominios de nivel superior, dominios y subdominios.
* Dominios y nombres de host.
* Resolución de nombres: relación entre nombres de dominio y direcciones IP.
* Registros DNS básicos: `A`, `AAAA`, `CNAME` y `NS`.
* Servidores DNS y clientes DNS.
* Configuración básica de un servicio DNS para un entorno de prácticas.
* Resolución de nombres dentro de una red local.
* Utilización de nombres de dominio para acceder a una aplicación web en lugar de utilizar directamente su dirección IP.
* Integración entre DNS y servidor web: resolución del nombre hacia el servidor que aloja la aplicación.

* **Servicios de directorio**: finalidad y características.
* Diferencias entre un servicio de directorio y otros sistemas de almacenamiento de información.
* Estructura jerárquica de un directorio.
* LDAP: concepto, características y funcionamiento básico.
* Organización de la información mediante entradas, atributos y estructura jerárquica.
* Usuarios y grupos en un servicio de directorio.
* Autenticación centralizada mediante un servicio de directorio.
* Configuración básica de un servicio LDAP en un entorno de prácticas.
* Concepto de integración de LDAP con una aplicación web.
* Relación entre los servicios de red y el despliegue de aplicaciones web.

**Metodología**

* Metodologías activas centradas en el alumnado. El aprendizaje se organiza en torno a **prácticas breves y contextualizadas de configuración y utilización de servicios de red**. .

* En la primera parte, el alumnado utiliza un servicio FTP para comprender cómo se transfieren los archivos entre un cliente y un servidor, trabajando con usuarios, grupos y permisos y realizando las operaciones tanto desde la línea de comandos como desde un cliente gráfico.

* En la segunda parte, DNS se introduce como un servicio necesario para sustituir el acceso mediante dirección IP por un nombre fácilmente identificable. El alumnado configura un nombre para el servidor web y comprueba el proceso de resolución hasta acceder a la aplicación desplegada.

* Finalmente, LDAP se aborda de forma introductoria, centrándose en el concepto de servicio de directorio, su estructura jerárquica y su utilización como mecanismo de autenticación centralizada, sin profundizar en una administración avanzada del servicio.

**Secuencia de actividades**

* **A1:** Instalación y configuración básica de un servidor FTP. Creación de usuarios y grupos, configuración de permisos y preparación de un directorio para la transferencia de archivos.
* **A2:** Transferencia de archivos. Conexión mediante un cliente FTP de línea de comandos y mediante un cliente gráfico. Realización de operaciones de subida y descarga de archivos y comprobación de los resultados.
* **A3:** Modos activo y pasivo y transferencia segura. Explicación conceptual de las diferencias entre ambos modos y aproximación a FTPS y SFTP como alternativas para realizar transferencias seguras.

* **A4:** Configuración de un DNS sencillo. Creación de un nombre para el servidor web y configuración de la resolución hacia su dirección IP. Comprobación mediante herramientas de consulta DNS.
* **A5:** Integración DNS-Apache. Configuración del servidor web para que la aplicación pueda ser accesible mediante un nombre como `http://aula.local\` en lugar de utilizar directamente la dirección IP del servidor.

* **A6:** Introducción a los servicios de directorio. Análisis de la finalidad de LDAP, su estructura jerárquica y la organización de usuarios y grupos.
* **A7:** Configuración básica de LDAP. Creación de una estructura sencilla de directorio con usuarios y grupos y realización de consultas básicas sobre la información almacenada.
* **A8:** Autenticación centralizada. Análisis conceptual del proceso mediante el cual una aplicación puede utilizar un servicio LDAP para validar las credenciales de sus usuarios.

* **A09:** Práctica global y documentación. Comprobación del funcionamiento de los servicios configurados y elaboración de una documentación breve con la configuración, comandos utilizados, pruebas realizadas y resultados obtenidos.

**Recursos**

* Equipos del aula de informática y máquinas virtuales con Ubuntu Server.
* Servidor de transferencia de archivos FTP para las prácticas.
* Cliente FTP de línea de comandos y cliente FTP gráfico.
* Servidor DNS y herramientas de consulta y diagnóstico de resolución de nombres.
* Servidor web Apache HTTP Server configurado en las unidades anteriores.
* Servidor LDAP y herramientas básicas de administración y consulta.
* Terminal y herramientas de administración de Ubuntu Server.
* Navegador web para comprobar el acceso a la aplicación mediante nombre de dominio.
* Aplicación web desplegada en las unidades anteriores para comprobar la integración de los servicios de red.
* Aula virtual (Aules) para la distribución de materiales, actividades y documentación.

### 4. Evaluación y adaptación

**Instrumentos de evaluación**
La evaluación será continua y formativa, enfocada en la adquisición de los criterios de evaluación del RA04 y el RA05.
* **Rúbricas de prácticas (40%):** valoración sistemática de la documentación y resultado generados en cada actividad, atendiendo a la corrección técnica, la funcionalidad y configuración conrrectas y la claridad de la documentación.
* **Pruebas objetivas (60%):** prueba teórico-práctica al finalizar el RA para verificar el cumplimiento de los criterios de evaluación.

**Adaptaciones**
* **Medidas según necesidades:** las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
* **DUA:** se empleará el **Diseño Universal para el Aprendizaje**, proporcionando materiales en múltiples formatos y permitiendo la flexibilización de tiempos en las actividades prácticas.

---

## UP05: Documentación e Integración continua

### 1. Identificación

| Campo | Detalle |
| :--- | :--- |
| **Código** | UP05 |
| **Módulo** | Despliegue de aplicaciones web (0614) |
| **Duración** | **6 Horas** |
| **Temporalización** | Del **25/01/2027** al **01/02/2027** |

### 2. Fundamentación

**Resultado de Aprendizaje**

* **RA06.** Elabora la documentación de la aplicación web evaluando y seleccionando herramientas de generación de documentación, control de versiones y de integración continua.

**Criterios de Evaluación**

* **a)** Se han identificado diferentes herramientas de generación de documentación.
* **b)** Se han documentado los componentes software utilizando los generadores específicos de las plataformas.
* **c)** Se han utilizado diferentes formatos para la documentación.
* **d)** Se han utilizado herramientas colaborativas para la elaboración y mantenimiento de la documentación.
* **e)** Se ha instalado, configurado y utilizado un sistema de control de versiones.
* **f)** Se ha garantizado la accesibilidad y seguridad de la información y código almacenada por el sistema de control de versiones.
* **g)** Se ha documentado la instalación, configuración y uso del sistema de control de versiones utilizado.
* **h)** Se han utilizado herramientas para la integración continua del código.

**Competencias**

* **Profesionales:** a), b), c), j), n), ñ), q).
* **Ocupación:** c), d), o), p), r).

### 3. Organización

**Contenidos**

* Documentación de aplicaciones web: finalidad, características y tipos de documentación.
* Documentación técnica y documentación orientada al usuario.
* Formatos habituales para la documentación: Markdown y HTML.
* Herramientas colaborativas para la creación y mantenimiento de documentación.
* Creación y utilización de plantillas de documentación.
* Documentación de los procesos de instalación, configuración y despliegue de una aplicación web.
* Documentación de componentes y recursos de una aplicación web.
* Sistemas de control de versiones: finalidad y características.
* Git como sistema de control de versiones.
* Repositorios locales y remotos.
* Operaciones básicas de control de versiones: `clone`, `status`, `add`, `commit`, `push` y `pull`.
* Organización y mantenimiento de un repositorio para un proyecto de despliegue web.
* Control de cambios y recuperación de versiones anteriores.
* Seguridad y accesibilidad de la información almacenada en un sistema de control de versiones.
* Plataformas colaborativas para alojar repositorios y documentación.
* Integración continua: concepto, finalidad y ventajas.
* Flujo básico de integración continua: modificación del código, envío al repositorio, ejecución automática y comprobación del resultado.
* Automatización de tareas mediante herramientas de integración continua.
* Configuración de un flujo básico de integración continua.
* Comprobación automática del proyecto y detección de errores.
* Documentación del proceso de integración continua.

**Metodología**

* Metodologías activas centradas en el alumnado. El aprendizaje se organiza en torno a **la documentación y automatización del proyecto de despliegue desarrollado durante las unidades anteriores**. El alumnado parte de una aplicación web ya desplegada y genera la documentación necesaria para que otra persona pueda comprender, instalar y utilizar el proyecto.

* Posteriormente, el proyecto se incorpora a un repositorio Git remoto, estableciendo un flujo básico de control de versiones. Finalmente, se configura una herramienta de integración continua que ejecute automáticamente una serie de comprobaciones cada vez que se incorporen cambios al repositorio.

**Secuencia de actividades**

* **A1:** Creación de documentación mediante Markdown. Elaboración de un README.md y de documentación técnica del proyecto utilizando una estructura y plantilla previamente definida.
* **A2:** Control de versiones. Creación o utilización de un repositorio Git para almacenar el proyecto y la documentación. Realización de las operaciones básicas de actualización y sincronización con el repositorio remoto.
* **A3:** Introducción a la integración continua. Análisis del funcionamiento de un flujo de integración continua y configuración de una acción automática que se ejecute al realizar cambios en el repositorio.
* **A4:** Automatización de comprobaciones. Configuración de un flujo sencillo que compruebe automáticamente el proyecto y permita detectar errores antes de considerar terminado un cambio.

* **A5:** Práctica global. Actualización del proyecto de despliegue desarrollado durante las unidades anteriores, documentación de los cambios, publicación mediante Git y comprobación de la ejecución automática del flujo de integración continua.
* **A6:** Documentación final. Elaboración de una documentación técnica que incluya el funcionamiento del repositorio, el proceso de despliegue, las operaciones de control de versiones y el flujo de integración continua configurado.

**Recursos**

* Equipos del aula de informática.
* Git y plataforma de alojamiento de repositorios utilizada en el curso.
* Repositorio del proyecto de despliegue desarrollado durante las unidades anteriores.
* Herramientas de documentación mediante Markdown.
* Herramienta de integración continua proporcionada por la plataforma de control de versiones.
* Editor de texto o entorno de desarrollo para la edición de documentación y archivos de configuración.
* Aula virtual (Aules) para la distribución de materiales, actividades y documentación.

### 4. Evaluación y adaptación

**Instrumentos de evaluación**

La evaluación será continua y formativa, enfocada en la adquisición de los criterios de evaluación del RA06.

* **Rúbricas de prácticas (40%):** valoración sistemática de la documentación y resultado generados en cada actividad, atendiendo a la corrección técnica, la funcionalidad y configuración conrrectas y la claridad de la documentación.
* **Pruebas objetivas (60%):** prueba teórico-práctica al finalizar el RA para verificar el cumplimiento de los criterios de evaluación.

**Adaptaciones**

* **Medidas según necesidades:** las adaptaciones se aplicarán de manera flexible tras la evaluación inicial y el seguimiento diario del progreso del alumnado.
* **DUA:** se empleará el **Diseño Universal para el Aprendizaje**, proporcionando materiales en múltiples formatos y permitiendo la flexibilización de tiempos en las actividades prácticas.

---
