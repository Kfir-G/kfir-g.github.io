---
title: Why Imdsv1 Is A Security Risk For Cloud Infrastructure
published: true
date: 2023-08-06 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/350bbe4e8c94
---

# Why IMDSv1 is a Security Risk for Cloud Infrastructure

Amazon’s Instance Metadata Service (IMDS) provides a way for applications running on Amazon Elastic Compute Cloud (EC2) instances to access… 

* * *

### Why IMDSv1 is a Security Risk for Cloud Infrastructure

![](https://cdn-images-1.medium.com/max/800/0*3dHB5-eZ7bHmcuTe.jpeg)

Amazon’s Instance Metadata Service (IMDS) provides a way for applications running on Amazon Elastic Compute Cloud (EC2) instances to access instance metadata and user data. However, the first version of this service, IMDSv1, has been shown to be vulnerable to server-side request forgery (SSRF) attacks. In this blog post, we will explore the security risks associated with using IMDSv1 and why it is important to update to the more secure IMDSv2.

### What is the difference between the protocol?

IMDSv1 and IMDSv2 are two versions of the Instance Metadata Service (IMDS) provided by AWS. IMDS is a service that allows EC2 instances to access metadata and credentials from a local endpoint.

The main difference between IMDSv1 and IMDSv2 is that IMDSv2 uses `session authentication` to protect against open firewalls, reverse proxies, and SSRF vulnerabilities. IMDSv2 requires the software running on the EC2 instance to obtain a `secret token` using a PUT request before making any GET requests to the IMDS. The token expires after a maximum of six hours and can be used for subsequent requests within the same session.

IMDSv1, on the other hand, uses **unauthenticated** GET requests and is more susceptible to SSRF attacks. IMDSv1 does not require any tokens or session management.

AWS recommends adopting IMDSv2 and restricting access to IMDSv2 only for added security. You can use AWS Systems Manager to enforce IMDSv2 on your EC2 instances. You can also use the latest versions of AWS SDKs and CLIs that support IMDSv2.

<https://aws.amazon.com/blogs/security/defense-in-depth-open-firewalls-reverse-proxies-ssrf-vulnerabilities-ec2-instance-metadata-service/>

### How to enforce IMDSv2 on Terraform yaml file

You can enforce the use of IMDSv2 on an EC2 instance launched by Terraform by setting the `metadata_options` block within the `aws_instance `resource. Within this block, you can set the `http_tokens` attribute to `required`, which will enforce the use of IMDSv2 on the instance.

Here’s an example:
    
    
    resource "aws_instance" "example" {  
      ami           = "ami-0c94855ba95c71c99" # This is an example Amazon Linux 2 AMI ID; replace with the desired AMI ID for your region  
      instance_type = "t2.micro"  
      
      metadata_options {  
        http_tokens = "required"  
      }  
    }

This configuration will launch an EC2 instance that requires the use of IMDSv2 to access its metadata.

### **How to enforce IMDSv2 with AWS CLI**

You can use the `modify-instance-metadata-options` command of the AWS CLI to enforce the use of IMDSv2 on an existing EC2 instance. This command allows you to modify the instance metadata parameters on a running or stopped instance. Here’s an example command that enforces the use of IMDSv2 on a specified instance:
    
    
    aws ec2 modify-instance-metadata-options --instance-id i-0123456789abcdef --http-tokens required --http-endpoint enabled

In this example, replace `i-0123456789abcdef` with the ID of the instance you want to modify. The`--http-tokens required` option enforces the use of IMDSv2 on the instance, while the`--http-endpoint enabled` option ensures that the instance metadata service remains enabled.

### What are noticeable thing that happened in the past

In June 2021, a threat actor known as UNC2903 [exploited](https://www.breaches.cloud/incidents/unc2903/) a vulnerability in the Adminer database management tool to harvest and abuse credentials using Amazon’s Instance Metadata Service (IMDS). The attacker used a relay box with a 301 redirect script to fool the victim’s server into following the redirect and returning an error that contained AWS API credentials. The attacker then used these credentials to access the victim’s AWS account. This attack highlights the importance of updating to IMDSv2, which would have mitigated this attack.

### Conclusion

In conclusion, IMDSv1 is a security risk for cloud infrastructure due to its vulnerability to server-side request forgery (SSRF) attacks. IMDSv2, on the other hand, uses session authentication and requires a secret token to be obtained before making any requests to the IMDS, providing added security against SSRF attacks. It is important to update to IMDSv2 and enforce its use on EC2 instances, either through Terraform configuration or by using the AWS CLI. Notable incidents, such as the one carried out by UNC2903, highlight the importance of updating to IMDSv2 to mitigate the risk of credential harvesting and abuse.

### References:

Use IMDSv2 — Amazon Elastic Compute Cloud. [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html.)

How can I use Systems Manager automation to enforce that only IMDSv2 is used to access instance metadata from my Amazon EC2 instance? <https://repost.aws/knowledge-center/ssm-ec2-enforce-imdsv2>

Add defense in depth against open firewalls, reverse proxies, and SSRF vulnerabilities with enhancements to the EC2 Instance Metadata Service <https://aws.amazon.com/blogs/security/defense-in-depth-open-firewalls-reverse-proxies-ssrf-vulnerabilities-ec2-instance-metadata-service/>

* * *

**Read it on Spanish:** [Por qué IMDSv1 es un riesgo de seguridad para la infraestructura en nube](https://medium.com/@kfir_g/por-qu%C3%A9-imdsv1-es-un-riesgo-de-seguridad-para-la-infraestructura-en-nube-891c3668efc5)

By [Kfir Gisman](https://medium.com/@Kfir-G) on [August 6, 2023](https://medium.com/p/350bbe4e8c94).

[Canonical link](https://medium.com/@Kfir-G/why-imdsv1-is-a-security-risk-for-cloud-infrastructure-350bbe4e8c94)
