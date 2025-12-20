---
title: Asegurando Docker  Mejores Pr Cticas Para Usuarios Non Root
published: true
date: 2024-01-04 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/aafb40f7766b
---

# Asegurando Docker: Mejores Prácticas para Usuarios Non-Root

Docker es una plataforma de contenerización que simplifica la implementación y escalabilidad de aplicaciones al empaquetarlas en unidades… 

* * *

### Asegurando Docker: Mejores Prácticas para Usuarios Non-Root

* * *

[Docker](https://www.docker.com/) es una plataforma de contenerización que simplifica la implementación y escalabilidad de aplicaciones al empaquetarlas en unidades ligeras y portátiles llamadas contenedores. Una imagen de Docker es un paquete ejecutable independiente que incluye todo lo necesario para ejecutar una aplicación de software, como el código, el tiempo de ejecución, las bibliotecas y las herramientas del sistema. Las imágenes sirven como base para la creación de contenedores, permitiendo una implementación consistente y eficiente de aplicaciones en diversos entornos.

Docker ganó [popularidad](https://www.docker.com/blog/docker-index-dramatic-growth-in-docker-usage-affirms-the-continued-rising-power-of-developers/) entre los desarrolladores al revolucionar la implementación de aplicaciones mediante la contenerización. Sus contenedores ligeros y portátiles ofrecieron un entorno consistente, simplificando el proceso de desarrollo e implementación. La facilidad de uso de Docker, su compatibilidad en diferentes plataformas y la eficiente utilización de recursos contribuyeron a su rápida adopción, capacitando a los desarrolladores para construir, enviar y ejecutar aplicaciones de manera fluida en entornos diversos.

Docker, al igual que cualquier software, no está exento de [vulnerabilidades](https://www.docker.com/blog/container-security-and-why-it-matters/). A medida que la tecnología de contenerización evoluciona, surgen preocupaciones de seguridad. Los usuarios deben permanecer atentos, actualizando y monitoreando regularmente las imágenes de Docker para abordar posibles vulnerabilidades y garantizar un entorno de implementación seguro.

Conceder acceso a un usuario** __**_non-root_** __** dentro de un contenedor de Docker sirve como un ejemplo simple pero impactante para ilustrar vulnerabilidades en Docker, enfatizando la importancia de mantener las mejores prácticas de seguridad.

Ejecutar contenedores de Docker con privilegios de usuario _root_ puede plantear riesgos de seguridad por varias razones:

  1. Escalada de privilegios: Ejecutar contenedores como usuario _root_ puede proporcionar una vía para la elevación de privilegios. Si un atacante puede explotar una vulnerabilidad dentro del contenedor, podría lograr la escalada de sus privilegios y tomar el control del sistema subyacente del host.
  2. Aumento de la superficie de ataque: Permitir que un contenedor de Docker se ejecute como usuario _root_ aumenta la superficie de ataque potencial. Si un atacante obtiene el control de un contenedor con privilegios de _root_ , puede tener más opciones para explotar vulnerabilidades y comprometer el sistema host.
  3. Acceso al sistema de archivos: El acceso _root_ dentro de un contenedor significa acceso irrestricto al sistema de archivos. Esto podría llevar a modificaciones o eliminaciones no deseadas de archivos críticos del sistema, potencialmente causando inestabilidad del sistema o pérdida de datos.
  4. Aislamiento de espacio de nombres de usuario: Los contenedores de Docker aprovechan los espacios de nombres de usuarios para proporcionar cierto nivel de aislamiento entre los usuarios del contenedor y del sistema host. Ejecutar contenedores como un usuario _non-root_ garantiza que, incluso si un atacante obtiene acceso al contenedor, no tendrá automáticamente acceso de _root_ en el host.
  5. Mejores prácticas de seguridad: Seguir las mejores prácticas de seguridad es esencial para minimizar posibles vulnerabilidades. Ejecutar contenedores con el menor privilegio necesario es un principio fundamental en la seguridad de contenedores. Al utilizar un usuario _non-root_ , se adhiere al principio de menor privilegio, limitando el impacto potencial de violaciones de seguridad.



Utilizar un usuario _non-root_ en Docker es implementar el principio de menor privilegio delineado en las pautas de Control de Acceso de [OWASP](https://owasp.org/www-community/Access_Control). Esta práctica está desaconsejada, como se destaca tanto en [las Hojas de Seguridad de OWASP Docker](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html#rule-2-set-a-user), específicamente en la regla n.º 2 “establecer un usuario”, como en el [CIS Docker Benchmark V1.6.0](https://www.cisecurity.org/insights/blog/announcing-cis-benchmark-for-docker-1-6) bajo “4.1 — Asegurarse de que se haya creado un usuario para el contenedor (Manual)”. Seguir estas pautas mejora la seguridad del contenedor al limitar permisos innecesarios y reducir la posibilidad de problemas de seguridad.

Con un usuario _non-root_ en un Dockerfile, incluye la instrucción “USER”, como “USER myuser”, para cambiar a una identidad menos privilegiada. Sin ella, el valor predeterminado es ejecutarse como _root_. En un comando “docker run”, especificar un usuario implica el uso de la bandera “-u”, por ejemplo, “docker run -u 1000”, donde 1000 es el ID de usuario. Estos fragmentos de código ilustran cómo establecer y gestionar los permisos de usuario dentro de una imagen de Docker, promoviendo la seguridad al minimizar el uso de privilegios elevados.

Test Negativo:
    
    
    # Example Negative  
      
    # Uses Ubuntu as a parent image  
    FROM ubuntu:22.04  
      
    # Create a non-root user and switch to it  
    RUN useradd -m myuser  
    USER myuser  
      
    # When the container launches, bash shell also launches  
    CMD ["/bin/bash"]`

Test Positivo:
    
    
    #Example Positive  
      
    # Uses Ubuntu as a parent image  
    FROM ubuntu:22.04  
      
    # When the container launches, bash shell also launches  
    CMD ["/bin/bash"]

* * *

#### Demostración de obtener acceso non-root en un Dockerfile:

Esta demostración viola los principios de Elevación de Privilegios, Acceso al Sistema de Archivos y las Mejores Prácticas de Seguridad.

#### ¿Qué es el archivo passwd?

El archivo `/etc/passwd` dentro de un contenedor de Docker es un archivo de sistema estándar que almacena información de cuentas de usuario. Se utiliza comúnmente en sistemas operativos tipo Unix, incluyendo Linux. Cada línea en el archivo representa una cuenta de usuario y contiene varias piezas de información acerca de ese usuario.

El formato típico de una línea en el archivo `/etc/passwd` es el siguiente:

`username:password:userID:groupID:userInfo:homeDirectory:loginShell`

Aquí un desglose de los campos:

`**username:** El nombre del usuario.  
**password:** Generalmente representado por ‘x’, indicando que la contraseña cifrada real se almacena en el archivo /etc/shadow u otro lugar seguro.  
**userID (UID):** Un identificador numérico único para el usuario.  
**groupID (GID):** El identificador numérico del grupo principal del usuario.  
**userInfo:** Información adicional sobre el usuario (a menudo, el nombre completo).  
**homeDirectory:** El directorio principal del usuario, donde comúnmente inicia sesión.  
**loginShell:** La shell predeterminada del usuario.`

#### ¿Por qué demostrar un exploit inseguro?

En un sistema típico tipo Unix, incluido Linux, el archivo `/etc/passwd` se utiliza para almacenar información de cuentas de usuario y tradicionalmente tiene permisos de lectura para todos los usuarios. Los permisos pueden parecer así:

`-rw-r — r — 1 root root 1153 Dec 8 12:34 /etc/passwd`

Aquí, el archivo es legible por todos, pero solo modificable por el usuario _root_. Si un usuario _non-root_ tiene la capacidad de escribir en el archivo `/etc/passwd`, esto puede potencialmente llevar a vulnerabilidades y riesgos de seguridad. Aquí hay algunas razones:

  1. Elevación de Privilegios del Usuario: Si un usuario _non-root_ puede escribir en el archivo `/etc/passwd`, podría manipular las entradas en él. Esto podría incluir la modificación del UID (Identificación de Usuario) o GID (Identificación de Grupo) de usuarios existentes, permitiendo potencialmente al usuario _non-root_ escalar sus privilegios.
  2. Suplantación de Identidad de Usuario: Al modificar el archivo `/etc/passwd`, un usuario _non-root_ podría intentar suplantar a otros usuarios o obtener acceso no autorizado a recursos asociados con esos usuarios. Esto podría provocar violaciones de seguridad y acceso no autorizado.
  3. Integridad del Sistema: El archivo `/etc/passwd` es crucial para el funcionamiento adecuado del sistema. Si sus contenidos se manipulan, podría causar inestabilidad del sistema, errores o interrupciones en la autenticación de usuarios.
  4. Escape del Contenedor: Si esta manipulación ocurre dentro de un entorno contenerizado, podría utilizarse como parte de un ataque más amplio para escapar del contenedor y obtener acceso no autorizado al sistema principal.



#### Demostración

Ejecuté el comando docker build en las pruebas anteriores del Dockerfile, tanto las positivas como las negativas (que aparecen arriba), seguido del comando docker run. En la prueba positiva, donde el Dockerfile carecía de un campo “USER”, utilicé el comando `echo “test” >> /etc/passwd` para ilustrar el acceso al comando. Por otro lado, en la prueba negativa con el campo “USER”, demostré la prevención de obtener control de usuario _root_.

![](https://cdn-images-1.medium.com/max/800/1*7Oj4PLN8zLK1v-CxN32zvQ.png)Test Negativo![](https://cdn-images-1.medium.com/max/800/1*ybZWBBtKcghfl0Srph3xvg.png)Test Positivo

#### Conclusión

En conclusión, Docker ha transformado por completo el panorama de la implementación de aplicaciones a través de su innovadora plataforma de contenerización. Proporciona a los desarrolladores contenedores ágiles y portátiles, simplificando los flujos de trabajo de desarrollo. La amplia adopción de Docker se atribuye a su interfaz fácil de usar, compatibilidad en diversas plataformas y la utilización eficiente de recursos. Sin embargo, a medida que evoluciona la tecnología de contenerización, introduce desafíos de seguridad, especialmente en la gestión de vulnerabilidades.

Para abordar estos problemas, es crucial seguir las mejores prácticas y directrices de OWASP y el CIS Docker Benchmark. Evitar otorgar privilegios de usuario _root_ en los contenedores de Docker es un paso de seguridad importante, como se muestra al manipular el archivo `/etc/passwd`, lo que expone riesgos potenciales en la gestión de la información de cuentas de usuarios. Asegurar entornos de Docker depende de gestionar adecuadamente a los usuarios, resaltando la importancia de utilizar usuarios _non-root_ en los Dockerfiles y configuraciones en tiempo de ejecución.

Como desarrolladores, incorporar estas prácticas es fundamental para mitigar riesgos de seguridad y asegurar el establecimiento de un entorno de implementación sólido y seguro.

* * *

#### Referencias

<https://www.docker.com/blog/docker-index-dramatic-growth-in-docker-usage-affirms-the-continued-rising-power-of-developers/>

<https://www.docker.com/blog/container-security-and-why-it-matters/>

<https://linuxize.com/post/etc-passwd-file/>

<https://owasp.org/www-community/Access_Control>

<https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html#rule-2-set-a-user>

<https://www.cisecurity.org/insights/blog/announcing-cis-benchmark-for-docker-1-6>

<https://docs.docker.com/engine/reference/builder/#user>

By [Kfir Gisman](https://medium.com/@Kfir-G) on [January 4, 2024](https://medium.com/p/aafb40f7766b).

[Canonical link](https://medium.com/@Kfir-G/asegurando-docker-mejores-pr%C3%A1cticas-para-usuarios-non-root-aafb40f7766b)

Exported from [Medium](https://medium.com) on December 20, 2025.
