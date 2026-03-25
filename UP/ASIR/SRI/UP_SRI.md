# Unidades de programación: 0375 Servicios de Red e Internet (2025-2026)


### Resumen de Unidades de Programación (Curso 2025-2026)

| Código | Nombre de la UP | Duración (Horas Centro) | Temporalización | RAs Asociados |
| :--- | :--- | :--- | :--- | :--- |
| **UP01** | Servidor DNS para hosting público | 19h | 08/09/2025 – 30/09/2025 | **RA01** |
| **UP02** | DHCP en alta disponibilidad | 19h | 01/10/2025 – 31/10/2025 | **RA02** |
| **UP03** | Servidor de Hosting | 26h | 01/11/2025 – 14/12/2025 | **RA03**, **RA04** |
| **UP04** | Servidor de Correo | 6h | 15/12/2025 – 19/12/2025 | **RA05** |
| **UP05** | Servidor de streaming | 12h | 20/12/2025 – 23/01/2026 | **RA07**, **RA08** |
| **UP06** | Mensajería | 10h | 24/01/2026 – 06/02/2026 | **RA06** |



## UP01: Servidor DNS para hosting público
### 1. Identificación
*   **Código:** UP01 | **Módulo:** 0375
*   **Duración:** 19 horas.
*   **Temporalización:** 08/09/2025 – 30/09/2025.

### 2. Fundamentación (Real Decreto 1629/2009)
*   **Resultado de Aprendizaje:**
    *   **RA01:** Administra servicios de resolución de nombres, analizándolos y garantizando la seguridad del servicio.
*   **Criterios de Evaluación:**
    *   a) Se han identificado y descrito escenarios en los que surge la necesidad de un servicio de resolución de nombres.
    *   b) Se han clasificado los principales mecanismos de resolución de nombres.
    *   c) Se ha descrito la estructura, nomenclatura y funcionalidad de los sistemas de nombres jerárquicos.
    *   d) Se han instalado y configurado servicios jerárquicos de resolución de nombres.
    *   e) Se ha preparado el servicio para reenviar consultas de recursos externos a otro servidor de nombres.
    *   f) Se ha preparado el servicio para almacenar y distribuir las respuestas procedentes de otros servidores.
    *   g) Se han añadido registros de nombres correspondientes a una zona nueva, con opciones relativas a servidores de correo y alias.
    *   h) Se han implementado soluciones de servidores de nombres en direcciones «ip» dinámicas.
    *   i) Se han realizado transferencias de zona entre dos o más servidores.
    *   j) Se han documentado los procedimientos de instalación y configuración.
*   **Competencias:**
    *   **Profesionales:** b) Administrar servicios de red instalando y configurando el software, en condiciones de calidad.
    *   **Empleabilidad:** 16. Innovación; 18. Resolución de problemas.

### 3. Organización
*   **Contenidos (Orden 36/2012):** Sistemas de nombres planos y jerárquicos. Resolutores de nombres. Proceso de resolución de un nombre de dominio. Servidores raíz y dominios de primer nivel y sucesivos. Zonas primarias y secundarias. Transferencias de zona. Delegación. Tipos de registros. Servidores de nombres en direcciones «ip» dinámicas. Utilización de reenviadores. Comandos relativos a la resolución de nombres. El cliente del servicio de nombres de dominio. Configuración. El servidor de nombres de dominio. Configuración. Herramientas gráficas de configuración. Documentación de las configuraciones establecidas.
*   **Teoría:** [Servicios en red: DNS](https://jgarciabenlloch.github.io/protocolos/dns).
*   **Metodología:** Metodologías activas basadas en el proyecto [Terraformadores de Venus](https://terraformadoresdevenus.com).
*   **Secuencia (Fases):**
    *   **E1:** [Misión 2: Configuración del Servidor DNS en la Red Sentinel](https://terraformadoresdevenus.com/mision-dns-sentinel).
    *   **E2:** [Misión 3: Delegación de Zonas en el Servidor DNS](https://terraformadoresdevenus.com/mision-delegacion-dns).
    *   **E3:** [Misión: Actualización Dinámica de DNS](https://terraformadoresdevenus.com/mision-actualizacion-dinamica).

### 4. Recursos Tecnológicos
*   **Base Tecnológica:** GNS3, VirtualBox, Sistema Operativo Linux (BIND9).

### 5. Evaluación y Adaptación
*   **Instrumentos:** 20% parte práctica (Misiones de Venus) y 80% prueba objetiva teórica.
*   **Adaptaciones:** Aplicación de Diseño Universal para el Aprendizaje (DUA) y ritmos flexibles según necesidades detectadas.

---

## UP02: DHCP en alta disponibilidad
### 1. Identificación
*   **Código:** UP02 | **Módulo:** 0375
*   **Duración:** 19 horas.
*   **Temporalización:** 01/10/2025 – 31/10/2025.

### 2. Fundamentación (Real Decreto 1629/2009)
*   **Resultado de Aprendizaje:**
    *   **RA02:** Administra servicios de configuración automática, identificándolos y verificando la correcta asignación de los parámetros.
*   **Criterios de Evaluación:**
    *   a) Se han reconocido los mecanismos automatizados de configuración de los parámetros de red y las ventajas que proporcionan.
    *   b) Se han ilustrado los procedimientos y pautas que intervienen en una solicitud de configuración de los parámetros de red.
    *   c) Se han instalado servidores de configuración de los parámetros de red.
    *   d) Se ha preparado el servicio para asignar la configuración básica a los equipos de una red local.
    *   e) Se han configurado asignaciones estáticas y dinámicas.
    *   f) Se han integrado en el servicio opciones adicionales de configuración.
    *   g) Se han documentado los procedimientos realizados.

