---
title: Solving Logs Woes  A Dive Into Singleton Design Pattern
published: true
date: 2024-04-15 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/1f77e70bd498
---

# Solving Logs Woes: A Dive into Singleton Design Pattern

The article explores solving logging issues in Python by leveraging the Singleton Design Pattern, ensuring centralized logging. 

* * *

### **Solving Logs Woes: A Small Dive into Singleton Design Pattern**

![](https://cdn-images-1.medium.com/max/800/1*SYcs9K2pd-mDEOYWgYEUxA.jpeg) Credit: [Saydung89](https://pixabay.com/users/saydung89-18713596/)

Recently, I’ve been working on a new feature for a Python software project. To make sure it’s solid, I thought it’d be a good idea to add logs using the “[logging](https://docs.python.org/3/library/logging.html)” Python package. It’s been really helpful because I can see what’s happening at every step of my program right in the console. It’s made tracking down bugs a lot easier.

Initially, I thought incorporating _logging_ would be straightforward — simply import the library and start logs. However, I hit a roadblock when I couldn’t get it to write logs from files. Despite trying various solutions like checking the logging configuration file and creating new instances or modules, none of them worked. Then, a colleague suggested a solution I had overlooked: the _Singleton Design Pattern_. This approach turned out to be the key to solving my problem. Now, I’ll explain what it is and how to implement it, so you’ll feel confident using it in the future if similar issues arise.

### What Is Singleton Design Approach

The Singleton design pattern is a simple yet powerful concept often used in software development. Imagine you have a class (let’s call it Logger) and you want only one instance of this class to exist throughout your program’s execution.

In simpler terms, think of the Singleton as a guardian that ensures there’s only one instance of a particular class. It’s like having a single key to a treasure chest — no matter how many times you ask for the key, you’ll always get the same one.

#### Here’s a breakdown:

  * **One and Only One** : The Singleton ensures that there’s only one instance of a class. It’s like having a single instance of your favorite game running — you can’t open two instances of the same game simultaneously.
  * **Global Access:** Once the Singleton is created, it provides a global point of access to that instance. Just like a lighthouse guiding ships in the night, the Singleton guides your program to the same instance every time you need it.
  * **Common Use Cases:** Singletons are handy for resources that should be shared across the entire application, such as a database connection, a logger, or a configuration manager.
  * **Implementation:** Typically, Singletons are implemented using a static method (like `getInstance()`) that either creates a new instance if none exists or returns the existing instance if it does.



**Here’s a simple example in Python:**
    
    
     class Singleton:  
     _instance = None  
      
     @staticmethod  
     def getInstance():  
         if Singleton._instance is None:  
             Singleton._instance = Singleton()  
         return Singleton._instance  
      
    # Usage:  
    singleton_instance1 = Singleton.getInstance()  
    singleton_instance2 = Singleton.getInstance()  
      
    print(singleton_instance1 == singleton_instance2)  # Output: True

  * **Benefits:** Singletons help conserve resources by ensuring that only one instance of a class exists. They also simplify global state management by providing a centralized point of access.
  * **Caveats:** While Singletons are useful, they can sometimes be overused, leading to tight coupling and global state-related issues. It’s essential to use them judiciously and consider other alternatives when appropriate.



### How Singleton Design Resolved My Issue

Now, let’s delve into how I utilized the Singleton pattern to address my issue in the code:
    
    
    class Logger:  
     _instance = None  
      
     def __new__(cls):  
         if cls._instance is None:  
             cls._instance = super().__new__(cls)  
             cls._instance.setup_logger()  
         return cls._instance  
      
     def setup_logger(self):  
         # logging configuration here

  1. `_instance`**Attribute:** This attribute keeps track of the single instance of the `Logger` class.
  2. `__new__`**Method:** Python’s special `__new__` method is harnessed here to manage object instantiation. If `_instance` is `None`, indicating no instance exists, a new one is created via `super().__new__(cls)`and `setup_logger()` is invoked to configure the logger. Subsequent calls to `__new__` will return the same instance stored in `_instance`.
  3. `setup_logger`**Method:** Responsible for configuring the logger. It’s executed only once during the creation of the singleton instance.



#### How It Functions:

  * Whenever you create an instance of `Logger (logger_root = Logger())`, `__new__` kicks in.
  * If `_instance` is `None`, implying no instance exists, a fresh one is created and stored in `_instance`.
  * Subsequent calls to `Logger()` return the same instance stored in `_instance`, ensuring the singular existence of the `Logger` class across your program.



#### Pros and Considerations:

  * **Universal Access:** Access the logger instance globally via `logger_root`.
  * **Thread Safety:** This implementation doesn’t address thread safety. For multithreaded applications, consider synchronizing access to the singleton instance.
  * **Lazy Initialization:** The logger instance is lazily instantiated, meaning it’s created only when first requested. This conserves resources if the logger isn’t always in use.



#### Double Checking

I won’t delve too deeply into the _double-checking pattern_ that I integrated into my `__new__` function. Essentially, I added double-checking within the `__new__` method by first checking if the `_instance` is `None`, then acquiring a lock to ensure thread safety, and finally rechecking if `_instance` is still `None` before creating a new instance. If you’re interested in learning more about it, you can check out this link: ( <https://www.geeksforgeeks.org/java-program-to-demonstrate-the-double-check-locking-for-singleton-class/> )

### Conclusion

By integrating the Singleton pattern, you ensure a streamlined, centralized logging mechanism within your project.

* * *

### References

[**Singleton Design Pattern**  
 _In this article, we will talk about what is Singleton Design Pattern and when we need it. Further, we will implement…_ medium.com](https://medium.com/@emredalc/singleton-design-pattern-ce7e2f153aa0 "https://medium.com/@emredalc/singleton-design-pattern-ce7e2f153aa0")[](https://medium.com/@emredalc/singleton-design-pattern-ce7e2f153aa0)

[**Introduction to Design Patterns & Understanding Singleton Design Pattern**  
 _If you are a software engineer, understanding design patterns and working with those will make you an exceptional…_ medium.com](https://medium.com/geekculture/introduction-to-design-patterns-understanding-singleton-design-pattern-5a4d49960444 "https://medium.com/geekculture/introduction-to-design-patterns-understanding-singleton-design-pattern-5a4d49960444")[](https://medium.com/geekculture/introduction-to-design-patterns-understanding-singleton-design-pattern-5a4d49960444)

[**Singleton**  
 _Singleton is a creational design pattern that lets you ensure that a class has only one instance, while providing a…_ refactoring.guru](https://refactoring.guru/design-patterns/singleton "https://refactoring.guru/design-patterns/singleton")[](https://refactoring.guru/design-patterns/singleton)

[**Singleton Pattern in Python - A Complete Guide - GeeksforGeeks**  
 _A Computer Science portal for geeks. It contains well written, well thought and well explained computer science and…_ www.geeksforgeeks.org](https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/ "https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/")[](https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/)

[**logging - Logging facility for Python**  
 _Source code: Lib/logging/__init__.py Important: This page contains the API reference information. For tutorial…_ docs.python.org](https://docs.python.org/3/library/logging.html "https://docs.python.org/3/library/logging.html")[](https://docs.python.org/3/library/logging.html)

### In Plain English 🚀

 _Thank you for being a part of the_[** _In Plain English_**](https://plainenglish.io) _community! Before you go:_

  * Be sure to **clap** and **follow** the writer ️👏**️️**
  * Follow us: [**X**](https://twitter.com/inPlainEngHQ)**|**[**LinkedIn**](https://www.linkedin.com/company/inplainenglish/)**|**[**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw)**|**[**Discord**](https://discord.gg/in-plain-english-709094664682340443)**|**[**Newsletter**](https://newsletter.plainenglish.io/)
  * Visit our other platforms: [**Stackademic**](https://stackademic.com/)**|**[**CoFeed**](https://cofeed.app/)**|**[**Venture**](https://venturemagazine.net/)**|**[**Cubed**](https://blog.cubed.run)
  * More content at [**PlainEnglish.io**](https://plainenglish.io)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [April 15, 2024](https://medium.com/p/1f77e70bd498).

[Canonical link](https://medium.com/@Kfir-G/solving-logs-woes-a-dive-into-singleton-design-pattern-1f77e70bd498)

Exported from [Medium](https://medium.com) on December 20, 2025.
