---
title: Why I Use Curl Instead Of Postman  Learning Http By Feel
published: true
date: 2025-11-10 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/2fd88ef90fb7
---

# Why I Use curl Instead of Postman: Learning HTTP by Feel

Sometimes you don’t need another GUI. You need to touch the protocol. While everyone opens Postman tabs, I open my terminal and type: 

* * *

### Why I Use `curl` Instead of Postman: Learning HTTP by Feel

![](https://cdn-images-1.medium.com/max/800/1*1_8JXRQ6X6-4_JRU2rbibw.jpeg)Photo by Kelly : <https://www.pexels.com/photo/motor-bike-running-close-up-photography-2519374/>

* * *

Sometimes you don’t need another GUI. You need to touch the protocol. While everyone opens Postman tabs, I open my terminal and type:
    
    
    curl -X POST http://127.0.0.1:8000/api/shorten \  
      -H "Content-Type: application/json" \  
      -d '{"url": "https://example.com"}'

That’s it- raw, direct, and honest. No buttons, no noise. Just HTTP, right under your fingertips.

* * *

### Learning Through the Fingertips

Typing the request yourself makes every part of HTTP visible.

  * `-X POST` chooses the verb with intent
  * `-H` sets the headers precisely
  * `-d` sends the data explicitly



And when you hit enter, you see exactly what the server gives back:
    
    
    {"short_url": "http://localhost:8000/000001"}

Every `curl` command teaches you the rhythm of request and response- the web’s real heartbeat.

* * *

### Seeing the Protocol, Not the UI

When you use `curl -v`, the terminal becomes your microscope:
    
    
    curl -v http://127.0.0.1:8000/api/000001

You see every move:
    
    
    > GET /api/000001 HTTP/1.1  
    > Host: 127.0.0.1:8000  
    > User-Agent: curl/8.7.1  
    > Accept: */*  
    < HTTP/1.1 307 Temporary Redirect  
    < location: https://example.com/

The protocol becomes transparent. You understand what’s happening, not just that something happened.

* * *

### Discovering More

The beauty of `curl` is in its depth.  
You don’t have to memorize- you explore.
    
    
    curl --help  
    curl --help all | less

Each flag opens a new door like:

  * `-I` fetch headers only
  * `-L` follow redirects automatically
  * `-o` save output to a file
  * `-w "%{http_code}"` show only the response code
  * `-s` silent mode (no progress bar)
  * `-S` show errors even when silent
  * `-k` ignore SSL certificate checks
  * `-x http://proxy:8080` use a proxy



The official docs are an endless rabbit hole of discovery: <https://curl.se/docs/manpage.html>

If you don’t want to leave the terminal, you can explore everything from the CLI itself. Here are a few ways to learn `curl` directly through your shell:
    
    
    # See all common options with short descriptions  
    curl --help  
      
    # See every possible flag and advanced usage  
    curl --help all | less  
      
    # Get a manual-style explanation (same as the website docs)  
    man curl  
      
    # Search inside the manual for a specific flag  
    man curl | grep timeout  
      
    # Quick reminder for a specific option  
    curl --help | grep -i header

This is the beauty of `curl`: the docs live right where you work. You don’t have to Google anything- the knowledge is built into the tool.

* * *

### How curl Fits in Everyday Dev Life

`curl` is not just for testing APIs. It’s a daily development companion.

### 1\. Health checks
    
    
    curl -fsSL http://localhost:8000/health || echo "Service down"

### 2\. Quick response code check
    
    
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000

### 3\. Debugging with headers
    
    
    curl -v -X GET http://localhost:8000/api/items  
    curl -i http://localhost:8000/api/status

### 4\. Testing authentication
    
    
    curl -u admin:password http://localhost:8000/api/users

### 5\. Sending JSON data
    
    
    curl -X POST http://localhost:8000/api/shorten \  
      -H "Content-Type: application/json" \  
      -d '{"url": "https://example.com"}'

### 6\. Simulating different HTTP verbs
    
    
    curl -X PUT http://localhost:8000/api/items/1 -d '{"name": "updated"}'  
    curl -X DELETE http://localhost:8000/api/items/1

### 7\. Working inside Docker containers
    
    
    docker exec -it tinyurl-app-fastapi-1 curl http://redis:6379

### 8\. Testing redirects and caching
    
    
    curl -L http://localhost:8000/short/123  
    curl -I http://localhost:8000/static/style.css

### 9\. Monitoring endpoints continuously
    
    
    watch -n 2 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health'

### 10\. Downloading and uploading files
    
    
    curl -O https://example.com/file.zip  
    curl -T myfile.txt ftp://ftp.example.com/ --user user:password

* * *

### The Terminal Teaches Clarity

When you write requests in `curl`, you’re not hiding behind tools. You’re speaking to your server directly.

Each request is a sentence. Each flag is a verb. Each header is a whisper between client and server.

`curl` slows you down just enough to see what’s really happening. And once you see it, you never unsee it.

* * *

### Feel the Protocol

`curl` is how you think in HTTP. It’s how you debug, learn, and build with precision. It’s that small command you reach for when nothing else feels right.

So the next time you open your terminal, type `curl` and listen. The protocol has been trying to talk to you all along.

By [Kfir Gisman](https://medium.com/@Kfir-G) on [November 10, 2025](https://medium.com/p/2fd88ef90fb7).

[Canonical link](https://medium.com/@Kfir-G/why-i-use-curl-instead-of-postman-learning-http-by-feel-2fd88ef90fb7)
