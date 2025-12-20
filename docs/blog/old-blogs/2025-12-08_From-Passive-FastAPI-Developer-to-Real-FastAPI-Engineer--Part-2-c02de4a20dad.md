---
title: From Passive Fastapi Developer To Real Fastapi Engineer  Part 2
published: true
date: 2025-12-08 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/c02de4a20dad
---

# From Passive FastAPI Developer to Real FastAPI Engineer- Part 2

Your First Raw ASGI App (No Frameworks Allowed). 

* * *

### From Passive FastAPI Developer to Real FastAPI Engineer- Part 2

* * *

![](https://cdn-images-1.medium.com/max/800/1*o6ATpTY8qXDv4amVOFcQCQ.jpeg)Photo by Kaue Barbier: <https://www.pexels.com/photo/28182837/>

Your First Raw ASGI App (No Frameworks Allowed).

Before FastAPI.  
Before Starlette.  
Before Uvicorn.

There is **ASGI-** the low-level async contract that makes modern Python web apps possible.

[In Part 1](https://medium.com/gitconnected/from-passive-fastapi-developer-to-real-fastapi-engineer-part-1-asgi-059a588a54ae), we learned how HTTP works at the byte level. Now in Part 2, you’re going to **build an ASGI app from scratch**.

No router.  
No response class.  
No `request.query_params`.  
Just you and the ASGI spec.

Let’s turn the black box into a glass box.

* * *

### 1\. Why Build a Raw ASGI App?

Most FastAPI developers never touch ASGI.  
Most don’t know what’s inside a request.  
Most don’t know what Uvicorn gives them.  
Most don’t know what Starlette abstracts.

This chapter fixes that.

By the end, you will understand:

  * How a web server calls your ASGI application
  * What a **scope** is.
  * How `receive()` and `send()` work.
  * How a single HTTP request becomes **events.**
  * The difference between WSGI (sync) and ASGI (async).
  * What FastAPI really sits on top of.



Once you know this layer, FastAPI becomes predictable, not magical.

* * *

### 2\. ASGI in 60 Seconds

ASGI = **Asynchronous Server Gateway Interface** The modern replacement for WSGI.

WSGI ASGI Sync Async One call, one response Event-driven HTTP only HTTP + WebSocket + lifespan Blocking Non-blocking.

### The ASGI callable signature
    
    
    async def app(scope, receive, send):  
        ...

Where:

Parameter Meaning `scope` Immutable connection info (method, headers, path, etc.) `receive()` Async function: read events from server (request body, disconnect) `send()` Async function: send events to server (response start/body)

* * *

### 3\. Step-by-Step: Build a Raw ASGI App

Create a file:
    
    
    raw_asgi_app.py

Paste this:
    
    
    # raw_asgi_app.py  
      
    async def app(scope, receive, send):  
        print("=== SCOPE RECEIVED ===")  
        print(scope)  
        # Only handle HTTP requests  
        if scope["type"] != "http":  
            return  
        # Wait for request event (headers/body)  
        event = await receive()  
        print("=== REQUEST EVENT ===")  
        print(event)  
        body = b"Hello from raw ASGI!"  
        # Send HTTP start  
        await send({  
            "type": "http.response.start",  
            "status": 200,  
            "headers": [(b"content-type", b"text/plain")]  
        })  
        # Send response body  
        await send({  
            "type": "http.response.body",  
            "body": body,  
        })

* * *

### 4\. Run the App With Uvicorn

Even though we didn’t build routing or server logic, Uvicorn **can execute any ASGI app** :
    
    
    uvicorn raw_asgi_app:app --host 127.0.0.1 --port 8000

Test it:
    
    
    curl "http://127.0.0.1:8000/hello?name=kfir"

Watch your terminal print:

  * The **scope**
  * The **request event**
  * The ASGI lifecycle



This is the moment where ASGI becomes real.

* * *

### 5\. Understanding the ASGI Scope

Example (shortened):
    
    
    {  
        "type": "http",  
        "method": "GET",  
        "path": "/hello",  
        "query_string": b"name=kfir",  
        "headers": [  
            (b"host", b"127.0.0.1:8000"),  
            (b"user-agent", b"curl/8.0"),  
            (b"accept", b"*/*")  
        ],  
        "client": ("127.0.0.1", 53921),  
        "server": ("127.0.0.1", 8000)  
    }

This is exactly the same information Starlette uses to build a `Request` object.

* * *

### 6\. Understanding `receive()` Events

For HTTP requests:
    
    
    {  
        "type": "http.request",  
        "body": b"",  
        "more_body": False  
    }

For clients disconnecting:
    
    
    {"type": "http.disconnect"}

* * *

### 7\. Understanding `send()` Events

### Start the HTTP response:
    
    
    {  
        "type": "http.response.start",  
        "status": 200,  
        "headers": [...],  
    }

### Send body:
    
    
    {  
        "type": "http.response.body",  
        "body": b"...",  
    }

If streaming:
    
    
    {"body": chunk, "more_body": True}

* * *

### 8\. Diagram — The ASGI Lifecycle
    
    
    Client (curl)  
       │  
       ▼  
    Raw HTTP bytes  
       │  
       ▼  
    Uvicorn (parsing, connection, events)  
       │  
       ▼  
    ASGI App (your app)  
       │        ▲  
     send()     │ receive()  
       ▼        │  
    Response events  
       │  
       ▼  
    Uvicorn → TCP → Client

* * *

### 9\. Compare This With WSGI

WSGI:
    
    
    def app(environ, start_response):  
        ...

ASGI:
    
    
    async def app(scope, receive, send):  
        ...

WSGI gives you:

  * sync
  * blocking
  * no streaming
  * no WebSockets



ASGI gives you:

  * async
  * streaming
  * background tasks
  * WebSockets
  * HTTP/2 support



* * *

### 10\. Quick Exercises

### 1\. Return JSON manually
    
    
    body = b'{"msg":"hello"}'  
    headers = [(b"content-type", b"application/json")]

### 2\. Parse query params manually
    
    
    qs = scope["query_string"].decode()

### 3\. Print content length
    
    
    for name, value in scope["headers"]:  
        if name == b"content-length":  
            print("Content-Length:", value.decode())

### 4\. Respond in two chunks (streaming)
    
    
    await send({"type": "http.response.body", "body": b"Hello ", "more_body": True})  
    await send({"type": "http.response.body", "body": b"Kfir!"})

* * *

#### Wrapping Up: Why You Just Built ASGI by Hand

By writing an ASGI app without FastAPI, Starlette, or any framework, you’ve crossed an important threshold: you now understand what **actually happens before any modern Python web framework can do its job**.

You saw how:

  * A TCP connection becomes **raw HTTP bytes.**
  * Those bytes become an **ASGI scope + events.**
  * Your Python code responds using **send()/receive() .**
  * The entire request/response lifecycle is just **structured events** , not magic.



This understanding is what separates a **FastAPI user** from a **FastAPI engineer**.

Every routing decision, middleware execution, background task, and WebSocket message ultimately reduces to the exact pattern you implemented manually.

If you can build this tiny ASGI app from scratch, you can understand, debug, and optimize any modern Python web stack- from Uvicorn workers to Starlette internals all the way up to FastAPI dependencies.

Congratulations. You’re officially “under the hood.”

* * *

### Official References (Highly Recommended)

These are the _authoritative sources_ behind everything in this blog:

### ASGI

  * Official ASGI Spec  
<https://asgi.readthedocs.io/en/latest/specs/main.html>



### HTTP / Request Lifecycle

  * HTTP Semantics — RFC 9110  
<https://httpwg.org/specs/rfc9110.html>
  * HTTP/1.1 Message Syntax — RFC 9112  
<https://httpwg.org/specs/rfc9112.html>



### Uvicorn

  * Official Uvicorn Docs  
<https://www.uvicorn.org>



### Starlette (ASGI Toolkit)

  * Official Starlette Docs  
<https://www.starlette.io>



### FastAPI

  * Official FastAPI Docs  
<https://fastapi.tiangolo.com>



### WSGI / CGI History

  * WSGI PEP 333  
<https://peps.python.org/pep-0333>
  * WSGI PEP 3333  
<https://peps.python.org/pep-3333>
  * Common Gateway Interface  
<https://www.rfc-editor.org/rfc/rfc3875>



By [Kfir Gisman](https://medium.com/@Kfir-G) on [December 8, 2025](https://medium.com/p/c02de4a20dad).

[Canonical link](https://medium.com/@Kfir-G/from-passive-fastapi-developer-to-real-fastapi-engineer-part-2-c02de4a20dad)

Exported from [Medium](https://medium.com) on December 20, 2025.
