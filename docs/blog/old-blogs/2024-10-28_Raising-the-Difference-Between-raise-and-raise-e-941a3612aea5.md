---
title: Raising The Difference Between Raise And Raise E
published: true
date: 2024-10-28 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/941a3612aea5
---

# Raising the Difference Between raise and raise e

Explains how raise preserves the original traceback for better debugging, while raise e resets it, potentially obscuring the error’s origin 

* * *

### Raising the Difference Between raise and raise e

When handling exceptions in Python, it’s common to encounter scenarios where we need to re-raise an error. There are two primary ways to do this: `raise` and `raise e`. While they may seem similar at first glance, these two forms handle tracebacks differently, impacting how errors are logged and, ultimately, how debugging plays out. In this post, we'll break down the distinction between `raise` and `raise e` and discuss when to use each for clearer, more maintainable error handling.

![](https://cdn-images-1.medium.com/max/800/0*WbJH5HemLA7pI-Wi.jpg)

* * *

### The Basics of Exception Handling

Before diving into the difference, let’s recap how exception handling works in Python. When an error occurs within a `try` block, the code jumps to the `except` block, where we can handle the error gracefully or re-raise it for further handling. Sometimes, it’s useful to catch an error, do something (like logging it), and then re-raise the exception to be handled by another part of the program.
    
    
    try:  
        result = 1 / 0  # Division by zero raises a ZeroDivisionError  
    except ZeroDivisionError as e:  
        print("Caught an error!")  
        raise  # Re-raises the original exception

In this case, the `raise` statement re-raises the original `ZeroDivisionError`, allowing the error to propagate up to higher-level error handlers.

* * *

### `raise` vs. `raise e`

Here’s the critical difference:

  * `**raise**`: Re-raises the caught exception while preserving the original traceback.
  * `**raise e**`: Re-raises the caught exception but **resets** the traceback to start from the line where `raise e` is called.



The distinction may seem minor, but it can significantly impact how tracebacks are displayed and how easy they are to interpret.

#### Example Code

Let’s illustrate this difference with a Python script:
    
    
    import traceback  
      
    def raise_exception_with_raise():  
        try:  
            result = 1 / 0  # This will cause a ZeroDivisionError  
        except ZeroDivisionError as e:  
            print("Caught an error, re-raising with 'raise'...")  
            raise  # Re-raises the original exception with its original traceback  
    def raise_exception_with_raise_e():  
        try:  
            result = 1 / 0  # This will cause a ZeroDivisionError  
        except ZeroDivisionError as e:  
            print("Caught an error, re-raising with 'raise e'...")  
            raise e  # Raises the exception with a new traceback  
    print("======= Using 'raise': =======")  
    try:  
        raise_exception_with_raise()  
    except ZeroDivisionError as e:  
        print("Traceback using 'raise':")  
        traceback.print_exc()  # Prints the original traceback  
    print("\n======= Using 'raise e': =======")  
    try:  
        raise_exception_with_raise_e()  
    except ZeroDivisionError as e:  
        print("Traceback using 'raise e':")  
        traceback.print_exc()  # Prints the new traceback

In this example, both `raise_exception_with_raise` and `raise_exception_with_raise_e` attempt to divide by zero, catching the `ZeroDivisionError` in their `except` blocks. Let’s look at what happens with each approach.

* * *

### Output Analysis

#### Using `raise`:
    
    
    ======= Using 'raise': =======  
    Caught an error, re-raising with 'raise'...  
    Traceback using 'raise':  
    Traceback (most recent call last):  
      File "example.py", line 19, in <module>  
        raise_exception_with_raise()  
      File "example.py", line 5, in raise_exception_with_raise  
        result = 1 / 0  # This will cause a ZeroDivisionError  
    ZeroDivisionError: division by zero

In this case, `raise` keeps the traceback simple and direct. It starts at the line where the original exception occurred (line 5 in `raise_exception_with_raise`) and goes up to where it was ultimately handled in the main program block. This full traceback preserves the original call stack, which makes tracking down the error straightforward.

#### Using `raise e`:
    
    
    ======= Using 'raise e': =======  
    Caught an error, re-raising with 'raise e'...  
    Traceback using 'raise e':  
    Traceback (most recent call last):  
      File "example.py", line 26, in <module>  
        raise_exception_with_raise_e()  
      File "example.py", line 15, in raise_exception_with_raise_e  
        raise e  # Raises the exception with a new traceback  
      File "example.py", line 12, in raise_exception_with_raise_e  
        result = 1 / 0  # This will cause a ZeroDivisionError  
    ZeroDivisionError: division by zero

Here, `raise e` shows an extra layer in the traceback, starting with the line `raise e` was called on (line 15 in `raise_exception_with_raise_e`). This resets the traceback’s starting point to the `raise e` statement, potentially obscuring the original error location.

### When to Use `raise` vs. `raise e`

**1\. Use**`**raise**`**for Simplicity and Clarity**

In most cases, `raise` is preferable because it retains the original traceback, making it easy to see exactly where the error occurred. This is particularly helpful in larger applications where an error may need to propagate up several layers before it’s handled.

**2\. Use**`**raise e**`**Sparingly**

There are rare cases where `raise e` might be useful, such as when you need to highlight a new context for an error. However, this approach can make debugging more challenging, as the original context is partially obscured by the new traceback.

* * *

### Conclusion

While both `raise` and `raise e` re-raise exceptions, they handle tracebacks differently. The direct `raise` statement is usually the best choice for preserving clarity in debugging, as it keeps the traceback as close to the original error as possible. In contrast, `raise e` resets the traceback to the current line, which can be helpful in specific contexts but generally makes the error’s origin harder to identify. Knowing when and how to use each one can make your error handling cleaner, more understandable, and, ultimately, more effective.

* * *

### References

  * [Python Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html#errors-and-exceptions)
  * [Python Exception Handling: Patterns and Best Practices by Jerry Ng](https://jerrynsh.com/python-exception-handling-patterns-and-best-practices/)



### Stackademic 🎓

Thank you for reading until the end. Before you go:

  * Please consider **clapping** and **following** the writer! 👏
  * Follow us [**X**](https://twitter.com/stackademichq) | [**LinkedIn**](https://www.linkedin.com/company/stackademic) | [**YouTube**](https://www.youtube.com/c/stackademic) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
  * [**Create a free AI-powered blog on Differ.**](https://differ.blog/)
  * More content at [**Stackademic.com**](https://stackademic.com/)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [October 28, 2024](https://medium.com/p/941a3612aea5).

[Canonical link](https://medium.com/@Kfir-G/raising-the-difference-between-raise-and-raise-e-941a3612aea5)