### 3. Organización
*   **Contenidos (Orden 36/2012):** Funcionamiento del servicio DHCP. Características. Mensajes. Asignaciones. Tipos. Utilización de un cliente de DHCP. Autoconfiguración de red sin el servicio. Instalación y configuración de un servidor DHCP en sistemas operativos libres y propietarios. Parámetros y declaraciones de configuración. Servidor autorizado. Comandos utilizados para el funcionamiento del servicio. Herramientas gráficas de configuración. Diagnóstico y resolución de incidencias en el servicio. Documentación de las configuraciones establecidas.
*   **Teoría:** [Servicios en red: DHCP](https://jgarciabenlloch.github.io/protocolos/dhcp).
*   **Metodología:** Aprendizaje basado en retos técnicos de la infraestructura de Venus.
*   **Secuencia (Fases):**
    *   **E1:** [Misión: Configuración de un Servidor DHCP en Lobezno](https://terraformadoresdevenus.com/mision-dhcp-lobezno).
    *   **E2:** [Misión: Alta Disponibilidad de DHCP](https://terraformadoresdevenus.com/mision-dhcp-ha).
    *   **E3:** [Misión: Actualización Dinámica de DNS - Integración DHCP](https://terraformadoresdevenus.com/mision-actualizacion-dinamica).

### 4. Recursos Tecnológicos
*   **Equipamiento:** MikroTik (Relay DHCP), Kea DHCP, Docker, Linux.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Práctica de configuración en Venus (20%) y examen RA02 (80%).
*   **Adaptaciones:** Flexibilización de tiempos y materiales de apoyo en Aules.

---

## UP03: Servidor de Hosting
### 1. Identificación
*   **Código:** UP03 | **Módulo:** 0375
*   **Duración:** 26 horas.
*   **Temporalización:** 01/11/2025 – 14/12/2025.

### 2. Fundamentación (Real Decreto 1629/2009)
*   **Resultados de Aprendizaje:**
    *   **RA03:** Administra servidores Web aplicando criterios de configuración y asegurando el funcionamiento del servicio.
    *   **RA04:** Administra servicios de transferencia de archivos asegurando y limitando el acceso a la información.
*   **Criterios de Evaluación (RA03):** a) Fundamentos y protocolos; b) Instalación y configuración; c) Módulos; d) Sitios virtuales; e) Autenticación y control de acceso; f) Certificados digitales; g) Seguridad en comunicaciones; h) Monitorización; i) Análisis de registros; j) Documentación.
*   **Criterios de Evaluación (RA04):** a) Utilidad y modo de operación; b) Instalación y configuración; c) Usuarios y grupos; d) Acceso anónimo; e) Límites de acceso; f) Acceso activo y pasivo; g) Pruebas con clientes; h) Navegador como cliente; i) Documentación.

### 3. Organización
*   **Contenidos (Orden 36/2012):** Web: Protocolo HTTP. Tipos MIME. Instalación y configuración. Módulos. Amfitriones virtuales. Autenticación. HTTPS. Certificados. Registro y monitorización. FTP: Servidores y clientes. Permisos y cuotas. Tipos de usuarios. Modes de conexión. Transferencias.
*   **Teoría:** [HTTP](https://jgarciabenlloch.github.io/protocolos/http) y [FTP](https://jgarciabenlloch.github.io/protocolos/ftp).
*   **Metodología:** Proyecto de infraestructura de nube pública para startups.
*   **Secuencia (Fases):**
    *   **E1:** [Proyecto: Infraestructura Hosting - Servidor Apache y Seguridad HTTPS (Let's Encrypt)](https://terraformadoresdevenus.com/proyecto-hosting).
    *   **E2:** [Proyecto: Infraestructura Hosting - Servidor Nginx y Hosting Especializado para Clientes](https://terraformadoresdevenus.com/proyecto-hosting).
    *   **E3:** [Proyecto: Infraestructura Hosting - Servidor FTP seguro FTPS, SFTP y File Browser](https://terraformadoresdevenus.com/proyecto-hosting).

### 4. Recursos Tecnológicos
*   **Infraestructura:** AWS (EC2, IP elástica), Let's Encrypt, Apache, Nginx, vsftpd, Docker.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Resolución del Proyecto Integral de Hosting (20%) y prueba objetiva (80%).
*   **Adaptaciones:** Uso de guías visuales y laboratorios remotos para atención individualizada.

---

## UP04: Servidor de Correo
### 1. Identificación
*   **Código:** UP04 | **Módulo:** 0375
*   **Duración:** 6 horas.
*   **Temporalización:** 15/12/2025 – 19/12/2025.

### 2. Fundamentación (Real Decreto 1629/2009)
*   **Resultado de Aprendizaje:**
    *   **RA05:** Administra servidores de correo electrónico, aplicando criterios de configuración y garantizando la seguridad del servicio.
*   **Criterios de Evaluación:** a) Protocolos de envío/recogida; b) Instalación; c) Cuentas de usuario; d) Impedir usos indebidos; e) Recogida remota; f) Clientes de correo; g) Firma digital y cifrado; h) Servicio seguro; i) Documentación.

