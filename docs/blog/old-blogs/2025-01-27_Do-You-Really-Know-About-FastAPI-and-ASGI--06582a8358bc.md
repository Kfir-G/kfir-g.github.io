---
title: Do You Really Know About Fastapi And Asgi
published: true
date: 2025-01-27 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/06582a8358bc
---

# Do You Really Know About FastAPI and ASGI?

Uvicorn is a high-performance ASGI server, and Starlette provides core tools for routing, middleware, and WebSockets. 

* * *

### Do You Really Know About FastAPI and ASGI?

* * *

#### Before Uvicorn and Starlette: How Did Synchronous Servers Work?

In traditional web development, servers like **WSGI (Web Server Gateway Interface)** were used to bridge web applications and HTTP servers. Frameworks like Flask and Django rely on WSGI servers (e.g., Gunicorn) to handle incoming requests. However, WSGI servers are synchronous by design, meaning:

  1. **Blocking I/O** : Each request blocks a worker thread until it completes, making it inefficient for handling high-concurrency scenarios like WebSockets or long-lived requests.
  2. **Scalability Challenges** : Scaling required adding more threads or processes, which increased resource consumption.



To address these limitations, the **ASGI (Asynchronous Server Gateway Interface)** standard was introduced. ASGI enables asynchronous, non-blocking communication, making it ideal for modern applications requiring WebSockets, HTTP/2, or other real-time capabilities.

* * *

#### The Arrival of Uvicorn and Starlette

FastAPI is built on top of **Uvicorn** and **Starlette** , each serving distinct but complementary roles. Let’s dive into their purposes and benefits.

### 1\. Uvicorn: The ASGI Server

Uvicorn is an **ASGI server** that runs FastAPI applications. It’s responsible for:

  * **Handling HTTP requests** : Uvicorn receives incoming HTTP/HTTPS requests and routes them to the application.
  * **Asynchronous I/O** : Designed to handle asynchronous calls efficiently, making it faster and more scalable than synchronous servers.
  * **Protocols Supported** :
  * HTTP/1.1, HTTP/2
  * WebSockets
  * **Production Readiness** : Uvicorn’s speed and lightweight design make it suitable for production environments.



**Benefits of Uvicorn**

  * High performance with event-driven architecture using **uvloop** (an optimized event loop for Python).
  * Native support for WebSockets and HTTP/2.
  * Minimal overhead for asynchronous applications.



**How to Use Uvicorn**

Here’s an example of running a FastAPI app with Uvicorn:
    
    
    uvicorn main:app --host 0.0.0.0 --port 8000

You can also run it programmatically:
    
    
    import uvicorn  
      
    if __name__ == "__main__":  
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

* * *

### 2\. Starlette: The ASGI Framework

Starlette is a lightweight **ASGI framework** that provides the core functionality for FastAPI. It offers tools and utilities for building web applications, including:

  * **Routing** : Map URLs to Python functions or classes.
  * **Middleware** : Add layers to process requests/responses (e.g., authentication, logging).
  * **Background Tasks** : Execute tasks outside the request/response cycle.
  * **WebSockets** : Enable real-time communication with clients.
  * **Testing Utilities** : Simplifies testing with an integrated testing client.



**Benefits of Starlette**

  * Modular and flexible design, making it a great foundation for frameworks like FastAPI.
  * Built-in support for async programming, allowing efficient resource utilization.
  * Comprehensive documentation and active community support.



**How to Use Starlette**

While you rarely interact directly with Starlette in FastAPI, you can use it independently to build minimal web applications. Here’s an example:
    
    
    from starlette.applications import Starlette  
    from starlette.responses import JSONResponse  
    from starlette.routing import Route  
      
    async def homepage(request):  
        return JSONResponse({"message": "Hello from Starlette!"})  
    app = Starlette(debug=True, routes=[  
        Route('/', homepage)  
    ])

Run this app with Uvicorn:
    
    
    uvicorn app:app --reload

* * *

### Differences Between Uvicorn and Starlette

Feature Uvicorn Starlette **Category** ASGI server ASGI framework **Purpose** Runs the application Provides core web framework features **Focus** Handles request/response lifecycle Routing, middleware, WebSockets, etc. **Interaction** Runs FastAPI apps Forms the foundation of FastAPI

### Putting It Together: Understanding Uvicorn and Starlette in FastAPI

FastAPI combines the best of Uvicorn and Starlette:

  * **Uvicorn** : Ensures high performance by handling the execution of the application.
  * **Starlette** : Powers FastAPI’s core functionalities, such as routing, middleware, and WebSocket support.



As a developer, understanding the roles of Uvicorn and Starlette helps you:

  * Optimize your application for performance (e.g., tuning Uvicorn settings for production).
  * Leverage Starlette’s utilities when building custom features.



By appreciating their distinct yet interconnected roles, you can make more informed decisions when building or deploying FastAPI applications.

### Thank you for being a part of the community

 _Before you go:_

  * Be sure to **clap** and **follow** the writer ️👏**️️**
  * Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
  * [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
  * [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
  * [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
  * For more content, visit [**plainenglish.io**](https://plainenglish.io/) \+ [**stackademic.com**](https://stackademic.com/)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [January 27, 2025](https://medium.com/p/06582a8358bc).

[Canonical link](https://medium.com/@Kfir-G/do-you-really-know-about-fastapi-and-asgi-06582a8358bc)

Exported from [Medium](https://medium.com) on December 20, 2025.
