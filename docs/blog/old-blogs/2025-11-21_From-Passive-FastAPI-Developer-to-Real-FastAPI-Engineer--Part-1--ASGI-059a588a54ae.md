---
title: From Passive Fastapi Developer To Real Fastapi Engineer  Part 1  Asgi
published: true
date: 2025-11-21 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/059a588a54ae
---

# From Passive FastAPI Developer to Real FastAPI Engineer- Part 1: ASGI

Understanding ASGI by Breaking Down an HTTP Request 

* * *

### From Passive FastAPI Developer to Real FastAPI Engineer- Part 1: ASGI

* * *

![](https://cdn-images-1.medium.com/max/800/1*0aGbK5MJNAkF0XKM0hV3zA.jpeg)Photo by Kaue Barbier: <https://www.pexels.com/photo/28182842/>

* * *

### Understanding ASGI by Breaking Down an HTTP Request

Modern Python web frameworks feel effortless- you write a function, return some JSON, and boom: a web app. But underneath that smooth layer lies a ton of complexity: raw bytes over TCP, state machines, protocols, concurrency, and error-prone details you never want to touch.

**ASGI exists to shield you from that pain.** Let’s break an HTTP request down and see how ASGI fits into the picture.

* * *

### What is ASGI?

**ASGI (Asynchronous Server Gateway Interface)** is a **Python specification** that defines how web servers communicate with asynchronous Python applications.

Official spec: <https://asgi.readthedocs.io/en/latest/>

You can think of it as the evolution of WSGI, designed for modern async apps, HTTP/2, and WebSockets.

* * *

### Why Do We Need ASGI?

Inside every web server, there are three conceptual layers:
    
    
    Transport  ->  Protocol  ->  Application Logic  
    TCP/SSL        HTTP/WS        Your FastAPI code

The problem:  
If every framework had to re-implement TCP handling, HTTP parsing, connection lifecycle, etc., we’d live in a world of endless duplicated code and subtle bugs.

**ASGI proposes a clean split into two Python components:**

  1. **Protocol Server** (e.g., Uvicorn, Hypercorn)


  * Handles raw network I/O
  * Transforms bytes into structured ASGI events



**2\. Application** (e.g., Starlette, FastAPI, custom ASGI apps)

  * Receives events like `http.request`
  * Returns events like `http.response.start` and `http.response.body`



This “bridge” is ASGI:
    
    
    Protocol Server  <---- ASGI ---->  Application

* * *

### A Quick Timeline of Request Interfaces

Year Spec Notes:

**1993** CGI Process-per-request. Ancient, slow.

**2003** WSGI (PEP 333) Standardized sync Python apps.

**2010** WSGI 1.0.1 (PEP 3333) Updated for Python 3.

**2016** ASGI Async, event-based design.

**2019** ASGI 3.0 Modern form used today.

* * *

### Why WSGI Wasn’t Enough

WSGI apps are **synchronous** and take exactly two parameters:
    
    
    def app(environ, start_response):  
        start_response("200 OK", [("Content-Type", "text/plain")])  
        return [b"hello"]

This works for HTTP/1.1 but fails for:

  * concurrency
  * streaming
  * long-lived connections
  * WebSockets



WSGI can’t represent async behavior or event-driven protocols.

* * *

### ASGI’s Core Idea

An ASGI application is **an async callable** :
    
    
    async def app(scope, receive, send):  
        ...

  * **scope** → Metadata about the connection (type, path, headers, etc.)
  * **receive()** → Wait for events from server (e.g., request body chunks)
  * **send()** → Emit events back (response start, response body, WebSocket messages)



This event system is the real power. It makes communication flexible and supports full-duplex protocols.

* * *

### A Minimal ASGI App (Raw)
    
    
    async def app(scope, receive, send):  
        assert scope["type"] == "http"  
      
    await send({  
            "type": "http.response.start",  
            "status": 200,  
            "headers": [(b"content-type", b"text/plain")],  
        })  
        await send({  
            "type": "http.response.body",  
            "body": b"Hello from raw ASGI!",  
        })

Run it with Uvicorn:
    
    
    uvicorn example:app

* * *

### HTTP Request Flow in WSGI vs ASGI

### WSGI Flow (Sync)
    
    
    Client  
      |  
    HTTP Request  
      |  
    WSGI Server parses bytes  
      |  
    (environ, start_response)  
      |  
    WSGI App  
      |  
    Iterables of bytes  
      |  
    WSGI Server → HTTP Response

No events. No async. No real-time messaging.

* * *

### ASGI Flow (Event-Based, Async)
    
    
    Client  
      |  
    Raw Bytes  
      |  
    Protocol Server (Uvicorn / Daphne)  
      |  
    ASGI Event: "http.request", "http.disconnect"  
      |  
    async app(scope, receive, send)  
      |  
    Your app emits events:  
      - "http.response.start"  
      - "http.response.body"  
      - "websocket.accept"  
      - "websocket.send"

This model is more general, flexible, and future-proof.

* * *

### Why ASGI Matters

### 1\. Concurrency

Async I/O = thousands of simultaneous connections.

### 2\. WebSockets Support

WSGI can’t do WebSockets.  
ASGI makes WebSockets just another protocol supported by events.

### 3\. Full-Duplex Communication

Send and receive independently- essential for:

  * WebSockets
  * HTTP streaming
  * Server-Sent Events
  * Background events



### 4\. Protocol Independence

ASGI officially supports:

  * **http**
  * **websocket**
  * **lifespan** (startup/shutdown events)



More protocols can be added without rewriting frameworks.

* * *

### A Tiny Diagram: ASGI in FastAPI
    
    
          ┌──────────────────┐  
          │   Your FastAPI   │  
          │      App         │  
          └────────┬─────────┘  
                   │  ASGI callable  
                   ▼  
            ASGI Interface  
                   ▲  
                   │ events  
          ┌────────┴─────────┐  
          │   Uvicorn Server │  
          │ (Protocol Layer) │  
          └──────────────────┘

You “inject” your application into the protocol server.  
The server handles all low-level details- your app just reacts to events.

* * *

### Final Summary

ASGI gives us:

  * async concurrency
  * flexible event-driven communication
  * WebSocket support
  * protocol independence
  * clean separation of logic vs transport
  * a standard interface for modern Python web servers



It’s the foundation that makes **Starlette** and **FastAPI** so fast and the reason you never have to manipulate raw HTTP bytes yourself.

* * *

### References:

  * The **ASGI official specification** at <https://asgi.readthedocs.io/en/latest/>
  * The **WSGI standard** via **PEP 333** at <https://peps.python.org/pep-0333/> and **PEP 3333** at <https://peps.python.org/pep-3333/>, the historical **CGI/1.1 RFC** at <https://www.rfc-editor.org/rfc/rfc3875>
  * The **Uvicorn ASGI server** documentation at <https://www.uvicorn.org/>
  * The **Starlette framework** documentation at <https://www.starlette.io/>
  * Tmhe **HTTP/1.1 protocol** definition at <https://www.rfc-editor.org/rfc/rfc7230>, and the **WebSocket protocol spec** at <https://www.rfc-editor.org/rfc/rfc6455>



By [Kfir Gisman](https://medium.com/@Kfir-G) on [November 21, 2025](https://medium.com/p/059a588a54ae).

[Canonical link](https://medium.com/@Kfir-G/from-passive-fastapi-developer-to-real-fastapi-engineer-part-1-asgi-059a588a54ae)
