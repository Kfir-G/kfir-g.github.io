---
title: What Really Happens When You Type Google Com In Your Browser
published: true
date: 2025-03-30 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/c33e8c2e6eed
---

# What Really Happens When You Type google.com in Your Browser?

From URL to Webpage: A Deep Dive into DNS, TCP, TLS, and HTTP 

* * *

### What Really Happens When You Type `google.com` in Your Browser?

![](https://cdn-images-1.medium.com/max/800/1*kE9_VS2SZlUWDnhVnMIfHw.jpeg)Photo by Thiago Matos : <https://www.pexels.com/photo/colorful-ferris-wheel-against-cloudy-sky-30342870/>

Every time you type `google.com` into your browser’s address bar and press Enter, a complex sequence of events unfolds behind the scenes. This post will break down each step in detail with Python examples and references to official documentation.

* * *

### 1\. Domain Name Resolution (DNS Lookup)

Before your browser can connect to Google’s servers, it needs the IP address corresponding to `google.com`. This process is called **DNS resolution**.

### How it Works:

  1. The browser first checks its **DNS cache** to see if the domain has been resolved recently.
  2. If not found, it queries the OS’s DNS resolver.
  3. If still unresolved, the OS sends a request to a **recursive DNS server** (provided by your ISP or a third-party like Google’s `8.8.8.8`).
  4. The recursive DNS server queries **root name servers** → **TLD name servers** (`.com`) → **Authoritative name servers** for `google.com`.
  5. The authoritative name server provides the IP address (e.g., `142.250.184.14`).
  6. The response is cached for future queries.



🔗 **Official Docs:**

  * [IETF RFC 1034 — DNS Concepts](https://datatracker.ietf.org/doc/html/rfc1034)
  * [Google Public DNS](https://developers.google.com/speed/public-dns)



### Python Code for DNS Resolution:
    
    
    import socket  
      
    domain = "google.com"  
    ip = socket.gethostbyname(domain)  
    print(f"Resolved {domain} to {ip}")

* * *

### 2\. Establishing a TCP Connection

Once the IP is known, the browser establishes a **TCP connection** using the **three-way handshake** :

  1. **SYN** : The client sends a TCP packet with the SYN flag set.
  2. **SYN-ACK** : The server responds with a packet containing SYN and ACK flags.
  3. **ACK** : The client acknowledges and the connection is established.



🔗 **Official Docs:**

  * [IETF RFC 793 — TCP Protocol](https://datatracker.ietf.org/doc/html/rfc793)
  * [Linux TCP/IP Networking Guide](https://www.tldp.org/LDP/nag2/index.html)



### Python Code for TCP Connection:
    
    
    import ssl, socket  
      
    context = ssl.create_default_context()  
    sock = socket.create_connection((ip, 443))  # HTTPS uses port 443  
    secure_sock = context.wrap_socket(sock, server_hostname=domain)  
    print("TCP connection established with Google")

* * *

### 3\. TLS Handshake & Secure Connection

Since Google uses HTTPS, an additional **TLS handshake** takes place:

  1. **Client Hello** : The browser sends supported encryption protocols.
  2. **Server Hello** : The server responds with a chosen encryption algorithm.
  3. **Certificate Exchange** : The server provides an SSL certificate for verification.
  4. **Key Exchange** : Both parties establish an encrypted communication channel.



🔗 **Official Docs:**

  * [IETF RFC 8446 — TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446)
  * [Mozilla TLS Overview](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security)



### Python Code for TLS Handshake:
    
    
    print(secure_sock.version())  # Print the TLS version used

* * *

### 4\. Sending an HTTP Request

Once connected, the browser sends an HTTP request. A standard request for Google’s homepage:
    
    
    GET / HTTP/1.1  
    Host: google.com  
    Connection: close  
    User-Agent: Mozilla/5.0 (compatible; Chrome)

🔗 **Official Docs:**

  * [IETF RFC 7230 — HTTP/1.1 Message Syntax](https://datatracker.ietf.org/doc/html/rfc7230)
  * [Mozilla HTTP Request Structure](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages)



### Python Code for Sending an HTTP Request:
    
    
    request = "GET / HTTP/1.1\r\nHost: google.com\r\nConnection: close\r\n\r\n"  
    secure_sock.sendall(request.encode())

* * *

### 5\. Receiving and Processing the Response

Google’s server responds with an HTTP response, typically a **301 Redirect** :
    
    
    HTTP/1.1 301 Moved Permanently  
    Location: https://www.google.com/

This instructs the browser to retry the request at `[https://www.google.com/](https://www.google.com/.)`[.](https://www.google.com/.)

🔗 **Official Docs:**

  * [IETF RFC 9110 — HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)
  * [Google HTTP Status Codes](https://developers.google.com/web/fundamentals/performance/http2#http-status-codes)



### Python Code for Receiving Response:
    
    
    response = b""  
    while True:  
        data = secure_sock.recv(4096)  
        if not data:  
            break  
        response += data  
    print(response.decode(errors='ignore'))

* * *

### 6\. Rendering the Webpage

Once the browser receives the response, it:

  1. Parses the HTML.
  2. Fetches additional resources (CSS, JavaScript, images).
  3. Executes scripts.
  4. Renders the page on the screen.



🔗 **Official Docs:**

  * [MDN Browser Rendering](https://developer.mozilla.org/en-US/docs/Web/Performance/How_browsers_work)
  * [Google Chrome Rendering Guide](https://developer.chrome.com/blog/inside-browser-part1/)



* * *

### 7\. Handling Subsequent Requests (Cookies, Caching, CDN)

  * **Cookies:** The server might set authentication cookies.
  * **Caching:** The browser stores assets for faster loading in future requests.
  * **CDN Requests:** Additional requests might be sent to Google’s CDN for assets.



🔗 **Official Docs:**

  * [RFC 6265 — HTTP Cookies](https://datatracker.ietf.org/doc/html/rfc6265)
  * [Google CDN Optimization](https://developers.google.com/speed/public-dns/docs/caching)



* * *

### Conclusion

When you type `google.com` and press Enter, a series of sophisticated network processes occur, including DNS resolution, TCP/TLS handshakes, HTTP requests, and webpage rendering. Each step plays a critical role in delivering web pages securely and efficiently.

### Want to Try It Yourself?

Run the Python snippets above to see the process in action!

By [Kfir Gisman](https://medium.com/@Kfir-G) on [March 30, 2025](https://medium.com/p/c33e8c2e6eed).

[Canonical link](https://medium.com/@Kfir-G/what-really-happens-when-you-type-google-com-in-your-browser-c33e8c2e6eed)
