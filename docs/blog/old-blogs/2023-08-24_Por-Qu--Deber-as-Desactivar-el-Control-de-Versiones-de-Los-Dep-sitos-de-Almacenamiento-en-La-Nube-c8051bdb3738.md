---
title: Por Qu  Deber As Desactivar El Control De Versiones De Los Dep Sitos De Almacenamiento En La Nube
published: true
date: 2023-08-24 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/c8051bdb3738
---

# Por Qué Deberías Desactivar el Control de Versiones de Los Depósitos de Almacenamiento en La Nube

This blog is available in English here: https://medium.com/@kfir_g/why-you-should-disable-cloud-storage-bucket-versioning-e6638beffac6 

* * *

### Por Qué Deberías Desactivar el Control de Versiones de Los Depósitos de Almacenamiento en La Nube

* * *

This blog is available in English here: <https://medium.com/@kfir_g/why-you-should-disable-cloud-storage-bucket-versioning-e6638beffac6>

* * *

El almacenamiento en la nube es un servicio que te permite almacenar y acceder a tus datos en la infraestructura de Google. Ofrece alta disponibilidad, durabilidad, escalabilidad y rendimiento para tus datos. Una de las características que ofrece el almacenamiento en la nube es el control de versiones de los depósitos, que te permite mantener varias versiones de un objeto en el mismo depósito. Esto puede ser útil para recuperarse de eliminaciones o sobreescrituras accidentales, así como para preservar versiones históricas de tus datos. Sin embargo, en esta blog, explicaré por qué podrías querer desactivar el control de versiones de los depósitos de almacenamiento en la nube y cómo hacerlo.

### Las Desventajas del Control de Versiones de Los Depósitos de Almacenamiento en La Nube

Si bien el control de versiones de los depósitos de almacenamiento en la nube puede tener algunos beneficios, también tiene algunas desventajas que debes tener en cuenta. Estas son algunas de las razones por las que podrías querer desactivar el control de versiones de los depósitos de almacenamiento en la nube:

  * **Costo** : Cada versión de un objeto se cobra a la misma tarifa que cuando estaba activo, por lo que mantener varias versiones puede aumentar sus costos de almacenamiento. Puedes usar la administración del ciclo de vida de los objetos para eliminar automáticamente las versiones anteriores, pero esto puede no ser suficiente para tus necesidades. Por ejemplo, si tienes una gran cantidad de objetos que cambian con frecuencia, podrías terminar con muchas versiones que no necesitas. Además, si habilitas el control de versiones en un depósito que ya contiene objetos, todos los objetos existentes se tratarán como versiones activas y se te cobrará por ellas también.
  * **Complejidad** : Gestionar varias versiones de un objeto puede añadir complejidad a la lógica y los flujos de trabajo de tu aplicación. Necesitas especificar el número de generación de la versión a la que quieres acceder, y manejar los casos en los que no hay versiones activas o no actuales disponibles. Por ejemplo, si quieres listar todos los objetos de un depósito, necesitas usar el parámetro `versions`para incluir tanto las versiones activas como las no actuales, o usar el parámetro `prefixes`para agruparlas por nombre. Si quieres descargar o eliminar un objeto, necesitas usar el parámetro generación para especificar qué versión quieres. Si no especificas un número de `generation`, Cloud Storage usará por defecto la última versión activa.
  * **Seguridad** : Si tienes datos sensibles que quieres eliminar permanentemente, desactivar el versionado de depósitos de Cloud Storage puede asegurar que no queden rastros de los datos en el depósito. De lo contrario, necesitas eliminar cada versión individualmente especificando el número de generación, o usar la gestión del ciclo de vida de los objetos para eliminarlos después de un cierto período de tiempo. Sin embargo, esto puede no ser suficiente para garantizar que tus datos se borren completamente de los servidores de Google. Según la [documentación](https://cloud.google.com/storage/docs/object-versioning?hl=es-419#permanently_delete) de Google- Google puede retener las versiones eliminadas durante algún tiempo después de la eliminación y esas versiones eliminadas pueden seguir siendo accesibles por los usuarios autorizados hasta que se borren permanentemente. Por lo tanto, si quieres evitar cualquier riesgo potencial de fuga o violación de datos, desactivar el versionado de depósitos de Cloud Storage podría ser una mejor opción.



### Cómo Desactivar el Versionado de Depósitos de Cloud Storage

Si decides que el versionado de depósitos de Cloud Storage no es adecuado para tus necesidades, puedes desactivarlo fácilmente usando uno de los siguientes métodos:

Consola de Google Cloud: Puedes usar la consola de Google Cloud para gestionar tus depósitos y objetos. Para desactivar el versionado de depósitos de Cloud Storage para un depósito, sigue estos pasos:

  1. Ve a la página [Navegador de Cloud Storage] en la consola de Google Cloud.
  2. Selecciona el depósito para el que quieres desactivar el versionado de depósitos de Cloud Storage.
  3. Haz clic en el botón **Editar** depósito en la parte superior de la página.
  4. En la sección **Versionado** , desmarca la casilla junto a **Habilitar versionado**.
  5. Haz clic en **Guardar** para aplicar los cambios.



**gsutil** : Puedes usar la herramienta de línea de comandos gsutil para realizar diversas operaciones en tus depósitos y objetos. Para desactivar el versionado de depósitos de Cloud Storage para un depósito, usa este comando:
    
    
    gsutil versioning set off gs://<bucket_name>

Reemplaza `<bucket_name>`con el nombre de tu depósito.

**API de Cloud Storage:** Puedes usar la API de Cloud Storage para interactuar programáticamente con tus depósitos y objetos. Para desactivar el versionado de depósitos de Cloud Storage para un depósito, envía una solicitud PATCH a este punto final:
    
    
    PATCH https://storage.googleapis.com/storage/v1/b/<bucket_name>

Reemplaza `bucket_name`con el nombre de tu depósito. En el cuerpo de la solicitud, establece la propiedad `versioning.enabled`en `false`. Por ejemplo:
    
    
    {  
      "versioning": {  
        "enabled": false  
      }  
    }

**Terraform** :
    
    
    resource "google_storage_bucket" "bucket_name" {  
      ...  
      versioning {  
        enabled = false  
      }  
    }

### Conclusión

El versionado de depósitos de Cloud Storage es una característica que puede ayudarte a preservar y restaurar múltiples versiones de tus objetos en el mismo depósito. Sin embargo, también tiene algunos inconvenientes que podrían superar sus beneficios, como el coste, la complejidad y la seguridad. Por lo tanto, es posible que quieras desactivar el versionado de depósitos de Cloud Storage para tus depósitos, dependiendo de tu caso de uso y requisitos. Puedes usar la consola de Google Cloud, la herramienta de línea de comandos gsutil o la API de Cloud Storage para desactivar el versionado de depósitos de Cloud Storage fácil y rápidamente.

* * *

### Referencias

  1. <https://cloud.google.com/storage/docs/using-versioned-objects>
  2. <https://cloud.google.com/storage/docs/object-versioning#permanently_delete>
  3. <https://cloud.google.com/storage/docs/samples/storage-disable-versioning>
  4. <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket#enabled>



By [Kfir Gisman](https://medium.com/@Kfir-G) on [August 24, 2023](https://medium.com/p/c8051bdb3738).

[Canonical link](https://medium.com/@Kfir-G/por-qu%C3%A9-deber%C3%ADas-desactivar-el-control-de-versiones-de-los-dep%C3%B3sitos-de-almacenamiento-en-la-nube-c8051bdb3738)

Exported from [Medium](https://medium.com) on December 20, 2025.
