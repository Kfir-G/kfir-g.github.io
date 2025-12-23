---
title: From Passive FastAPI Developer to Real FastAPI Engineer – Part 3: Middleware and Background Tasks
published: true
date: 2025-12-20 03:28:33 UTC
tags: fastapi,starlette,asgi,python,softwareengineering
canonical_url: https://kfir-g.dev/blog/blogs/2025-12-20_From-Passive-FastAPI-Developer-to-Real-FastAPI-Engineer--Part-3.md
---

# From Passive FastAPI Developer to Real FastAPI Engineer – Part 3: Middleware and Background Tasks

Exploring ASGI middleware, background tasks, and advanced request/response patterns in FastAPI.

---

### ASGI Middleware in FastAPI

Middleware is a layer that sits between the server and your application. In ASGI, middleware is **an async callable** that can intercept requests and responses:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request

app = FastAPI()

class SimpleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Request URL: {request.url}")
        response = await call_next(request)
        response.headers['X-Custom-Header'] = 'Hello from Middleware'
        return response

app.add_middleware(SimpleMiddleware)
````

Middleware can be used for:

* Logging requests and responses
* Adding custom headers
* Handling authentication and authorization
* Measuring performance or request duration

---

### Background Tasks

FastAPI supports running tasks **after sending the response**, which is essential for operations that don’t need to block the request:

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-data/")
async def send_data(data: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Received: {data}")
    return {"message": "Data received. Logging in background."}
```

Benefits:

* Improves response time for users
* Allows long-running tasks to run asynchronously
* Integrates cleanly with async applications

---

### Request and Response Lifecycle

Understanding the request/response lifecycle is key for advanced FastAPI applications:

```
Client → ASGI Server → Middleware → Path Operation → Response → Middleware → ASGI Server → Client
```

* **Request passes through middleware first**
* **Path operation executes next**
* **Response goes back through middleware before returning to client**

Middleware can **mutate request or response**, while background tasks run **after the response is sent**.

---

### Combining Middleware and Background Tasks

You can combine these features for advanced use cases:

* Logging requests and saving metrics in background
* Authenticating users and sending notifications asynchronously
* Transforming requests and caching responses

```python
@app.post("/upload/")
async def upload_file(file: bytes, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_file, file)
    return {"status": "File received, processing in background"}
```

This pattern is essential for **high-performance, real-world FastAPI apps**.

---

### Best Practices

1. **Keep middleware lightweight** – avoid blocking operations.
2. **Use background tasks for I/O-heavy operations**.
3. **Leverage ASGI features for streaming and WebSocket scenarios**.
4. **Monitor performance** – middleware can introduce latency if overused.

---

### References

* [FastAPI Middleware Documentation](https://fastapi.tiangolo.com/tutorial/middleware/)
* [Starlette ASGI Middleware](https://www.starlette.io/middleware/)
* [Background Tasks in FastAPI](https://fastapi.tiangolo.com/tutorial/background-tasks/)

[Canonical link](https://kfir-g.dev/blog/old-blogs/2025-12-20_From-Passive-FastAPI-Developer-to-Real-FastAPI-Engineer--Part-3.md)
