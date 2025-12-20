---
title: Understanding Durability In Postgresql  A Deep Dive Into The  D  In Acid
published: true
date: 2025-07-07 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/af42ce13fb2b
---

# Understanding Durability in PostgreSQL -A Deep Dive into the “D” in ACID

When you hit COMMIT, is your data really safe? See how PostgreSQL uses WAL to guarantee Durability- the ‘D’ in ACID 

* * *

### Understanding Durability in PostgreSQL -A Deep Dive into the “D” in ACID

![](https://cdn-images-1.medium.com/max/800/1*AL879AAET-OT13Q6l-1u3w.jpeg)Photo by Matheus Viana: <https://www.pexels.com/photo/person-on-bike-2372972/>

* * *

So far in this series, we’ve looked at how PostgreSQL handles Atomicity, Consistency, and Isolation. But what happens _after_ you commit a transaction? What if the power goes out, the server crashes, or someone trips over the plug?

This is where **Durability** , the final letter in ACID, comes in. Durability means that once a transaction is committed, it will _not_ be lost- no matter what.

* * *

### What Does Durability Really Mean?

In practical terms, Durability means that when your application gets a `COMMIT` confirmation, the data is safely stored and recoverable even if the database crashes immediately afterward.

PostgreSQL achieves this with its **Write-Ahead Logging (WAL)** mechanism. Instead of immediately rewriting table files on disk, PostgreSQL writes changes to a log file first. If the system crashes, PostgreSQL can replay this log to get back to a consistent state.

* * *

### How Does WAL Work?

Here’s the basic flow:

  1. You run a transaction that changes some data.
  2. PostgreSQL writes the changes to the WAL file on disk.
  3. Only _after_ the WAL record is safely on disk does PostgreSQL acknowledge the `COMMIT`.



So the WAL acts like a black box flight recorder for your database.

* * *

### Let’s See Durability in Action

You can see WAL files in action in your data directory. Here’s a simple demo.

First, check your WAL settings:
    
    
    SHOW wal_level;  
    SHOW synchronous_commit;

By default, `synchronous_commit` is `on`. This means PostgreSQL waits until WAL changes are flushed to disk before confirming the commit.

* * *

### Test: Crash Recovery (Safe Experiment)

Let’s simulate how WAL protects your data.

  1. Create a test table:


    
    
    CREATE TABLE durability_test (id SERIAL PRIMARY KEY, data TEXT);

2\. Insert some rows and commit:
    
    
    INSERT INTO durability_test (data) VALUES ('Important Data 1'), ('Important Data 2'); COMMIT;

3\. Now, force PostgreSQL to checkpoint to flush data to disk:
    
    
    CHECKPOINT;

4\. If the server crashes _after_ the WAL is written but _before_ data files are updated, PostgreSQL will replay the WAL on startup to make sure your rows are still there.

Of course, don’t yank the power cord — but you can trust that WAL would restore the committed rows.

* * *

### When Durability Can Be Tuned

Sometimes, applications may want to trade off strict Durability for speed. For example, you can turn off `synchronous_commit`:
    
    
    SET synchronous_commit = off;

Now PostgreSQL can acknowledge a commit _before_ the WAL is flushed to disk. If the server crashes immediately, you could lose the last few transactions.

This is faster but obviously less durable — so use it only when you’re okay with that risk (like bulk loads or cache tables).

* * *

### Real-World Takeaway

Durability is what lets you sleep at night knowing your committed data won’t vanish. PostgreSQL’s WAL and crash recovery have been battle-tested for decades. As long as you keep your WAL files safe (and your disks healthy), your data stays safe too.

* * *

### References

  * [PostgreSQL: Write-Ahead Logging (WAL)](https://www.postgresql.org/docs/current/wal-intro.html)
  * [PostgreSQL: Synchronous Commit](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT)
  * [PostgreSQL: Crash Recovery](https://www.postgresql.org/docs/current/wal-reliability.html)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [July 7, 2025](https://medium.com/p/af42ce13fb2b).

[Canonical link](https://medium.com/@Kfir-G/understanding-durability-in-postgresql-a-deep-dive-into-the-d-in-acid-af42ce13fb2b)

Exported from [Medium](https://medium.com) on December 20, 2025.
