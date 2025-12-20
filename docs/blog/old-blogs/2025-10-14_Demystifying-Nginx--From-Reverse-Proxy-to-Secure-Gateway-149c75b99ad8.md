---
title: Demystifying Nginx  From Reverse Proxy To Secure Gateway
published: true
date: 2025-10-14 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/149c75b99ad8
---

# Demystifying Nginx: From Reverse Proxy to Secure Gateway

When I started building TinyURL, a simple FastAPI + PostgreSQL service for shortening URLs, I thought Nginx would just “serve traffic.”… 

* * *

### Demystifying Nginx: From Reverse Proxy to Secure Gateway

![](https://cdn-images-1.medium.com/max/800/1*5v3hP9YGA3i-1K5f9gVDFA.jpeg)Photo by RealToughCandy.com: <https://www.pexels.com/photo/person-holding-a-sticker-with-green-letters-11035538/>

When I started building **TinyURL** , a simple FastAPI + PostgreSQL service for shortening URLs, I thought Nginx would just “serve traffic.” Turns out, it became the most critical piece of my deployment — the gatekeeper that made everything behind it work smoothly and securely.

In this post, I’ll share what I actually learned while wiring Nginx into my FastAPI backend and Streamlit frontend, both running in Docker.

* * *

### 1\. Nginx is more than a web server

Before this project, I mostly thought of Nginx as something you use to “host static files.” In reality, it’s a powerful **reverse proxy** — it sits in front of your app, receives every incoming request, and decides where it should go.

In my stack:
    
    
    Client → Nginx → FastAPI (backend) → Postgres  
                         ↳ Streamlit (UI)

Nginx doesn’t just forward traffic- it also:

  * Handles HTTPS termination
  * Adds security headers
  * Manages WebSocket upgrades for Streamlit
  * Hides internal services (FastAPI and Postgres) from the public internet



Once I saw that flow working inside Docker Compose, it finally clicked how production apps are structured.

* * *

### 2\. Reverse proxying is all about headers and trust

Here’s a simplified version of my production config:
    
    
    location /api/ {  
        proxy_pass http://fastapi:8000;  
        proxy_set_header Host $host;  
        proxy_set_header X-Real-IP $remote_addr;  
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  
        proxy_set_header X-Forwarded-Proto $scheme;  
    }

These headers are crucial. Without them, FastAPI would have no idea what the original client’s IP or scheme was.  
`X-Forwarded-Proto` in particular tells the backend if the original request came over HTTPS- that’s how FastAPI can generate correct redirect URLs or absolute links.

This part made me appreciate how Nginx “translates” external requests for internal services while preserving client context.

* * *

### 3\. HTTPS is not optional

The first time I tried running my app on an EC2 instance, Chrome immediately complained: _“Not secure.”_

That’s when I integrated **Let’s Encrypt** with Nginx. The setup was surprisingly simple once I understood what was happening:

  * The `/.well-known/acme-challenge/` path lets Certbot verify domain ownership.
  * Once validated, Let’s Encrypt issues free SSL certificates.
  * Nginx then terminates HTTPS using those certs:


    
    
    ssl_certificate /etc/letsencrypt/live/kg-tiny-url.xyz/fullchain.pem;  
    ssl_certificate_key /etc/letsencrypt/live/kg-tiny-url.xyz/privkey.pem;  
    ssl_protocols TLSv1.2 TLSv1.3;

I also learned to add a separate HTTP server block just to redirect everything to HTTPS. Small detail, big difference.

* * *

### 4\. Security headers are free wins

I wanted to understand what real production configs look like, so I dug into HTTP security headers. Adding these took one line each in Nginx but instantly hardened the app:
    
    
    add_header Strict-Transport-Security "max-age=31536000" always;  
    add_header X-Frame-Options "DENY" always;  
    add_header X-Content-Type-Options "nosniff" always;  
    add_header Content-Security-Policy "default-src 'self'" always;

You don’t notice them in daily use, but tools like Mozilla Observatory or Lighthouse will thank you.

* * *

### 5\. Docker networking just works- if you name things right

Inside Docker Compose, every container gets a DNS name. My `proxy_pass http://fastapi:8000` line works because the FastAPI container is literally named **fastapi** in the YAML file.

That’s how Nginx can find it without any IP addresses.  
Once I realized that Docker’s internal DNS makes service discovery effortless, networking suddenly felt simple instead of scary.

* * *

### 6\. The moment it all worked

After wiring it all up, I opened my browser to:
    
    
    https://kg-tiny-url.xyz/ui/

The Streamlit UI loaded. When I shortened a link, it called the FastAPI backend through `/api/`.  
Everything was encrypted, routed, and logged properly- all through Nginx.

That was the moment I understood why every real-world deployment uses a reverse proxy.

* * *

### 7\. Final takeaway

Nginx isn’t just a traffic router- it’s the **security layer, performance booster, and network translator** that makes containerized apps production-ready.

By the end of this project, I didn’t just “set up Nginx.” I learned how the internet actually talks to my code.

* * *

If you’re new to Nginx or just want to deepen your understanding, I highly recommend pairing this write-up with **this free YouTube tutorial** (<https://www.youtube.com/watch?v=7VAI73roXaY>) for a hands-on introduction, and **the Udemy “NGINX Crash Course”** ([https://www.udemy.com/course/nginx-crash-course/?kw=ngi&src=sac](https://www.udemy.com/course/nginx-crash-course/?kw=ngi&src=sac)) for a more structured, in-depth path. These two resources helped me grasp concepts like reverse proxying, SSL termination, WebSocket upgrades, and scaling more confidently — and I think they’ll help you too.

By [Kfir Gisman](https://medium.com/@Kfir-G) on [October 14, 2025](https://medium.com/p/149c75b99ad8).

[Canonical link](https://medium.com/@Kfir-G/demystifying-nginx-from-reverse-proxy-to-secure-gateway-149c75b99ad8)

Exported from [Medium](https://medium.com) on December 20, 2025.
