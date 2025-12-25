---
title: Securing Docker  Non Root User Best Practices
published: true
date: 2023-12-29 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/5784ac25e755
---

# Securing Docker: Non-Root User Best Practices

Docker is a containerization platform that simplifies the deployment and scaling of applications by packaging them into lightweight… 

* * *

### Securing Docker: Non-Root User Best Practices

* * *

[Docker](https://www.docker.com/) is a containerization platform that simplifies the deployment and scaling of applications by packaging them into lightweight, portable units called containers. A Docker image is a standalone, executable package that includes everything needed to run a software application, including the code, runtime, libraries, and system tools. Images serve as the foundation for creating containers, enabling consistent and efficient application deployment across various environments.

Docker gained [popularity](https://www.docker.com/blog/docker-index-dramatic-growth-in-docker-usage-affirms-the-continued-rising-power-of-developers/) among developers for revolutionising application deployment through containerization. Its lightweight, portable containers provided a consistent environment, simplifying the development and deployment process. Docker’s ease of use, compatibility across different platforms, and efficient resource utilisation contributed to its rapid adoption, empowering developers to build, ship, and run applications seamlessly across diverse environments.

Docker, like any software, is not immune to [vulnerabilities](https://www.docker.com/blog/container-security-and-why-it-matters/). As containerization technology evolves, security concerns arise. Users must remain vigilant, regularly updating and monitoring Docker images to address potential vulnerabilities and ensure a secure deployment environment.

Granting a non-root user access within a Docker container serves as a simple yet impactful example to illustrate vulnerabilities in Docker, emphasising the importance of maintaining security best practices.

Running Docker containers with root user privileges can pose security risks for several reasons:

  1. Privilege Escalation: Running containers as the root user may provide a path for privilege escalation. If an attacker can exploit a vulnerability within the container, they might be able to escalate their privileges and gain control of the underlying host system.
  2. Increased Attack Surface: Allowing a Docker container to run as the root user increases the potential attack surface. If an attacker gains control of a container with root privileges, they may have more options to exploit vulnerabilities and compromise the host system.
  3. File System Access: Root access within a container means unrestricted access to the file system. This could lead to unintended modifications or deletions of critical system files, potentially causing system instability or data loss.
  4. User Namespace Isolation: Docker containers leverage user namespaces to provide some level of isolation between the container and host system users. Running containers as a non-root user ensures that even if an attacker gains access to the container, they won’t automatically have root access on the host.
  5. Security Best Practices: Following security best practices is essential to minimise potential vulnerabilities. Running containers with the least privilege necessary is a fundamental principle in container security. By using a non-root user, you adhere to the principle of least privilege, limiting the potential impact of security breaches.



Utilising a non-root user in Docker implementing the least privilege principle outlined in [OWASP Access Control](https://owasp.org/www-community/Access_Control) guidelines. This practice is discouraged, as highlighted in both the [OWASP Docker Security Sheets](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html#rule-2-set-a-user), specifically in rule #2 “set a user,” and the [CIS Docker Benchmark V1.6.0](https://www.cisecurity.org/insights/blog/announcing-cis-benchmark-for-docker-1-6) under “4.1 — Ensure that a user for the container has been created (Manual).” Following these guidelines improves container security by limiting unnecessary permissions and lessening the chance of security issues.

With a non-root user in a Dockerfile, you’d include the “USER” instruction, such as “USER myuser,” to switch to a less privileged identity. Without it, the default is running as root. In a “docker run” command, specifying a user involves the “-u” flag, like “docker run -u 1000” where 1000 is the user ID. These code snippets illustrate how to set and manage user permissions within a Docker image, promoting security by minimising the use of elevated privileges.

Negative Test:
    
    
    # Example Negative  
      
    # Uses Ubuntu as a parent image  
    FROM ubuntu:22.04  
      
    # Create a non-root user and switch to it  
    RUN useradd -m myuser  
    USER myuser  
      
    # When the container launches, bash shell also launches  
    CMD ["/bin/bash"]`

Positive Test:
    
    
    #Example Positive  
      
    # Uses Ubuntu as a parent image  
    FROM ubuntu:22.04  
      
    # When the container launches, bash shell also launches  
    CMD ["/bin/bash"]

* * *

### Demonstration of acquiring non-root access in a Dockerfile

This Demo violation of Privilege Escalation, File System Access and Security Best Practice.

#### What Is passwd File

The `/etc/passwd` file inside a Docker container is a standard system file that stores user account information. It is commonly used on Unix-like operating systems, including Linux. Each line in the file represents a user account and contains various pieces of information about that user.

The typical format of a line in the `/etc/passwd` file is as follows:

`username:password:userID:groupID:userInfo:homeDirectory:loginShell`

Here’s a breakdown of the fields:

`**username:** The name of the user.  
**password:** Usually represented by ‘x,’ indicating that the actual encrypted password is stored in the /etc/shadow file or another secure location.  
**userID (UID):** A unique numerical identifier for the user.  
**groupID (GID):** The numerical identifier of the user’s primary group.  
userInfo: Additional information about the user (often the full name).  
**homeDirectory:** The user’s home directory, where they typically start when they log in.  
**loginShell:** The user’s default shell.`

#### Why Is It Demonstrate Insecure Exploit

In a typical Unix-like system, including Linux, the `/etc/passwd` file is used to store user account information, and traditionally it has read permissions for all users. The permissions might look something like:

`-rw-r — r — 1 root root 1153 Dec 8 12:34 /etc/passwd`

Here, the file is readable by everyone, but only writable by the root user. If a non-root user has the ability to write to the` /etc/passwd` file, it can potentially lead to security vulnerabilities and risks. Here are a few reasons why:

  1. User Privilege Escalation: If a non-root user can write to the `/etc/passwd` file, they may be able to manipulate the entries within it. This could include modifying the UID (user ID) or GID (group ID) of existing users, potentially allowing the non-root user to escalate their privileges.
  2. User Identity Spoofing: By modifying the `/etc/passwd` file, a non-root user might be able to impersonate other users or gain unauthorised access to resources associated with those users. This could lead to security breaches and unauthorised access.
  3. System Integrity: The `/etc/passwd` file is crucial for the proper functioning of the system. If its contents are tampered with, it could result in system instability, errors, or disruptions in user authentication.
  4. Container Escape: If this manipulation occurs within a containerized environment, it might be used as part of a larger attack to escape the container and gain unauthorised access to the host system.



#### Demo

I executed the docker build command on the preceding positive and negative Dockerfile tests (that appears above), followed by the docker run command. In the positive test, where the Dockerfile lacked a “USER” field, I utilised a `echo “test” >> /etc/passwd` command to illustrate gaining command access. Conversely, in the negative test with the “USER” field, I demonstrated the prevention of gaining root user control.

![](https://cdn-images-1.medium.com/max/800/1*7Oj4PLN8zLK1v-CxN32zvQ.png)Negative Test![](https://cdn-images-1.medium.com/max/800/1*ybZWBBtKcghfl0Srph3xvg.png)Positive Test

#### Conclusion

In conclusion, Docker has completely transformed the landscape of application deployment through its innovative containerization platform. It provides developers with agile and portable containers, streamlining development workflows. The widespread adoption of Docker can be attributed to its user-friendly interface, compatibility across various platforms, and efficient resource utilization. However, as containerization technology evolves, it introduces security challenges, particularly in vulnerability management.

To tackle these issues, it’s crucial to follow best practices and guidelines from OWASP and the CIS Docker Benchmark. Avoiding giving root user privileges in Docker containers is an important security step, as shown by messing with the `/etc/passwd` file, which exposes potential risks in managing user account information.Securing Docker environments depends on managing users properly, highlighting the importance of using non-root users in Dockerfiles and runtime configurations.

As developers, incorporating these practices is paramount for mitigating security risks and ensuring the establishment of a robust and secure deployment environment.

* * *

#### References

<https://www.docker.com/blog/docker-index-dramatic-growth-in-docker-usage-affirms-the-continued-rising-power-of-developers/>

<https://www.docker.com/blog/container-security-and-why-it-matters/>

<https://linuxize.com/post/etc-passwd-file/>

<https://owasp.org/www-community/Access_Control>

<https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html#rule-2-set-a-user>

<https://www.cisecurity.org/insights/blog/announcing-cis-benchmark-for-docker-1-6>

<https://docs.docker.com/engine/reference/builder/#user>

By [Kfir Gisman](https://medium.com/@Kfir-G) on [December 29, 2023](https://medium.com/p/5784ac25e755).

[Canonical link](https://medium.com/@Kfir-G/securing-docker-non-root-user-best-practices-5784ac25e755)
