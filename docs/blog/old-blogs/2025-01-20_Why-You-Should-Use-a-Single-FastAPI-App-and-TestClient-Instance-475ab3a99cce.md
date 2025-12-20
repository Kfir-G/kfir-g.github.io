---
title: Why You Should Use A Single Fastapi App And Testclient Instance
published: true
date: 2025-01-20 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/475ab3a99cce
---

# Why You Should Use a Single FastAPI App and TestClient Instance

Learn why reusing a single FastAPI app and TestClient instance can simplify your testing setup and improve efficiency 

* * *

### Why You Should Use a Single FastAPI App and TestClient Instance

![](https://cdn-images-1.medium.com/max/1200/1*S82r3-z_rpD7SyMAxo43yg.jpeg)Photo by Shawon Dutta: <https://www.pexels.com/photo/beach-bluesky-beautiful-sky-blue-sea-7759874/>

When working with FastAPI, especially in larger projects, using **one instance of your FastAPI app** and **one instance of**`**TestClient**` across your entire project is critical for ensuring consistency, performance, and reliability. Let’s dive into why this is important and explore hands-on examples.

* * *

### 1\. Consistency Across the Application

Creating multiple instances of your FastAPI app can lead to inconsistencies. Each app instance has its own state, middleware, and dependency management. If you share stateful data, like in-memory storage or database connections, having multiple instances can cause unexpected behavior.

### 2\. Improved Performance

Each `TestClient` creates its own HTTP connection and initializes dependencies. Using one `TestClient` reduces overhead and makes tests faster.

### 3\. Avoid Initialization Issues

FastAPI apps often initialize resources like database connections or background tasks during startup. Multiple instances can result in duplicate initializations or conflicts.

* * *

### Hands-On Code Example

#### Correct: One App Instance, One TestClient
    
    
    from fastapi import FastAPI, Depends  
    from fastapi.testclient import TestClient  
      
    # Create a single FastAPI app instance  
    app = FastAPI()  
      
    # Simple in-memory database  
    database = {"items": []}  
      
    # Dependency  
    def get_database():  
        return database  
      
    @app.post("/items/")  
    def create_item(item: str, db=Depends(get_database)):  
        db["items"].append(item)  
        return {"message": f"Item '{item}' added."}  
      
    @app.get("/items/")  
    def list_items(db=Depends(get_database)):  
        return {"items": db["items"]}  
      
    # Create a single TestClient instance  
    client = TestClient(app)  
      
    # Tests  
    def test_create_item():  
        response = client.post("/items/", json={"item": "foo"})  
        assert response.status_code == 200  
        assert response.json() == {"message": "Item 'foo' added."}  
      
    def test_list_items():  
        response = client.get("/items/")  
        assert response.status_code == 200  
        assert response.json() == {"items": ["foo"]}

#### Incorrect: Multiple Instances Can Cause Issues
    
    
    # Incorrect: Multiple app instances  
    app1 = FastAPI()  
    app2 = FastAPI()  
      
    # Incorrect: Multiple TestClient instances  
    client1 = TestClient(app1)  
    client2 = TestClient(app2)  
      
    # Issue: State changes in client1 won't reflect in client2

### Common Issues with Multiple Instances

  1. **State Inconsistency** : Shared state (like `database`) will behave independently in different app instances.
  2. **Multiple Dependency Initializations** : Dependencies like database connections may be initialized multiple times, leading to resource exhaustion.
  3. **Startup/Shutdown Event Overlap** : Multiple app instances trigger these events independently, causing redundant or conflicting behavior.



* * *

### Best Practices

#### Structure Your Project for Reuse

Create your app in a dedicated file (e.g., `app.py`) and import it where needed.
    
    
    # app.py  
    from fastapi import FastAPI  
      
    app = FastAPI()  
    # Add routes here
    
    
    # main.py  
    from fastapi.testclient import TestClient  
    from app import app  
      
    client = TestClient(app)

#### Use `pytest` Fixtures for Shared Instances

Fixtures in `pytest` help manage shared resources like the `TestClient`:
    
    
    import pytest  
    from fastapi.testclient import TestClient  
    from app import app  
      
    @pytest.fixture(scope="module")  
    def test_client():  
        client = TestClient(app)  
        yield client  # Ensure cleanup  
      
    def test_example(test_client):  
        response = test_client.get("/items/")  
        assert response.status_code == 200

### Relevant Documentation

  * [Starlette TestClient](https://www.starlette.io/testclient/)
  * [Testing with FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)
  * [pytest Fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html)



By following these guidelines, you ensure your FastAPI project is consistent, efficient, and maintainable.

### Thank you for being a part of the community

 _Before you go:_

  * Be sure to **clap** and **follow** the writer ️👏**️️**
  * Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
  * [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
  * [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
  * [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
  * For more content, visit [**plainenglish.io**](https://plainenglish.io/) \+ [**stackademic.com**](https://stackademic.com/)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [January 20, 2025](https://medium.com/p/475ab3a99cce).

[Canonical link](https://medium.com/@Kfir-G/why-you-should-use-a-single-fastapi-app-and-testclient-instance-475ab3a99cce)

Exported from [Medium](https://medium.com) on December 20, 2025.
