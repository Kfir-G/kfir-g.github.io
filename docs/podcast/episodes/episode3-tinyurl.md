---
title: "Episode 3 – Building TinyURL in Production"
date: 2025-11-15
tags: [podcast, backend, fastapi, redis, nginx, devops, system-design]
audio: "/podcast/audio-files/episode3-tinyurl.mp3"
---

<img src="/podcast/logo.png" alt="Code with Mate Logo" width="200"/>

# Episode 3 – Dev Diary: Building TinyURL in Production

<audio controls style="width: 100%;">
  <source src="https://media.githubusercontent.com/media/Kfir-G/kfir-g.github.io/refs/heads/main/docs/podcast/audio-files/episode3-tinyurl.mp3" type="audio/mpeg">
  <source src="https://media.githubusercontent.com/media/Kfir-G/kfir-g.github.io/refs/heads/main/docs/podcast/audio-files/episode3-tinyurl.mp3" type="audio/mp3">
  Your browser does not support the audio element.
</audio>

In this episode, I walk through the full journey of building and shipping a **TinyURL-like service** to a real production environment.

This is not a theory-heavy episode. It is a hands-on breakdown of what actually happens when you take a backend system from local development to production: domains, SSL, reverse proxies, caching, databases, CI/CD pipelines, and all the mistakes along the way.

I start with a simple idea - shorten a URL - and end up deep inside system design, distributed systems, and production debugging.

---

## What We Talk About

**Goals behind the project**
- Learning how to ship a real system to production
- Deploying on AWS EC2
- Configuring domains and SSL
- Understanding ACID guarantees in practice
- Building a real CI/CD pipeline

**What a URL shortener really does**
- Why URL shorteners are read-heavy systems
- Base62 encoding and ID generation
- Hashing vs sequential IDs
- Collision avoidance and scalability tradeoffs
- Redirects, caching, and performance

**System architecture**
- FastAPI as the backend API
- PostgreSQL for persistence
- Redis for caching hot paths
- Nginx as a reverse proxy and SSL terminator
- Gunicorn for production-grade serving

**Performance and scale**
- Cache-aside strategy with Redis
- Why redirects must be fast
- Read-heavy traffic patterns
- Database bottlenecks and replication concepts

**CI/CD and deployment**
- Automatic deployment on push to main
- Docker and Docker Compose
- Common pipeline mistakes
- Environment configuration issues
- Debugging production failures

**What went wrong**
- Path and volume issues
- Nginx misconfigurations
- SSL and Certbot challenges
- Redis connection problems
- Async testing pitfalls

**What I learned**
- How production systems actually fail
- Why observability matters
- How small misconfigurations cause big outages
- How much caching changes system behavior
- Why shipping teaches faster than tutorials

---

## Technologies Used

- **FastAPI** – backend API
- **Gunicorn** – production server
- **PostgreSQL** – relational database
- **Redis** – caching layer
- **Nginx** – reverse proxy and SSL
- **Docker & Docker Compose**
- **AWS EC2**
- **GitHub Actions** – CI/CD
- **Pytest** – testing

---

## What I Want to Do Next

- Improve storage efficiency in production
- Handle multiple containers safely for ID generation
- Add rate limiting and abuse protection
- Add analytics and observability
- Explore distributed ID generation strategies

---

## References & Further Reading

- FastAPI: https://fastapi.tiangolo.com/
- Redis: https://redis.io/docs/latest/
- Nginx: https://nginx.org/en/docs/
- Gunicorn: https://docs.gunicorn.org/en/stable/
- PostgreSQL: https://www.postgresql.org/docs/
- Base62: https://en.wikipedia.org/wiki/Base62

Related articles:
- Demystifying Nginx: https://medium.com/gitconnected/demystifying-nginx-from-reverse-proxy-to-secure-gateway-149c75b99ad8
- Shipping FastAPI like a Pro: https://medium.com/python-in-plain-english/shipping-fastapi-like-a-pro-my-ci-cd-pipeline-for-tinyurl-c27b68434f04

---

This episode is for anyone who wants to stop building demos and start shipping real systems — and is ready to learn from things breaking along the way.
