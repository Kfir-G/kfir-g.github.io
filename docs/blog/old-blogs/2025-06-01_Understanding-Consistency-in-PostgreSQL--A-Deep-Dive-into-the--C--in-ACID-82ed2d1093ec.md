---
title: Understanding Consistency In Postgresql  A Deep Dive Into The  C  In Acid
published: true
date: 2025-06-01 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/82ed2d1093ec
---

# Understanding Consistency in PostgreSQL: A Deep Dive into the “C” in ACID

How PostgreSQL keeps your data safe from logical errors using constraints, triggers, and transactional rules 

* * *

### Understanding Consistency in PostgreSQL: A Deep Dive into the “C” in ACID

![](https://cdn-images-1.medium.com/max/800/1*HjAix9wWNkXyGl1BfIvVkw.jpeg)Photo by Matheus Viana: <https://www.pexels.com/photo/orange-wall-and-sitting-boy-10216566/>

* * *

In systems where data correctness is non-negotiable- whether you’re handling user authentication, e-commerce inventory, or hospital patient records- **Consistency** is the invisible guardrail that ensures the rules of your domain are never broken.

This article explores **Consistency** , the second principle of ACID. We’ll walk through how PostgreSQL enforces it via constraints, how violations are handled, and what developers need to be mindful of to avoid state corruption in real-world systems.

* * *

### What Consistency Really Means

Consistency ensures that a transaction brings the database from one valid state to another. That means all defined **constraints, rules, and invariants** must be satisfied before and after every transaction.

If any part of a transaction would leave the data in an invalid state, PostgreSQL **rejects the entire transaction-** not just the failing statement-preserving the integrity of your system.

* * *

### A Schema With Invariants

Let’s return to our simple banking system and define some rules we want PostgreSQL to enforce:
    
    
    CREATE TABLE accounts (  
        id SERIAL PRIMARY KEY,  
        name TEXT NOT NULL,  
        balance INTEGER NOT NULL CHECK (balance >= 0),  
        UNIQUE(name)  
    );

Here, we’ve defined:

  * Every account must have a non-null name.
  * Balances must be zero or greater.
  * Names must be unique.



These are **declarative constraints**. PostgreSQL uses them to guarantee that no transaction can violate your domain rules.

* * *

### Violating Consistency with a Bad Transaction

Say Alice tries to transfer more than she has:
    
    
    BEGIN;  
      
    UPDATE accounts SET balance = balance - 1200 WHERE name = 'Alice';  
    UPDATE accounts SET balance = balance + 1200 WHERE name = 'Bob';  
      
    COMMIT;

If Alice only has 1000, PostgreSQL will raise:
    
    
    ERROR:  new row for relation "accounts" violates check constraint "accounts_balance_check"

At this point, the transaction is marked as failed and must be rolled back:
    
    
    ROLLBACK;

**Result** : No changes are applied. This is Consistency at work- the integrity rule (`balance >= 0`) was violated, so PostgreSQL refused to apply any part of the transaction.

* * *

### Enforcing Business Logic with Triggers

Not all rules are easily encoded as column constraints. For more complex logic- like age-based restrictions or cross-table validations- we can use **triggers**.

Example: prevent creating users under age 18.
    
    
    CREATE OR REPLACE FUNCTION check_age()  
    RETURNS TRIGGER AS $$  
    BEGIN  
        IF NEW.age < 18 THEN  
            RAISE EXCEPTION 'Age must be at least 18';  
        END IF;  
        RETURN NEW;  
    END;  
    $$ LANGUAGE plpgsql;  
      
    CREATE TRIGGER check_age_trigger  
    BEFORE INSERT OR UPDATE ON users  
    FOR EACH ROW  
    EXECUTE FUNCTION check_age();

Now, any `INSERT` or `UPDATE` that violates this rule will automatically fail, and the transaction will be rolled back- keeping the system in a consistent state.

* * *

### Referential Integrity via Foreign Keys

Let’s introduce a `transactions` table that logs money transfers:
    
    
    CREATE TABLE transactions (  
        id SERIAL PRIMARY KEY,  
        from_account INTEGER REFERENCES accounts(id),  
        to_account INTEGER REFERENCES accounts(id),  
        amount INTEGER NOT NULL CHECK (amount > 0)  
    );

PostgreSQL ensures that both `from_account` and `to_account` actually exist. Attempting to insert a transaction for a non-existent account will fail immediately.
    
    
    INSERT INTO transactions (from_account, to_account, amount)  
    VALUES (999, 2, 100);
    
    
    ERROR:  insert or update on table "transactions" violates foreign key constraint

That’s PostgreSQL maintaining consistency via **referential integrity**.

* * *

### Consistency in Application Code (Python + psycopg3)

Here’s how consistency violations behave in real-world application code:
    
    
    import psycopg  
      
    conn = psycopg.connect("postgresql://user:pass@localhost/db")  
      
    try:  
        with conn.transaction():  
            with conn.cursor() as cur:  
                cur.execute("UPDATE accounts SET balance = balance - 1200 WHERE name = 'Alice'")  
                cur.execute("UPDATE accounts SET balance = balance + 1200 WHERE name = 'Bob'")  
      
    except Exception as e:  
        print(f"Transaction failed: {e}")

If the `balance - 1200` fails the `CHECK` constraint, the entire block is rolled back. You’ll never end up in a partial state where Alice lost money but Bob gained nothing.

* * *

### Summary of Cases

  * **Constraint violations** : Cause immediate rollback of the entire transaction.
  * **Triggers** : Allow custom rules that extend beyond column-level checks.
  * **Foreign key violations** : Prevent inconsistent references between tables.
  * **Application-level transactions** : `psycopg3` ensures that rule violations bubble up cleanly, triggering a rollback.



* * *

### Final Thoughts

Consistency is the safety net that protects your data from logical corruption. PostgreSQL’s constraint system- combined with triggers and foreign keys- ensures that your application’s data model is always honored.

If you’re building systems where correctness matters, you must treat consistency as a first-class design concern. Don’t rely on application code alone to enforce business rules- declarative constraints and transactional integrity are your best allies.

* * *

**Further Reading:**

  * [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
  * [PostgreSQL Foreign Keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
  * [Triggers](https://www.postgresql.org/docs/current/plpgsql-trigger.html)
  * [psycopg3 Transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html)



By [Kfir Gisman](https://medium.com/@Kfir-G) on [June 1, 2025](https://medium.com/p/82ed2d1093ec).

[Canonical link](https://medium.com/@Kfir-G/understanding-consistency-in-postgresql-a-deep-dive-into-the-c-in-acid-82ed2d1093ec)

Exported from [Medium](https://medium.com) on December 20, 2025.
