---
title: The Three Generations In Python S Garbage Collector
published: true
date: 2025-03-17 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/13a76e895e72
---

# The Three Generations in Python’s Garbage Collector

How Python’s GC Classifies Objects Into Generations- Objects are grouped by age to make garbage collection more efficient. 

* * *

### The Three Generations in Python’s Garbage Collector

![](https://cdn-images-1.medium.com/max/800/1*VmNaWLUj6L43Mdw6I2dCYQ.jpeg)Photo by Willian Santos: <https://www.pexels.com/photo/relaxed-beach-scene-with-vintage-camera-statue-28467843/>

Python’s **garbage collector (GC) follows a generational model** to optimize memory management. Instead of scanning all objects every time, it organizes them into **three generations** based on their lifespan. This approach is built on the **generational hypothesis** , which assumes:

  1. **Most objects are short-lived** and should be collected frequently.
  2. **Long-lived objects are rarely garbage** and should be checked less often.



By structuring garbage collection this way, Python reduces overhead while efficiently reclaiming memory. This guide explores how these **generations work, when GC runs, and how to fine-tune it** for better performance.

* * *

### 1️⃣ The Three Generations of Python’s GC

Every object created in Python **starts in Generation 0** and moves to older generations if it survives multiple GC runs.

### Generation 0 (Young Objects)- Collected Often

  * This is the **first place** where new objects are allocated.
  * These objects are **collected frequently** because most of them are short-lived.
  * Example of short-lived objects:


    
    
    def create_temp_object():       
      data = {"name": "Temp"}  # Created inside a function       
      return data              # Often discarded quickly

  * Once an object **survives a GC cycle** , it moves to **Generation 1**.



* * *

### Generation 1 (Medium-lived Objects) — Collected Less Often

  * Objects that **survived at least one collection in Gen 0** move here.
  * The assumption is that these objects are more likely to be used for a longer time.
  * Gen 1 is collected **less frequently** than Gen 0.
  * Example:


    
    
    cached_data = {"user": "John"}  # Used multiple times but not forever

  * If an object **continues to survive** , it moves to **Generation 2**.



* * *

### Generation 2 (Long-lived Objects)- Rarely Collected

  * Objects that **survive multiple GC cycles** end up in Gen 2.
  * These objects are assumed to be **important and necessary** for the program.
  * Gen 2 is **collected the least frequently** because it contains objects that have already survived several rounds.
  * Example:


    
    
    class DatabaseConnection:       
      def __init__(self):           
        self.connection = "Connected"    
      
    db = DatabaseConnection()  # Global object, used throughout the program

  * **Global variables, class instances, and modules** often stay in **Gen 2**.



* * *

### 2️⃣ How Do Generations Interact?

Each generation has a **threshold** that determines when GC runs. You can check these values using:
    
    
    import gc  
    print(gc.get_threshold())  # (700, 10, 10) by default

This means:

  1. **Gen 0 triggers collection after 700 new objects** are created.
  2. **Gen 1 runs every 10 Gen 0 collections.**
  3. **Gen 2 runs every 10 Gen 1 collections.**



### Example Workflow:

  * Your program creates **700 new objects** → GC runs for **Gen 0**.
  * If an object survives **one Gen 0 collection** , it moves to **Gen 1**.
  * After **10 Gen 0 collections** , **Gen 1** is checked.
  * After **10 Gen 1 collections** , **Gen 2** is checked.



* * *

### 3️⃣ Controlling Garbage Collection

### Checking How Many Objects Are in Each Generation

You can see the number of objects currently in each generation using:
    
    
    print(gc.get_count())  # Example output: (450, 25, 5)

This means:

  * **450 objects in Gen 0**
  * **25 objects in Gen 1**
  * **5 objects in Gen 2**



* * *

### Manually Running Garbage Collection

If you want to **force a collection** , you can use:
    
    
    gc.collect()  # Collects all generations  
    gc.collect(0)  # Collects only Generation 0  
    gc.collect(1)  # Collects Generation 0 and 1  
    gc.collect(2)  # Collects all three generations

* * *

### Adjusting Collection Frequency

If your program creates many objects **quickly** , you might want to **tune GC thresholds** :
    
    
    gc.set_threshold(1000, 20, 20)  # Increase thresholds to reduce GC runs

### When Should You Change These?

  * If your program **creates and destroys objects rapidly** (e.g., web servers, data processing).
  * If you notice **performance slowdowns due to frequent GC runs**.



* * *

### 4️⃣ Real-World Example: Optimizing Memory in FastAPI

### Problem: Too Many Objects in Memory

A FastAPI app **creates too many short-lived request objects** , increasing Gen 0 collections.
    
    
    from fastapi import FastAPI  
      
    app = FastAPI()  
      
    @app.get("/")  
    async def home():  
        data = {"message": "Hello"}  # This gets created and discarded every request  
        return data

**Issue:** Every request creates a new dictionary, filling up Gen 0 quickly.

* * *

### Solution: Reuse Objects When Possible
    
    
    cached_response = {"message": "Hello"}  # Store as a long-lived object  
      
    @app.get("/")  
    async def home():  
        return cached_response  # Uses existing object instead of creating new ones

**Benefit:** This **reduces GC pressure** by preventing unnecessary object creation.

* * *

### 5️⃣ Key Takeaways

  * **Python’s GC has three generations (0, 1, 2).**
  * **Gen 0 is collected most frequently, Gen 2 the least.**
  * **Objects move between generations based on survival.**
  * **GC runs based on threshold values (**`**gc.get_threshold()**`**).**
  * **You can manually trigger (**`**gc.collect()**`**) or tune (**`**gc.set_threshold()**`**) the GC.**
  * **Optimizing object reuse helps reduce GC pressure.**



### Further Reading

  * [Python Garbage Collection Docs](https://docs.python.org/3/library/gc.html)



### Thank you for being a part of the community

 _Before you go:_

  * Be sure to **clap** and **follow** the writer ️👏**️️**
  * Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0) | [**Differ**](https://differ.blog/inplainenglish)
  * [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
  * [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
  * [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
  * For more content, visit [**plainenglish.io**](https://plainenglish.io/) \+ [**stackademic.com**](https://stackademic.com/)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [March 17, 2025](https://medium.com/p/13a76e895e72).

[Canonical link](https://medium.com/@Kfir-G/the-three-generations-in-pythons-garbage-collector-13a76e895e72)

Exported from [Medium](https://medium.com) on December 20, 2025.
