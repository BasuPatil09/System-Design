# Transactions

A transaction groups several operations into one unit that either all succeed or all fail. The classic example is a money transfer.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

If the database crashes after the first update, the transaction was never committed, so on restart it's undone. Nobody loses 100. Databases manage this with a write-ahead log: changes are recorded in a log on disk before they're applied, so after a crash the database can replay or undo them.

## When transactions run at the same time

Running transactions strictly one after another would be correct but slow. So databases let them overlap and offer isolation levels, which control what odd results you're willing to tolerate. The odd results have names.

A dirty read is seeing another transaction's changes before it has committed. A non-repeatable read is reading the same row twice in one transaction and getting different values, because someone else committed in between. A phantom read is running the same query twice and getting extra rows the second time, because someone inserted matching rows.

| Isolation level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| Read uncommitted | Possible | Possible | Possible |
| Read committed | Prevented | Possible | Possible |
| Repeatable read | Prevented | Prevented | Possible by the standard |
| Serializable | Prevented | Prevented | Prevented |

That table is the SQL standard. Real databases differ in the details. PostgreSQL's repeatable read also blocks phantoms, because it uses snapshots. PostgreSQL defaults to read committed, and MySQL's InnoDB defaults to repeatable read. Higher isolation is safer but slower and causes more conflicts, so many applications stay at the default and handle the rare problem cases by hand.

## How isolation is done

One approach is locking. A transaction locks the rows it touches, and others wait. The other is MVCC (multi-version concurrency control), used by PostgreSQL, MySQL and Oracle. The database keeps several versions of a row, and each transaction reads from a consistent snapshot. Readers don't block writers and writers don't block readers, which is why MVCC does well on read-heavy workloads.

## Deadlocks

Two transactions can each hold a lock the other needs, and both wait forever. Databases detect the cycle and abort one of them, and your code gets an error to retry. You can reduce them by always touching rows in the same order and keeping transactions short.

Transactions that span more than one database or service are much harder. That's the topic of [Distributed Transactions](07-distributed-transactions.md).

<!-- nav:start -->
---

Previous: [CAP and PACELC](05-cap-and-pacelc.md) | Next: [Distributed Transactions](07-distributed-transactions.md) | [All topics](../README.md)
<!-- nav:end -->