### 3. Organización
*   **Contenidos (Orden 36/2012):** Agentes (MTA, MDA, MUA). Estructura de missatges. Protocol de transferència. Clients. Comptes, àlies i bústies. Webmail. Correu segur. Reenviament. Tècniques antispam. Protocols de descàrrega.
*   **Teoría:** [Servicios en red: EMAIL](https://jgarciabenlloch.github.io/protocolos/email).
*   **Secuencia (Fases):**
    *   **E1:** [Misión: Instalación y configuración del servicio de correo electrónico (Index Misiones)](https://terraformadoresdevenus.com/servicios-web-ftp-email-streaming).

### 4. Recursos Tecnológicos
*   **Sistemas:** Servidores Linux, Postfix, Dovecot, Roundcube.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Práctica de configuración de correo seguro (20%) y examen RA05 (80%).
*   **Adaptaciones:** DUA y materiales de consulta permanente en la plataforma.

---

## UP05: Servidor de streaming
### 1. Identificación
*   **Código:** UP05 | **Módulo:** 0375
*   **Duración:** 12 horas.
*   **Temporalización:** 20/12/2025 – 23/01/2026.

### 2. Fundamentación (Real Decreto 1629/2009)
*   **Resultados de Aprendizaje:**
    *   **RA07:** Administra servicios de audio identificando las necesidades de distribución y adaptando los formatos.
    *   **RA08:** Administra servicios de vídeo identificando las necesidades de distribución y adaptando los formatos.
*   **Criterios de Evaluación (RA07 y RA08):** a) Funcionalidad; b) Instalación de servidores; c) Configuración de clientes; d) Formatos y códecs; e) Sindicación (Podcasts); f) Videoconferencia; g) Herramientas gráficas; h) Documentación.

### 3. Organización
*   **Contenidos (Orden 36/2012):** Audio: Formats. Servidors de streaming. VoIP. Sindicació (Podcast). Vídeo: Formats. Servidors de vídeo. Còdecs. Videoconferència. Servidors de jocs en línia.
*   **Teoría:** [Servicios en red: STREAMING](https://jgarciabenlloch.github.io/protocolos/streaming).
*   **Secuencia (Fases):**
    *   **E1:** [Misión: Configuración de un Servidor de Streaming con Nginx y RTMP y AWS](https://terraformadoresdevenus.com/mision-streaming-nginx).

### 4. Recursos Tecnológicos
*   **Herramientas:** Nginx (Módulo RTMP), OBS Studio, VLC Media Player, Video.js, AWS.

### 5. Evaluación y Adaptación
*   **Instrumentos:** Retransmisión en vivo y página web del evento (20%) y prueba objetiva (80%).
*   **Adaptaciones:** Tutorías de refuerzo para la captura de señal multimedia.

---

## UP06: Mensajería
### 1. Identificación
*   **Código:** UP06 | **Módulo:** 0375
*   **Duración:** 10 horas.
*   **Temporalización:** 24/01/2026 – 06/02/2026.

### 2. Fundamentación (Real Decreto 1629/2009)
*   **Resultado de Aprendizaje:**
    *   **RA06:** Administra servicios de mensajería instantánea, noticias y listas de distribución, verificando y asegurando el acceso de los usuarios.
*   **Criterios de Evaluación:** a) Descripción servicios; b) Instalación mensajería; c) Clientes; d) Servicio noticias; e) Listas distribución; f) Tipos lista; g) Cuentas usuario; h) Documentación.

### 3. Organización
*   **Contenidos (Orden 36/2012):** Missatgeria instantània. Protocols. Clients. Normes de respecte. Servici de notícies. Llistes de distribució.
*   **Teoría:** [Servicios en red: Monitorización/Mensajería](https://jgarciabenlloch.github.io/protocolos/monitorizacion).
*   **Secuencia (Fases):**
    *   **E1:** [Misión: Implementar un sistema de mensajería con Matrix (Synapse) para alertas automáticas](https://terraformadoresdevenus.com/mision-monitorizacion-docker).

### 4. Recursos Tecnológicos
*   **Base Tecnológica:** Docker, Matrix (Synapse), Prometheus (Alertmanager).

### 5. Evaluación y Adaptación
*   **Instrumentos:** Configuración del servidor de mensajería y alertas (20%) y examen RA06 (80%).
*   **Adaptaciones:** Documentación técnica simplificada y ejemplos prácticos de sintaxis.