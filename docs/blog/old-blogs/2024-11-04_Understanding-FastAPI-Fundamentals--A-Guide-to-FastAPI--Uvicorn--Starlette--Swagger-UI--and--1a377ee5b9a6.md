---
title: Understanding Fastapi Fundamentals  A Guide To Fastapi  Uvicorn  Starlette  Swagger Ui  And
published: true
date: 2024-11-04 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/1a377ee5b9a6
---

# Understanding FastAPI Fundamentals: A Guide to FastAPI, Uvicorn, Starlette, Swagger UI, and…

Explore FastAPI’s fundamentals, including Uvicorn, Starlette, Pydantic, and Swagger UI with these key resources for tutorials, docs, guide 

* * *

### Understanding FastAPI Fundamentals: A Guide to FastAPI, Uvicorn, Starlette, Swagger UI, and Pydantic

![](https://cdn-images-1.medium.com/max/800/1*gSV_7HBlIUR10uU2SAESvw.jpeg)Photo by Kevin Menajang: <https://www.pexels.com/photo/photo-from-concrete-structures-920024/>

FastAPI is a modern, high-performance web framework for building APIs with Python, allowing developers to create powerful and efficient applications with minimal effort. It’s designed with asynchronous programming in mind, making it extremely fast and able to handle multiple requests concurrently. Key components that power FastAPI include Uvicorn, Starlette, Swagger UI, and Pydantic. In this guide, we’ll explore each of these components and see how they come together in FastAPI, with code examples to demonstrate key concepts.

* * *

### 1\. The Core of FastAPI

FastAPI is built on two major foundations:

  * **Asynchronous Programming** : Leveraging Python’s `async` and `await`, FastAPI can handle many requests at the same time, making it efficient for applications that require concurrency.
  * **Type Annotations** : FastAPI uses Python’s type hints to validate and serialize request and response data automatically, which makes development faster and safer.



Let’s start with a simple FastAPI app to get an idea of its structure:
    
    
    # main.py  
      
    from fastapi import FastAPI  
      
    app = FastAPI()  
      
    @app.get("/")  
    async def read_root():  
        return {"Hello": "World"}

This is a basic FastAPI application with a single route (`/`) that returns a JSON response with `{"Hello": "World"}`.

To run this app, you’ll use **Uvicorn** , an ASGI server designed to serve asynchronous web applications.

* * *

### 2\. Uvicorn: The ASGI Server

Uvicorn is a lightning-fast ASGI server, optimized for handling asynchronous code. It’s essential for running FastAPI applications because it handles incoming HTTP requests and manages the lifecycle of these requests.

To run your FastAPI app with Uvicorn, use the following command:
    
    
    uvicorn main:app --reload

  * `main:app` specifies that Uvicorn should look for an `app` instance in the `main.py` file.
  * `--reload` enables hot-reloading during development, so the server reloads automatically whenever you save changes.



When you run this command, Uvicorn will start serving your FastAPI app, and you can access it at `[http://127.0.0.1:8000](http://127.0.0.1:8000.)`[.](http://127.0.0.1:8000.)

* * *

### 3\. Starlette: FastAPI’s Web Framework Foundation

FastAPI is built on top of **Starlette** , a lightweight ASGI framework that handles the core HTTP operations, including routing, middleware, and WebSockets support. Starlette provides the low-level tools that FastAPI uses to manage HTTP requests, making it a stable and performant foundation for building web applications.

FastAPI leverages Starlette’s routing system to define API endpoints. For example:
    
    
    @app.get("/items/{item_id}")  
    async def read_item(item_id: int):  
        return {"item_id": item_id}

In this example:

  * `@app.get("/items/{item_id}")` defines a route with a path parameter `item_id`.
  * FastAPI handles this path parameter type (`int` here) by integrating Starlette's routing system with its type checking and validation.



Starlette also allows you to add **middleware** for various operations, such as handling CORS (Cross-Origin Resource Sharing), request logging, or custom authentication:
    
    
    from starlette.middleware.cors import CORSMiddleware  
      
    app.add_middleware(  
        CORSMiddleware,  
        allow_origins=["*"],  
        allow_credentials=True,  
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

This flexibility in Starlette makes FastAPI highly configurable, allowing developers to easily add custom middlewares as needed.

* * *

### 4\. Swagger UI: Interactive API Documentation

FastAPI automatically generates interactive API documentation with **Swagger UI**. This documentation is available by default at `/docs` and allows developers to test endpoints directly from the browser.

To see this in action, start up your FastAPI app and visit `http://127.0.0.1:8000/docs`. You’ll see an interactive Swagger UI that lists all of your routes, their parameters, and the expected responses.

Another documentation interface, **ReDoc** , is also provided at `/redoc` by default, offering a more detailed view of API specifications.

* * *

### 5\. Pydantic: Data Validation and Serialization

One of the most powerful aspects of FastAPI is its use of **Pydantic** for data validation. Pydantic models allow you to define the structure of request and response data with strict type constraints and automatic validation.

Let’s add a Pydantic model to our example:
    
    
    from fastapi import FastAPI  
    from pydantic import BaseModel  
      
    app = FastAPI()  
      
    # Define a Pydantic model  
    class Item(BaseModel):  
        name: str  
        price: float  
        is_offer: bool = False  
      
    # Use the model in an endpoint  
    @app.put("/items/{item_id}")  
    async def update_item(item_id: int, item: Item):  
        return {"item_id": item_id, "item": item}

In this code:

  * The `Item` model inherits from `BaseModel` and defines three fields: `name`, `price`, and `is_offer`. These fields have specific data types and an optional default value for `is_offer`.
  * When you send a request to `/items/{item_id}` with JSON data, FastAPI uses Pydantic to validate the data against the `Item` model, automatically converting data types if possible.



Try sending a request like this using Swagger UI at `/docs`:
    
    
    {  
      "name": "Sample Item",  
      "price": 29.99  
    }

FastAPI will validate the data and automatically return any errors if the data doesn’t match the expected types. For instance, if `price` is given as a string (like `"twenty"`), FastAPI will respond with a detailed validation error.

* * *

### 6\. Putting It All Together

Let’s expand our app by adding more routes and combining everything we’ve learned so far:
    
    
    from fastapi import FastAPI, HTTPException  
    from pydantic import BaseModel  
    from starlette.middleware.cors import CORSMiddleware  
      
    app = FastAPI()  
      
    # Define a Pydantic model  
    class Item(BaseModel):  
        name: str  
        price: float  
        is_offer: bool = False  
      
    # Add CORS middleware  
    app.add_middleware(  
        CORSMiddleware,  
        allow_origins=["*"],  
        allow_credentials=True,  
        allow_methods=["*"],  
        allow_headers=["*"],  
    )  
    # Home route  
    @app.get("/")  
    async def read_root():  
        return {"Hello": "World"}  
      
    # Get an item by ID  
    @app.get("/items/{item_id}")  
    async def read_item(item_id: int, q: str = None):  
        if item_id == 0:  
            raise HTTPException(status_code=404, detail="Item not found")  
        return {"item_id": item_id, "q": q}  
      
    # Update an item  
    @app.put("/items/{item_id}")  
    async def update_item(item_id: int, item: Item):  
        return {"item_id": item_id, "item": item}

With this setup:

  * **Routing and Parameter Handling** : The `@app.get("/items/{item_id}")` endpoint demonstrates path parameters and query parameters (e.g., `q`).
  * **Exception Handling** : Using `HTTPException` for custom error responses (e.g., when an item is not found).
  * **CORS** : CORS middleware allows you to make requests from different domains, crucial for frontend-backend communication in web apps.



* * *

### Running the Application

To run this application, use Uvicorn:
    
    
    uvicorn main:app --reload

Navigate to `http://127.0.0.1:8000/docs` to see the interactive documentation, or use a tool like **cURL** or **Postman** to send requests to the different endpoints.

* * *

### Summary

FastAPI combines the performance benefits of asynchronous programming with the simplicity of Python type hints to create a framework that’s fast, easy to use, and suitable for production applications. By integrating Uvicorn, Starlette, Swagger UI, and Pydantic, FastAPI provides an incredibly streamlined approach to API development, making it a great choice for both rapid prototyping and production-grade applications.

With these core fundamentals in place, you’re now equipped to dive deeper into the world of FastAPI and build scalable, high-performance applications.

### Reference

  1. [FastAPI Documentation](https://fastapi.tiangolo.com/)
  2. [Uvicorn Documentation](https://www.uvicorn.org/)
  3. [Starlette Documentation](https://www.starlette.io/)
  4. [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
  5. [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)



### In Plain English 🚀

 _Thank you for being a part of the_[** _In Plain English_**](https://plainenglish.io/) _community! Before you go:_

  * Be sure to **clap** and **follow** the writer ️👏**️️**
  * Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
  * [**Create a free AI-powered blog on Differ.**](https://differ.blog/)
  * More content at [**PlainEnglish.io**](https://plainenglish.io/)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [November 4, 2024](https://medium.com/p/1a377ee5b9a6).

[Canonical link](https://medium.com/@Kfir-G/understanding-fastapi-fundamentals-a-guide-to-fastapi-uvicorn-starlette-swagger-ui-and-1a377ee5b9a6)

Exported from [Medium](https://medium.com) on December 20, 2025.
