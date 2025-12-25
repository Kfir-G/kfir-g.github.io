---
title: Understanding Isolation In Postgresql  A Deep Dive Into The  I  In Acid
published: true
date: 2025-07-07 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/c493d635a35b
---

# Understanding Isolation in PostgreSQL: A Deep Dive into the “I” in ACID

How does PostgreSQL keep your transactions from stepping on each other? Dive deep into Isolation- the ‘I’ in ACID -with real examples 

* * *

### Understanding Isolation in PostgreSQL: A Deep Dive into the “I” in ACID

![](https://cdn-images-1.medium.com/max/800/1*w8bYYfVQxfSZuy1dzA07Ng.jpeg)Photo by Matheus Viana: <https://www.pexels.com/photo/open-locker-in-wooden-locker-room-31220117/>

When we talk about PostgreSQL being _ACID-compliant_ , Isolation is the “I” that quietly does a lot of heavy lifting. In my previous articles, we explored Atomicity and Consistency -how PostgreSQL makes sure that transactions either happen fully or not at all, and that the database remains valid. Now it’s time to look at how Isolation keeps transactions from interfering with each other when multiple operations run at the same time.

Isolation sounds simple: each transaction should run as if it’s the only one. But the details can get tricky, especially when different isolation levels come into play. Let’s see what this means, how it works in PostgreSQL, and what to watch out for.

* * *

### What Isolation Means

In short, Isolation makes sure that the intermediate state of a transaction is invisible to other transactions. If one transaction is in the middle of changing a row, another transaction shouldn’t see a half-finished version of that row.

Without Isolation, you can run into problems like:

  * **Dirty reads** : reading uncommitted changes that might get rolled back.
  * **Non-repeatable reads** : getting different results when you read the same row twice in a transaction.
  * **Phantom reads** : rows appear or disappear when you run the same query again.



PostgreSQL handles this with different isolation levels, each balancing correctness and performance.

* * *

### PostgreSQL’s Isolation Levels

PostgreSQL supports the standard SQL isolation levels:

  1. **Read Uncommitted**  
PostgreSQL actually treats this the same as Read Committed, so dirty reads are never allowed.
  2. **Read Committed** (default)  
Each query sees a snapshot of the database taken at the start of that query. Changes committed by other transactions become visible to the next query in the same transaction.
  3. **Repeatable Read**  
All queries in the transaction see the same snapshot taken when the transaction starts. You avoid non-repeatable reads, but phantom reads can still happen.
  4. **Serializable**  
The strictest level. Transactions run as if they were executed one after another. PostgreSQL uses Serializable Snapshot Isolation (SSI) to make this work and may abort transactions that can’t be serialized.



* * *

### Let’s See Isolation in Action

Here’s a simple table to experiment with:
    
    
    CREATE TABLE inventory (  
      id SERIAL PRIMARY KEY,  
      stock INT  
    );  
      
    INSERT INTO inventory (stock) VALUES (100);

Open two `psql` sessions: Session A and Session B.

* * *

### Read Committed: Non-Repeatable Reads

In Session A:
    
    
    BEGIN;  
    SET TRANSACTION ISOLATION LEVEL READ COMMITTED;  
      
    SELECT stock FROM inventory WHERE id = 1;  
    -- stock = 100

In Session B:
    
    
    UPDATE inventory SET stock = 50 WHERE id = 1;  
    COMMIT;

Back in Session A:
    
    
    SELECT stock FROM inventory WHERE id = 1;  
    -- stock = 50

The same row gave a different value within the same transaction. This is a non-repeatable read, and it’s allowed in Read Committed.

* * *

### Repeatable Read: Same Snapshot

Now try Repeatable Read.

Session A:
    
    
    BEGIN;  
    SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;  
      
    SELECT stock FROM inventory WHERE id = 1;  
    -- stock = 100

Session B:
    
    
    UPDATE inventory SET stock = 30 WHERE id = 1;  
    COMMIT;

Back in Session A:
    
    
    SELECT stock FROM inventory WHERE id = 1;  
    -- stock = 100

This time, the value stays the same because Repeatable Read ensures you always see the same snapshot.

* * *

### Serializable: Strictest Isolation

With Serializable, PostgreSQL checks whether your transactions could produce different results than if they ran one after the other.

Session A:
    
    
    BEGIN;  
    SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;  
      
    SELECT stock FROM inventory WHERE id = 1;  
    -- 100  
      
    UPDATE inventory SET stock = stock - 10 WHERE id = 1;

Session B:
    
    
    BEGIN;  
    SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;  
      
    SELECT stock FROM inventory WHERE id = 1;  
    -- 100  
      
    UPDATE inventory SET stock = stock - 20 WHERE id = 1;  
    COMMIT;

Back in Session A:
    
    
    COMMIT;  
    -- ERROR: could not serialize access due to concurrent update

PostgreSQL detects that running these transactions together could lead to inconsistencies, so it rolls one back. Better safe than sorry.

* * *

### Choosing the Right Level

  * **Read Committed** works well for most use cases where short transactions don’t need repeatable reads.
  * **Repeatable Read** is useful for consistent reads in longer transactions or reports.
  * **Serializable** is the safest but can lead to transaction rollbacks, so you need to handle retries.



* * *

### Final Thoughts

Isolation is about making sure your transactions don’t see each other’s work half-finished. It’s not something you think about every day- until things go wrong because of subtle race conditions.

Getting Isolation right is key to safe and predictable data in multi-user systems. Now you know what each level does and how PostgreSQL keeps your data consistent even when things get busy.

* * *

### References

  * [PostgreSQL: Isolation Levels](https://www.postgresql.org/docs/current/transaction-iso.html)
  * [PostgreSQL: Serializable Isolation](https://www.postgresql.org/docs/current/transaction-iso.html#XACT-SERIALIZABLE)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [July 7, 2025](https://medium.com/p/c493d635a35b).

[Canonical link](https://medium.com/@Kfir-G/understanding-isolation-in-postgresql-a-deep-dive-into-the-i-in-acid-c493d635a35b)
