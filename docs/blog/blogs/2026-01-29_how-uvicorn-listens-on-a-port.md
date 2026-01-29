---
title: How Uvicorn Listens on an Open Port – From SYN Queue to FastAPI
published: true
date: 2026-01-29 00:00:00 UTC
tags: python,fastapi,uvicorn,asgi,linux,networking,backend
canonical_url: https://kfir-g.dev/blog/blogs/2026-01-29_how-uvicorn-listens-on-a-port
---

# How Uvicorn Listens on an Open Port  

### From SYN Queue to FastAPI

For a backend engineer, understanding how Uvicorn listens on an open port is not an implementation detail - it’s a reliability skill.

When a FastAPI service struggles under load, the problem is often not async, not Python, and not your endpoint logic. It’s the TCP accept path. Long before your application sees a request, the Linux kernel, socket queues, and the event loop decide whether that connection even exists.

This post breaks down how Uvicorn binds to a port, what happens during the TCP handshake, and why SYN queues and accept queues directly affect latency, dropped connections, and system stability in production.

## The High-Level Flow

At a high level, this is what happens:

```text
Client → TCP Handshake → Kernel Queues → accept() → Uvicorn → ASGI → FastAPI
```

FastAPI only enters **very late** in this process.

## Step 1: Binding and Listening

When you start Uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Internally, Uvicorn:

1. Creates a socket
2. Binds it to an IP and port
3. Calls `listen(backlog)`

This is a **kernel-level operation**.

```text
socket()
bind()
listen(backlog)
```

From this point on, the **kernel owns incoming connections**, not Uvicorn.

## Step 2: TCP Handshake (Where Queues Begin)

A TCP connection requires a **three-way handshake**:

```text
Client → SYN
Server → SYN-ACK
Client → ACK
```

Linux uses **two queues** during this process.

## SYN Queue (Half-Open Connections)

The **SYN queue** stores connections that:

* Sent `SYN`
* Have not completed the handshake yet

Characteristics:

* Half-open connections
* Vulnerable to SYN floods
* Controlled by kernel TCP settings

If this queue fills:

* New SYN packets are dropped
* Clients see timeouts
* Your app is never notified

## Accept Queue (Fully Established Connections)

Once the handshake completes, the connection moves to the **accept queue**.

This queue holds:

* Fully established TCP connections
* Waiting for the application to call `accept()`

This queue **is what `listen(backlog)` actually controls**.

If the accept queue fills:

* Handshakes may complete
* But connections are dropped or reset
* Clients see connection failures even though the server is “up”

## Step 3: `accept()` – Where Uvicorn Enters

Uvicorn does **not** handle TCP itself.

It relies on:

* `asyncio`
* The OS socket API

Internally, the event loop repeatedly does:

```text
accept() → return socket → hand off to protocol handler
```

Only **now** does Uvicorn:

* Wrap the socket
* Parse HTTP
* Create an ASGI scope

If the event loop is slow or blocked:

* Accept queue fills
* Latency spikes
* Connections fail before FastAPI runs

## Step 4: Event Loop and Concurrency

Uvicorn uses an **async event loop** to:

* Accept new connections
* Read from sockets
* Schedule ASGI tasks

Important implications:

* `async` does **not** mean infinite parallelism
* Accepting connections still takes CPU time
* Slow handlers indirectly slow `accept()`

This is why CPU-bound work inside async apps is dangerous.

## Common Failure Modes Under Load

| Symptom                              | Root Cause                      |
| ------------------------------------ | ------------------------------- |
| Connection timeouts                  | SYN or accept queue overflow    |
| Works locally, fails in prod         | Different kernel backlog limits |
| High latency before request handling | Event loop overloaded           |
| Random connection resets             | Accept queue saturation         |

None of these are FastAPI bugs.

---

## Uvicorn Networking Cheat Sheet

This section is intentionally dense.
It’s meant as a **reference**, not a tutorial.

```bash
TCP FLOW (Server Side)

Client
  |
  |  SYN
  v
+------------------+
|   SYN Queue      |  (half-open)
|  - SYN received  |
|  - waiting ACK   |
+------------------+
        |
        | ACK
        v
+------------------+
|  Accept Queue    |  (fully open)
|  - handshake done|
|  - waiting accept()
+------------------+
        |
        | accept()
        v
+------------------+
|  Uvicorn Socket  |
|  - asyncio loop |
|  - protocol     |
+------------------+
        |
        v
+------------------+
|  ASGI App       |
|  - middleware   |
|  - FastAPI      |
+------------------+
```

Key facts:

* `listen(backlog)` limits the **accept queue**
* SYN queue is controlled by kernel TCP parameters
* Async does not bypass kernel limits
* If `accept()` is slow, FastAPI never sees traffic

---

## Why This Matters for FastAPI Engineers

FastAPI encourages async thinking - **but the kernel still gates traffic**.

You can write:

* Perfect async code
* Non-blocking endpoints
* Scalable middleware

And still fail under load if:

* Backlog is too small
* Event loop is saturated
* Kernel limits are ignored

Understanding this changes how you:

* Debug production incidents
* Tune deployments
* Design load tests

---

## Closing Thought

Async frameworks don’t replace the kernel.
They sit on top of it.

If your app never receives a request, the bug is often **below Python**, not inside it.
Once you understand the SYN queue and accept queue, Uvicorn stops being “magic” - and production behavior starts making sense.

---

## References & Official Documentation

### Linux Networking

* `listen(2)`
  [https://man7.org/linux/man-pages/man2/listen.2.html](https://man7.org/linux/man-pages/man2/listen.2.html)

* `accept(2)`
  [https://man7.org/linux/man-pages/man2/accept.2.html](https://man7.org/linux/man-pages/man2/accept.2.html)

* Linux TCP settings
  [https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html](https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html)

* [SYN packet handling in the wild](https://blog.cloudflare.com/syn-packet-handling-in-the-wild/) - recommended!

### Python & Asyncio

* Asyncio Event Loop
  [https://docs.python.org/3/library/asyncio-eventloop.html](https://docs.python.org/3/library/asyncio-eventloop.html)

* `loop.sock_accept()`
  [https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.sock_accept](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.sock_accept)

### Uvicorn

* Uvicorn Configuration
  [https://www.uvicorn.org/settings/](https://www.uvicorn.org/settings/)

### ASGI

* ASGI Specification
  [https://asgi.readthedocs.io/en/latest/](https://asgi.readthedocs.io/en/latest/)

### FastAPI
* FastAPI Concepts
 [https://fastapi.tiangolo.com/deployment/concepts/](https://fastapi.tiangolo.com/deployment/concepts/)