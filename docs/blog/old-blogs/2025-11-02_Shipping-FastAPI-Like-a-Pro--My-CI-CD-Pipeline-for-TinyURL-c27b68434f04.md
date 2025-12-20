---
title: Shipping Fastapi Like A Pro  My Ci Cd Pipeline For Tinyurl
published: true
date: 2025-11-02 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/c27b68434f04
---

# Shipping FastAPI Like a Pro: My CI/CD Pipeline for TinyURL

When I first deployed TinyURL- my FastAPI + Postgres + Nginx URL shortener-I wanted a workflow that felt real, not just docker compose up… 

* * *

### Shipping FastAPI Like a Pro: My CI/CD Pipeline for TinyURL

![](https://cdn-images-1.medium.com/max/800/1*jZegZscIECNvbkss-NuwQg.jpeg)Photo by Jan Zakelj: <https://www.pexels.com/photo/a-person-holding-yellow-pipes-9389356/>

When I first deployed **TinyURL-** my FastAPI + Postgres + Nginx URL shortener-I wanted a workflow that felt real, not just `docker compose up` on my laptop. So I built a simple but solid **CI/CD pipeline** using GitHub Actions that runs tests, builds containers, and deploys automatically.

Here’s what I learned and how it all fits together.

* * *

### 1\. CI/CD isn’t about tools- it’s about trust

The main goal wasn’t automation for its own sake. It was to reach a point where every push to `main` could safely go live- no surprises, no “works on my machine.”

That mindset helped me design a pipeline that checks, builds, and ships with zero manual steps.

* * *

### 2\. The build pipeline: test early, build once

Here’s a simplified view of my GitHub Actions workflow (`.github/workflows/deploy.yml`):
    
    
    name: Deploy TinyURL  
      
    on:  
      push:  
        branches:  
          - main  
    jobs:  
      build-and-deploy:  
        runs-on: ubuntu-latest  
        steps:  
          - name: Checkout repo  
            uses: actions/checkout@v4  
          - name: Set up Python  
            uses: actions/setup-python@v5  
            with:  
              python-version: 3.11  
          - name: Install dependencies  
            run: pip install -r requirements.txt  
          - name: Run tests  
            run: pytest -q  
          - name: Build Docker images  
            run: docker compose -f docker-compose.prod.yml build  
          - name: Deploy via SSH  
            env:  
              HOST: ${{ secrets.EC2_HOST }}  
              KEY: ${{ secrets.EC2_SSH_KEY }}  
            run: |  
              echo "$KEY" > key.pem  
              chmod 600 key.pem  
              scp -i key.pem docker-compose.prod.yml ubuntu@$HOST:/home/ubuntu/tinyurl/  
              ssh -i key.pem ubuntu@$HOST "cd /home/ubuntu/tinyurl && docker compose -f docker-compose.prod.yml up -d --build"

This is the heartbeat of my project:

  * Every push triggers the pipeline.
  * Tests must pass before anything deploys.
  * The build happens **once** , and that same build runs in production.



* * *

### 3\. Containerization made CI/CD predictable

The biggest win came from using **Docker Compose** for both local and production setups.

My dev environment runs three containers:

  * `db` (Postgres)
  * `fastapi` (backend)
  * `nginx` (reverse proxy)



And my production setup? Exactly the same- except the compose file uses:

  * Different environment variables
  * Mounted SSL certs from Let’s Encrypt
  * No auto-reload or debugging



Because both stacks share the same Docker config, the CI/CD pipeline doesn’t need special cases or hacks. If it runs locally, it’ll run in CI.

* * *

### 4\. Deployment: zero downtime, one command

Once the new image is built and pushed, the EC2 host just pulls and restarts containers with:
    
    
    docker compose -f docker-compose.prod.yml up -d --build

Nginx handles live traffic, so backend containers can restart without downtime. Since FastAPI and Nginx talk over Docker’s internal network, there’s no need for manual reconfiguration.

That “click → push → deploy” feeling is addictive.

* * *

### 5\. Secrets are sacred

The pipeline uses **GitHub Secrets** to store:

  * `EC2_HOST` (server IP or domain)
  * `EC2_SSH_KEY` (private key)
  * `POSTGRES_PASSWORD`
  * `FASTAPI_SECRET_KEY`



No plaintext credentials in the repo, no `.env` files in commits. That alone made me sleep better at night.

* * *

### 6\. What I learned the hard way

  * **Don’t skip tests-** failing fast is cheaper than debugging in production.
  * **Don’t rebuild images on the server-** build once, deploy the same artifact.
  * **Keep Docker tags consistent-** otherwise `latest` will surprise you.
  * **Automate HTTPS renewal** s- my Let’s Encrypt cron job now runs monthly.



These small habits make the pipeline boring- and boring pipelines are the best kind.

* * *

### 7\. The result

Now every push to `main` runs tests, builds containers, and ships a fully reproducible environment to production. No manual steps, no “did I rebuild?” anxiety. Just continuous confidence.

* * *

### Tech Stack Recap

  * **FastAPI-** backend API
  * **PostgreSQL-** database
  * **Streamlit-** frontend
  * **Nginx-** reverse proxy
  * **GitHub Actions-** CI/CD
  * **Docker Compose-** orchestration



* * *

>  _“CI/CD isn’t about speed- it’s about peace of mind.”_

* * *

 _This post is part of my TinyURL series- real-world lessons from turning a small FastAPI project into a production-grade service._

### A message from our Founder

**Hey,**[**Sunil**](https://linkedin.com/in/sunilsandhu)**here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 3.5m monthly readers? **We don’t receive any funding, we do this to support the community. ❤️**

If you want to show some love, please take a moment to **follow me on**[**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,**[**TikTok**](https://tiktok.com/@messyfounder), [**Instagram**](https://instagram.com/sunilsandhu). You can also subscribe to our [**weekly newsletter**](https://newsletter.plainenglish.io/).

And before you go, don’t forget to **clap** and **follow** the writer️!

By [Kfir Gisman](https://medium.com/@Kfir-G) on [November 2, 2025](https://medium.com/p/c27b68434f04).

[Canonical link](https://medium.com/@Kfir-G/shipping-fastapi-like-a-pro-my-ci-cd-pipeline-for-tinyurl-c27b68434f04)

Exported from [Medium](https://medium.com) on December 20, 2025.
