---
title: Unleash The Power Of  Fastapi  Async Vs Blocking I O
published: true
date: 2024-09-23 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/7ec80edb7320
---

# Unleash the Power of FastAPI: Async vs Blocking I/O

Discover how to optimize FastAPI by using async functions for concurrent request handling 

* * *

### Unleash the Power of FastAPI: Async vs Blocking I/O

![](https://cdn-images-1.medium.com/max/800/1*nET639qEQVDGFtet1KBZVQ.jpeg)

Are you ready to maximize your FastAPI application’s performance? In this article, we’ll explore how FastAPI handles concurrent requests and how you can optimize your app by leveraging async functions over traditional blocking I/O. By the end, you’ll have a deeper understanding of when to use `async def` versus `def` and how to make your FastAPI APIs run blazingly fast!

#### Why Does Concurrency Matter?

Handling multiple requests concurrently can dramatically improve the responsiveness of your web applications. A web server that can handle multiple requests at once is crucial in modern applications, especially when serving numerous users simultaneously.

FastAPI, powered by Python’s `asyncio` library, makes concurrent request handling a breeze with its support for asynchronous programming. The question is: how do we compare blocking and non-blocking I/O, and how does that impact our FastAPI applications?

#### Code Example

To demonstrate how FastAPI handles concurrent requests and to understand the performance differences between `async def` and `def`, we’ll create a simple example where we compare blocking I/O with non-blocking I/O using `time.sleep` and `asyncio.sleep`. Visit the Code example [**here**](https://gist.github.com/Kfir-G/c04659467de03dfe90b32356a4a11ea5).

#### Blocking I/O in FastAPI

Let’s first take a look at how traditional blocking I/O works in FastAPI. For this, we’ll use Python’s built-in `time.sleep()` to simulate an I/O-bound task that blocks the thread for 5 seconds:
    
    
    @app.get("/blocking")  
    def blocking_io():  
     time.sleep(5)  
     return {"message": "Blocking I/O completed"}

This blocks the entire application’s thread, meaning no other requests can be processed while this one is running. This is highly inefficient if your application needs to handle many simultaneous users.

#### Non-Blocking I/O: FastAPI’s Strength

With FastAPI, you can easily switch to non-blocking I/O using `async def` functions and `asyncio.sleep()`:
    
    
    @app.get("/non-blocking")  
    async def non_blocking_io():  
     await asyncio.sleep(5)  
     return {"message": "Non-blocking I/O completed"}

In this case, while one request is waiting, other requests can be processed because `asyncio.sleep()` doesn’t block the server’s main thread. This improves performance and allows FastAPI to handle more requests concurrently.

#### When to Use `def` vs async def in FastAPI

\- Use `def` for CPU-bound tasks where the operation can benefit from parallel execution using a thread pool.

\- Use `async def` for I/O-bound tasks like waiting on a database, API calls, or file I/O, where non-blocking behavior is essential to maximize performance.

#### Concurrency in Action

FastAPI excels in handling concurrent requests. You can simulate concurrent execution using `asyncio.gather()`:
    
    
    @app.get("/compare")  
    async def compare():  
     await asyncio.gather(non_blocking_io(), non_blocking_io())  
     return {"message": "Both async operations completed concurrently"}

Here, two asynchronous functions are executed concurrently, allowing your application to handle multiple tasks at the same time.

#### Handling Multiple Requests Concurrently

The real power of async becomes evident when you need to handle many requests concurrently. With FastAPI, it’s easy to spin up multiple non-blocking tasks:
    
    
    @app.get("/benchmark")  
    async def benchmark():  
     tasks = [non_blocking_io() for _ in range(10)]  
     await asyncio.gather(*tasks)  
     return {"message": "Handled 10 concurrent requests!"}

This approach scales well, enabling your application to serve more users without being held back by blocking I/O operations.

### Final Thoughts

FastAPI, with its native support for asynchronous programming, empowers you to build high-performance applications. By understanding the differences between blocking and non-blocking I/O, and when to use `async def` vs `def`, you can optimize your API’s performance to handle concurrent requests efficiently.

Stay tuned for more FastAPI deep dives, and happy coding!

* * *

### References

1\. [FastAPI Official Documentation](https://fastapi.tiangolo.com/)

2\. [Python’s asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

3\. [Threading in Python](https://docs.python.org/3/library/threading.html)

4\. [Concurrency in Python: Understanding Async and Threading](https://realpython.com/python-concurrency/)

5\. [FastAPI Performance Benchmark](https://fastapi.tiangolo.com/async/)

### In Plain English 🚀

 _Thank you for being a part of the_[** _In Plain English_**](https://plainenglish.io) _community! Before you go:_

  * Be sure to **clap** and **follow** the writer ️👏**️️**
  * Follow us: [**X**](https://twitter.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/)
  * Visit our other platforms: [**CoFeed**](https://cofeed.app/) | [**Differ**](https://differ.blog/)
  * More content at [**PlainEnglish.io**](https://plainenglish.io)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [September 23, 2024](https://medium.com/p/7ec80edb7320).

[Canonical link](https://medium.com/@Kfir-G/unleash-the-power-of-fastapi-async-vs-blocking-i-o-7ec80edb7320)

Exported from [Medium](https://medium.com) on December 20, 2025.
