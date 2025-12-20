---
title: Understanding Python Memory And Garbage Collection Through Hands On Experiments
published: true
date: 2025-01-06 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/86f25aa6b5d5
---

# Understanding Python Memory and Garbage Collection Through Hands-On Experiments

Dive into Python’s memory management with practical examples to understand reference counting, garbage collection, and efficient resource… 

* * *

### Understanding Python Memory and Garbage Collection Through Hands-On Experiments

![](https://cdn-images-1.medium.com/max/800/1*Dy4Yx22YWq5UItvauE0hPA.jpeg)Photo by badr mourafiq: <https://www.pexels.com/photo/creative-iphone-new-york-sony-9136482/>

Python is a high-level language that takes care of much of the memory management for you. However, understanding how it works under the hood can give you better insights into performance optimization and how to manage your resources efficiently. In this blog post, we’ll explore **Python’s memory management** and **garbage collection (GC)** with hands-on examples. We will focus on three core concepts:

  1. **Memory Allocation and Reference Counting**
  2. **Cyclic References**
  3. **Using**`**gc**`**to Manage Garbage Collection**



Let’s dive in with an experiment-driven approach using a small Python script that demonstrates these concepts in action.

* * *

### 1\. Memory Allocation and Reference Counting

Memory management in Python is primarily handled through **reference counting**. Every object in Python has a reference count that tracks how many references point to it. When the reference count drops to zero, the object is automatically deleted, and its memory is freed.

#### Example: Memory Allocation of Simple Objects
    
    
    import sys  
      
    # Create two variables pointing to the same integer object  
    x = 10  
    y = 10  # Both x and y point to the same memory location  
      
    # Memory address and reference count  
    print(f"Memory address of x (ID): {id(x)}")  
    print(f"Memory address of y (ID): {id(y)}")  
    print(f"Reference count for x: {sys.getrefcount(x)}")

**Key Points:**

  * Both `x` and `y` point to the same integer object (`10`), as integers are cached in Python.
  * The `id()` function shows that both variables share the same memory address.
  * `sys.getrefcount()` reveals that the reference count is greater than 1 because both `x` and `y` reference the same object.



After deleting one of the references (`del x`), the object is still alive because `y` still holds a reference to the object.
    
    
    del x  
      
    print(f"Reference count after deleting x: {sys.getrefcount(y)}")

#### Output:
    
    
    Memory address of x (ID): 140705611380560  
    Memory address of y (ID): 140705611380560  
    Reference count for x: 2  
    Reference count after deleting x: 1

As shown, the reference count of the object decreases after `x` is deleted, but the object is still not destroyed because `y` still holds a reference to it.

* * *

### 2\. Cyclic References and Garbage Collection

Sometimes, objects reference each other in a cycle (e.g., `A -> B -> A`), making it impossible for the reference count to reach zero. Python’s garbage collector handles these cases by detecting and cleaning up cyclic references.

#### Example: Creating a Cycle
    
    
    class Node:  
        def __init__(self, value):  
            self.value = value  
            self.next = None  
      
    # Create a cycle  
    node1 = Node(1)  
    node2 = Node(2)  
    node1.next = node2  
    node2.next = node1  # This creates a cyclic reference

Here, `node1` and `node2` reference each other, forming a cycle. Even after deleting both references, the objects are not collected because they still reference each other.
    
    
    del node1  
    del node2

### Triggering Garbage Collection

To break the cycle and reclaim memory, Python’s garbage collector (`gc`) can be manually triggered using `gc.collect()`.
    
    
    import gc  
      
    # Manually trigger garbage collection to clean up the cycle  
    gc.collect()

**Key Point:**

  * Python’s GC is able to detect and clean up cyclic references, ensuring that memory is freed even when reference counting can’t handle it.



### 3\. Using `gc` for Custom Garbage Collection

Python provides the `gc` module to interact with the garbage collector and control the cleanup process. We can check if garbage collection is enabled and even force a collection to clean up unreachable objects.
    
    
    import gc  
      
    print(f"Is Garbage Collection enabled? {gc.isenabled()}")  
    gc.collect()  # Force garbage collection  
    print(f"Garbage after collect: {gc.garbage}")

**Key Points:**

  * `gc.isenabled()` checks if garbage collection is enabled in the current Python session.
  * `gc.collect()` forces the garbage collection process, which can help clean up cyclic references or unreachable objects.



* * *

### 4\. Using `__del__` for Custom Cleanup

Python allows you to define custom cleanup code using the `__del__` method. This method is called when an object is about to be destroyed.

#### Example: Using `__del__`
    
    
    class MyObject:  
        def __init__(self, name):  
            self.name = name  
            print(f"MyObject {self.name} is created!")  
      
        def __del__(self):  
            print(f"MyObject {self.name} is being destroyed!")  
      
    obj1 = MyObject("Object 1")  
    obj2 = obj1  # obj2 is another reference to the same object  
      
    del obj1     # This will not delete the object, as obj2 still holds a reference  
    del obj2     # The object is now destroyed because both references are gone

In this example:

  * When `obj1` is deleted, the object is not destroyed because `obj2` still holds a reference to it.
  * When `obj2` is also deleted, the object’s `__del__` method is called, and the object is destroyed.



* * *

### Conclusion

Python’s memory management and garbage collection mechanisms are designed to handle most tasks automatically. By understanding **reference counting** and **cyclic references** , as well as how to manually trigger the garbage collector, you can ensure that your programs are more efficient and resource-friendly.

By experimenting with these examples, you gain hands-on experience in how Python manages memory, how cyclic references are handled, and how to clean up resources using the `gc` module.

Keep in mind:

  * **Reference Counting** : Keeps track of object references and deletes objects when they are no longer referenced.
  * **Garbage Collection** : Handles cyclic references that reference counting can’t clean up.
  * `**__del__**`**Method** : Allows for custom cleanup when objects are destroyed.



This knowledge helps you write more efficient and optimized Python code, particularly for resource-intensive applications.

* * *

### References

  * [Memory Management](https://docs.python.org/3/c-api/memory.html)
  * [Memory Management in Python](https://www.geeksforgeeks.org/memory-management-in-python/)
  * [gc — Garbage Collector interface](https://docs.python.org/3/library/gc.html)
  * [Garbage Collection in Python](https://www.geeksforgeeks.org/garbage-collection-python/)
  * [garbage collector](https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [January 6, 2025](https://medium.com/p/86f25aa6b5d5).

[Canonical link](https://medium.com/@Kfir-G/understanding-python-memory-and-garbage-collection-through-hands-on-experiments-86f25aa6b5d5)

Exported from [Medium](https://medium.com) on December 20, 2025.
