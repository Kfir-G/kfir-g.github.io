---
title: This Small Python Script Improved Understanding Of Low Level Programming
published: true
date: 2024-11-26 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/077a2a066273
---

# This Small Python Script Improved Understanding of Low-Level Programming

A Python script that simplifies concurrency while deepening understanding of low-level concepts like CPU-bound and I/O-bound tasks 

* * *

### **This Small Python Script Improved Understanding of Low-Level Programming**

![](https://cdn-images-1.medium.com/max/1200/1*NGF9X8S3cjzJeO5QGKfJsQ.jpeg) Photo by Alexander Kovalev: <https://www.pexels.com/photo/man-sitting-on-grass-using-computer-2748445/>

Python is widely used for its simplicity and ease of use, but for many programmers, there comes a point when the language itself no longer presents new challenges. Once developers become familiar with common libraries and techniques, the process of solving problems becomes routine. However, there is always more to learn, especially when diving into advanced topics like concurrency and low-level programming concepts.

A popular resource for those looking to take their Python skills further is the “[Talk Python To Me](https://talkpython.fm/)” podcast, which covers a broad range of topics related to Python development. One such [course](https://training.talkpython.fm/courses/explore_async_python/async-in-python-with-threading-and-multiprocessing), “Parallel Programming in Python with async/await and threads,” presents key concepts for handling concurrency and optimizing code execution.

In traditional computer science education, topics like computer architecture, C programming, mutexes, semaphores, and pointers are often introduced. However, many developers never truly connect these concepts with real-world programming scenarios. The understanding of CPU cores, for example, often remains abstract, disconnected from daily development tasks.

One key lesson from the course is the use of the [unsync](https://pypi.org/project/unsync/) library, which simplifies concurrent and parallel programming by combining async, threading, and multiprocessing into a unified API. This library automatically optimizes tasks based on whether they are CPU-bound, I/O-bound, or asynchronous. By eliminating the complexities of thread initiation, joining, and closure, the unsync library makes concurrent programming in Python more accessible and efficient.

The following script provides a practical demonstration of these concepts:
    
    
    # source: https://github.com/talkpython/async-techniques-python-course/blob/master/src/09-built-on-asyncio/the_unsync/thesync.py  
      
    def main():  
        t0 = datetime.datetime.now()  
      
        tasks = [  
            compute_some(),  
            compute_some(),  
            compute_some(),  
            download_some(),  
            download_some(),  
            download_some_more(),  
            download_some_more(),  
            wait_some(),  
            wait_some(),  
            wait_some(),  
            wait_some(),  
        ]  
      
        [t.result() for t in tasks]  
      
        dt = datetime.datetime.now() - t0  
        print(f"Synchronous version done in {dt.total_seconds():,.2f} seconds.")  
      
    @unsync(cpu_bound=True)  
    def compute_some():  
        print("Computing...")  
        for _ in range(1, 10_000_000):  
            math.sqrt(25 ** 25 + .01)  
      
    @unsync()  
    async def download_some():  
        print("Downloading...")  
        url = 'https://talkpython.fm/episodes/show/174/coming-into-python-from-another-industry-part-2'  
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:  
            async with session.get(url) as resp:  
                resp.raise_for_status()  
      
                text = await resp.text()  
      
        print(f"Downloaded (more) {len(text):,} characters.")  
      
    @unsync()  
    def download_some_more():  
        print("Downloading more ...")  
        url = 'https://pythonbytes.fm/episodes/show/92/will-your-python-be-compiled'  
        resp = requests.get(url)  
        resp.raise_for_status()  
      
        text = resp.text  
      
        print(f"Downloaded {len(text):,} characters.")  
      
    @unsync()  
    async def wait_some():  
        print("Waiting...")  
        for _ in range(1, 1000):  
            await asyncio.sleep(.001)

The script demonstrates various types of tasks and how they can be executed concurrently to improve performance and efficiency:

  * The `compute_some` function simulates heavy computations by calculating large numbers. It demonstrates how multithreaded processing can leverage multiple CPU cores to perform parallel calculations, reducing processing time and improving efficiency. In real-world applications, this approach is used for tasks like numerical simulations, data analysis, and computationally intensive operations.
  * The `download_some` function asynchronously fetches data from external sources (such as APIs or websites). It runs within an asyncio event loop, allowing for non-blocking I/O operations. This makes it ideal for handling multiple simultaneous I/O tasks without freezing the program, which is useful for applications that need to interact with multiple data sources at the same time, such as scraping data or handling concurrent API requests.
  * The `download_some_more` function demonstrates the use of synchronous HTTP requests. Though synchronous, it runs in a separate thread to prevent blocking the main thread. This approach is useful in simpler or legacy systems where non-blocking operations are not necessary but concurrency is still desired.
  * The `wait_some` function simulates an asynchronous task that introduces non-blocking pauses, allowing other tasks to continue running while waiting. This is particularly useful in scenarios where the program needs to wait for external events, timers, or user input without freezing other operations.



By utilizing concurrent programming, the script shows how multiple tasks can be performed simultaneously, speeding up processing time and allowing for more efficient use of resources.

* * *

In programming, memory (RAM) and processing power (CPU) are essential components that influence performance. RAM enables fast access to active data, allowing the smooth execution of multiple tasks, while the CPU handles the execution of instructions and computations. In real-world scenarios, sufficient memory ensures that large datasets or multiple operations can be processed at once, while a powerful CPU enables faster calculations and more responsive applications.

Understanding the relationship between memory, CPU, and concurrency has a significant impact on how developers approach optimization and task execution. By leveraging multi-core CPUs and efficient memory management, developers can create more responsive, high-performance applications that handle complex, data-intensive tasks with ease.

By [Kfir Gisman](https://medium.com/@Kfir-G) on [November 26, 2024](https://medium.com/p/077a2a066273).

[Canonical link](https://medium.com/@Kfir-G/this-small-python-script-improved-understanding-of-low-level-programming-077a2a066273)
