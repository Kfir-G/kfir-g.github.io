---
title: From Passive FastAPI Developer to Real FastAPI Engineer – Part 4: Lifespan, Startup, Shutdown, and State
published: true
date: 2025-12-25 00:00:00 UTC
tags: fastapi,starlette,asgi,python,softwareengineering
canonical_url: https://kfir-g.dev/blog/blogs/2025-12-20_From-Passive-FastAPI-Developer-to-Real-FastAPI-Engineer--Part-4.md
---

# From Passive FastAPI Developer to Real FastAPI Engineer – Part 4: Lifespan, Startup, Shutdown, and State

If you truly want to think in **ASGI**, you must understand what happens **outside** request handling.

Requests are only one part of the application lifecycle.  
In this part, we’ll dive into **ASGI lifespan events**, application **startup/shutdown**, and how **state** is managed correctly in FastAPI.

---

## The ASGI Lifespan Protocol

ASGI defines a **lifespan scope** that is separate from HTTP and WebSocket scopes.

At a protocol level, the server sends events like:

```
lifespan.startup
lifespan.shutdown
```

Your application must respond with:

```
lifespan.startup.complete
lifespan.shutdown.complete
```

This is how the server knows when your app is **ready to accept traffic** or **safe to terminate**.

FastAPI (via Starlette) abstracts this-but understanding it matters.

---

## Startup and Shutdown in FastAPI (The Old Way)

You may already know this pattern:

```python
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("App is starting")

@app.on_event("shutdown")
async def shutdown_event():
    print("App is shutting down")
```

This works, but it has limitations:

* Harder to test
* Less explicit lifecycle control
* Being gradually replaced by the **lifespan context manager**

---

## The Modern Way: Lifespan Context Manager

FastAPI now recommends using an **async context manager**:

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup logic here")
    yield
    print("Shutdown logic here")

app = FastAPI(lifespan=lifespan)
```

Why this is better:

* Clear lifecycle boundaries
* One place for resource management
* Easier to reason about startup vs shutdown
* Aligns directly with ASGI lifespan semantics

Think of it as:

```
enter → app runs → exit
```

---

## What Belongs in Startup?

Startup is for **process-level resources**, not request-level work.

Good examples:

* Database connections
* Redis clients
* HTTP client pools
* Loading ML models
* Initializing caches
* Starting background consumers

Bad examples:

* Per-user logic
* Request validation
* Anything depending on request data

---

## Application State (`app.state`)

FastAPI exposes a shared state object:

```python
app.state.db = db_connection
app.state.redis = redis_client
```

You can then access it inside requests:

```python
from fastapi import Request

@app.get("/items")
async def get_items(request: Request):
    db = request.app.state.db
    return {"status": "ok"}
```

Important properties of `app.state`:

* Shared across all requests
* Lives for the entire app lifetime
* **Not request-safe by default**
* Must hold thread-safe / async-safe objects

This is **not** global variables - it’s explicit, controlled state.

---

## Why Not Global Variables?

Globals seem easy:

```python
db = None
```

But they break down when:

* Running multiple workers
* Reloading with Uvicorn
* Testing with TestClient
* Sharing state across async tasks

`app.state` ties the resource lifecycle to the ASGI app, not the Python module.

---

## Shutdown: Cleaning Up Correctly

Shutdown is where you **release resources**:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = await create_client()
    yield
    await app.state.client.aclose()
```

If you don’t close:

* Connections leak
* File descriptors accumulate
* Containers fail graceful shutdown
* Kubernetes SIGTERM handling breaks

This is where **real production bugs** often hide.

---

## How This Fits with Middleware and Background Tasks

Let’s connect the dots:

| Feature          | Runs When      | Purpose                   |
| ---------------- | -------------- | ------------------------- |
| Lifespan         | App start/stop | Manage global resources   |
| Middleware       | Every request  | Cross-cutting concerns    |
| Background tasks | After response | Deferred per-request work |
| Path operation   | During request | Business logic            |

Each layer has a **clear responsibility**.

Mixing them leads to fragile systems.

---

## A Real-World Pattern

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient()
    yield
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)
```

Used with:

```python
@app.get("/external")
async def call_external(request: Request):
    client = request.app.state.http
    r = await client.get("https://example.com")
    return {"status": r.status_code}
```

This avoids:

* Creating clients per request
* Global variables
* Resource leaks

This is **ASGI thinking**.

---

## Common Mistakes to Avoid

1. ❌ Doing I/O inside middleware startup logic
2. ❌ Storing request data in `app.state`
3. ❌ Forgetting to close connections on shutdown
4. ❌ Using globals instead of lifespan-managed state
5. ❌ Mixing background tasks with startup logic

---

## Mental Model Upgrade

Stop thinking:

> “FastAPI runs my function when a request arrives”

Start thinking:

> “I am writing an ASGI application with a defined lifecycle”

That shift is what separates **framework users** from **engineers**.

---

Conclusion

Using middleware and background tasks wisely keeps your FastAPI app fast and maintainable. Even small improvements here pay off in overall performance and clarity.

---

## References

* [https://asgi.readthedocs.io/en/latest/specs/lifespan.html](https://asgi.readthedocs.io/en/latest/specs/lifespan.html)
* [https://fastapi.tiangolo.com/advanced/events/](https://fastapi.tiangolo.com/advanced/events/)
* [https://www.starlette.io/lifespan/](https://www.starlette.io/lifespan/)

[Canonical link](https://kfir-g.dev/blog/blogs/2025-12-25_From-Passive-FastAPI-Developer-to-Real-FastAPI-Engineer--Part-4.md)
