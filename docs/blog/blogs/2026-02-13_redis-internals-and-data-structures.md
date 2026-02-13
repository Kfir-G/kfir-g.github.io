---
title: Redis Internals & Data Structures - The In-Memory Backbone
published: true
date: 2026-02-13 00:00:00 UTC 
tags: redis,backend,architecture,performance,distributed-systems,data-structures
canonical_url: https://kfir-g.dev/blog/blogs/2026-02-13_redis-internals-and-data-structures.md
---

# Redis Internals & Data Structures

Redis is often called a "Swiss Army Knife" for developers. It’s not just a cache; it’s an **in-memory data structure server** that trades disk durability for extreme speed and predictable performance.

Understanding how Redis manages its "backbone"—the event loop and its specialized C-based structures—is the difference between a system that scales and one that suffers from "hot-key" bottlenecks.

This guide covers:

* The Single-Threaded Event Loop (I/O Multiplexing)
* Core Data Structures (Strings, Hashes, Lists, Sets, ZSets)
* Internal Encodings (SDS, ZipList, SkipList)
* Memory Management & Eviction
* Persistence (RDB vs. AOF)
* Redis Cluster & Sharding

## 1. The Architecture: Why it's so fast

At its core, Redis is **Single-Threaded** for command execution. This sounds like a bottleneck, but it’s its greatest strength. By avoiding context switching and expensive locks (mutexes), Redis can process 100k+ requests per second on a single core.

### The Event Loop (I/O Multiplexing)

Redis uses `epoll` (Linux) or `kqueue` (BSD/macOS) to monitor thousands of concurrent connections. It waits for data to be "ready" on a socket, processes the command, and moves to the next.

## 2. The Data Structure "Backbone"

Redis doesn't store data as "blind blobs." It understands the type of data it holds, allowing for atomic operations like "increment this counter" or "pop from this list."

### A. Strings (SDS)

The most basic type. Internally, Redis uses **Simple Dynamic Strings (SDS)** instead of standard C strings.

* **O(1) Length:** C strings require scanning for `\0`; SDS stores length.
* **Binary Safe:** Can store images or serialized Protobuf objects.

### B. Lists (Quicklists)

Implemented as a **Quicklist** (a hybrid of Linked Lists and ZipLists).

* **LPOP/RPUSH:** O(1) performance.
* **Use Case:** Task queues (like Celery's Redis broker).

### C. Hashes (Dicts)

Perfect for representing objects (e.g., a User profile).

* **Efficiency:** Small hashes are compressed into **ZipLists** to save RAM.
* **O(1) Access:** Direct access to fields without fetching the whole object.

### D. Sorted Sets (SkipLists)

The "Magic" of Redis. Every element has a **Score**.

* **SkipList Internals:** A probabilistic structure that allows O(log N) search/insert, similar to a balanced tree but easier to implement for range queries.
* **Use Case:** Leaderboards and Rate Limiters.

## 3. Internal Encodings & Optimization

Redis is obsessed with memory. It will change the *internal representation* of your data based on its size.

| Data Type | Small Dataset Encoding | Large Dataset Encoding |
| --- | --- | --- |
| **String** | Integer (if numeric) | SDS (Simple Dynamic String) |
| **Hash** | ZipList (Memory efficient) | Hash Table (O(1) lookup) |
| **List** | Quicklist | Quicklist |
| **Set** | IntSet (if only integers) | Hash Table |
| **ZSet** | ZipList | SkipList + Hash Table |

## 4. Persistence: RDB vs. AOF

Because Redis is in-memory, a crash = data loss. To fix this, it offers two backbones for durability:

1. **RDB (Snapshotting):** A compact, point-in-time binary snapshot.
* *Pros:* Extremely fast restarts.
* *Cons:* You might lose data between snapshots (e.g., last 5 mins).


2. **AOF (Append Only File):** Logs every write operation.
* *Pros:* Durable (fsync every second).
* *Cons:* Larger file size; slower recovery.

**The Modern Pro-Tip:** Most production setups use **Hybrid Persistence** (AOF + RDB preamble).

## 5. Scaling: Redis Cluster & Sharding

When one server isn't enough, Redis scales horizontally via **Clustering**.

* **Hash Slots:** The keyspace is divided into **16,384 slots**.
* **CRC16(key) % 16384:** This formula determines which node owns your data.
* **Gossip Protocol:** Nodes talk to each other to detect failures and handle failovers automatically via **Redis Sentinel**.

## 6. Real-World Logic (Python/FastAPI)

```python
import redis

# Connecting to the backbone
r = redis.Redis(host='localhost', port=6379, db=0)

# Atomic Counter (Thread-safe by design)
r.incr('page_views')

# Using a Hash for a User Profile
r.hset('user:100', mapping={
    'username': 'kfir_dev',
    'tier': 'premium',
    'status': 'active'
})

# Range query on a Sorted Set (Leaderboard)
top_users = r.zrevrange('leaderboard', 0, 9, withscores=True)
```

## Summary Checklist

* [x] **Strings** for basic keys and counters.
* [x] **Hashes** for structured objects.
* [x] **Lists** for FIFO/LIFO queues.
* [x] **Sorted Sets** for ranking and time-series logic.
* [x] **TTLs** (Time To Live) to prevent memory exhaustion.

## References

* Redis Official Data Structures: [https://redis.io/technology/data-structures/](https://redis.io/technology/data-structures/)
* Redis Internals (Deep Dive): [https://redis.io/docs/latest/develop/data-types/](https://redis.io/docs/latest/develop/data-types/)
