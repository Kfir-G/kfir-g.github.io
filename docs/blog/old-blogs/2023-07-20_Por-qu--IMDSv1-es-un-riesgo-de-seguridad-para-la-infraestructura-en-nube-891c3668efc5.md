---
title: Por Qu  Imdsv1 Es Un Riesgo De Seguridad Para La Infraestructura En Nube
published: true
date: 2023-07-20 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/891c3668efc5
---

# Por qué IMDSv1 es un riesgo de seguridad para la infraestructura en nube

El Servicio de Metadatos de Instancia (IMDS) de Amazon proporciona una forma para que las aplicaciones que se ejecutan en instancias de… 

* * *

### Por qué IMDSv1 es un riesgo de seguridad para la infraestructura en nube

![](https://cdn-images-1.medium.com/max/800/1*Kb2iIeHxk8rpuiPUouZq5w.jpeg)

El Servicio de Metadatos de Instancia (IMDS) de Amazon proporciona una forma para que las aplicaciones que se ejecutan en instancias de Amazon Elastic Compute Cloud (EC2) accedan a los metadatos y datos de usuario de la instancia. Sin embargo, se ha demostrado que la primera versión de este servicio, IMDSv1, es vulnerable a ataques de falsificación de solicitudes en el lado del servidor (SSRF). En esta publicación del blog, explicaremos los riesgos de seguridad asociados con el uso de IMDSv1 y por qué es importante actualizar a IMDSv2, que es más seguro.

#### **¿Cuál es la diferencia entre el protocolo?**

IMDSv1 e IMDSv2 son dos versiones del Servicio de Metadatos de Instancia (IMDS) proporcionado por AWS. IMDS es un servicio que permite a las instancias EC2 acceder a metadatos y credenciales desde un punto final local.

La principal diferencia entre IMDSv1 e IMDSv2 es que IMDSv2 utiliza `session autherntication`proteger contra cortafuegos abiertos (open firewall), proxies inversos y vulnerabilidades SSRF. IMDSv2 requiere que el software que se ejecuta en la instancia EC2 obtenga un `secret token` mediante una solicitud PUT antes de realizar cualquier solicitud GET al IMDS. El token caduca después de un máximo de seis horas y se puede utilizar para solicitudes posteriores dentro de la misma sesión.

Por otro lado, IMDSv1 utiliza solicitudes GET **no autenticadas** y es más susceptible a ataques SSRF. IMDSv1 no requiere tokens ni gestión de sesiones.

AWS [recomienda](https://aws.amazon.com/blogs/security/defense-in-depth-open-firewalls-reverse-proxies-ssrf-vulnerabilities-ec2-instance-metadata-service/) adoptar IMDSv2 y restringir el acceso solo a IMDSv2 para mayor seguridad. Puede usar AWS Systems Manager para hacer cumplir IMDSv2 en sus instancias EC2. También puede usar las últimas versiones de los SDK y CLI de AWS que admiten IMDSv2.

#### Cómo aplicar IMDSv2 en el archivo yaml de Terraform

Puede aplicar el uso de IMDSv2 en una instancia EC2 lanzada por [Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance#http_tokens) configurando el bloque `metadata_options`dentro del recurso `aws_instance`. Dentro de este bloque, puede establecer el atributo `http_tokens` en `required`, lo que hará cumplir el uso de IMDSv2 en la instancia.

Aquí hay un ejemplo:
    
    
    resource "aws_instance" "example" {  
      ami           = "ami-0c94855ba95c71c99" #Este es un ejemplo ID AMI Amazon Linux 2; reemplace con el ID AMI deseado para su región   
      
      metadata_options {  
        http_tokens = "required"  
      }  
    }

Esta configuración lanzará una instancia EC2 que requiere el uso de IMDSv2 para acceder a sus metadatos.

#### Cómo aplicar IMDSv2 con AWS CLI

Puede usar el comando modify-instance-metadata-options del AWS CLI para hacer cumplir el uso de IMDSv2 en una instancia EC2 existente. Este comando le permite modificar los parámetros de metadatos de instancia en una instancia en ejecución o detenida.
    
    
    aws ec2 modify-instance-metadata-options --instance-id i-0123456789abcdef --http-tokens required --http-endpoint enabled

En este ejemplo, reemplace `i0123456789abcdef`con el ID de la instancia que desea modificar. La opción`--http-tokens required` hace cumplir el uso de IMDSv2 en la instancia, mientras que la opción`--http-endpoint enabled `asegura que el servicio de metadatos de instancia permanezca habilitado.

#### ¿Qué cosas notables sucedieron en el pasado?

En junio de 2021, un actor amenazante conocido como UNC2903 [explotó](https://www.breaches.cloud/incidents/unc2903/) una vulnerabilidad en la herramienta de administración de bases de datos Adminer para cosechar y abusar credenciales utilizando el Servicio de Metadatos de Instancia (IMDS) de Amazon. El atacante utilizó una caja relé con un script redireccionador 301 para engañar al servidor víctima y hacer que siguiera la redirección y devolviera un error que contenía credenciales de API de AWS. Luego, el atacante utilizó estas credenciales para acceder a la cuenta de AWS de la víctima. Este ataque destaca la importancia de actualizar a IMDSv2, que habría mitigado este ataque.

#### Conclusión

En conclusión, IMDSv1 es un riesgo de seguridad para la infraestructura en la nube debido a su vulnerabilidad a los ataques de falsificación de solicitudes en el lado del servidor (SSRF). Por otro lado, IMDSv2 utiliza autenticación de sesión y requiere que se obtenga un token secreto antes de realizar cualquier solicitud al IMDS, lo que proporciona una mayor seguridad contra los ataques SSRF. Es importante actualizar a IMDSv2 y aplicar su uso en las instancias EC2, ya sea a través de la configuración de Terraform o mediante el uso del AWS CLI. Incidentes notables, como el llevado a cabo por UNC2903, destacan la importancia de actualizar a IMDSv2 para mitigar el riesgo de cosecha y abuso de credenciales.

#### Referencias:

Use IMDSv2 — Amazon Elastic Compute Cloud. [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html.)

How can I use Systems Manager automation to enforce that only IMDSv2 is used to access instance metadata from my Amazon EC2 instance? <https://repost.aws/knowledge-center/ssm-ec2-enforce-imdsv2>

Add defense in depth against open firewalls, reverse proxies, and SSRF vulnerabilities with enhancements to the EC2 Instance Metadata Service <https://aws.amazon.com/blogs/security/defense-in-depth-open-firewalls-reverse-proxies-ssrf-vulnerabilities-ec2-instance-metadata-service/>

* * *

**Leerlo en ingles:**[**** Why IMDSv1 is a Security Risk for Cloud Infrastructure](https://medium.com/@kfir_g/why-imdsv1-is-a-security-risk-for-cloud-infrastructure-350bbe4e8c94)

By [Kfir Gisman](https://medium.com/@Kfir-G) on [July 20, 2023](https://medium.com/p/891c3668efc5).

[Canonical link](https://medium.com/@Kfir-G/por-qu%C3%A9-imdsv1-es-un-riesgo-de-seguridad-para-la-infraestructura-en-nube-891c3668efc5)
