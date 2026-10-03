# ACID and BASE

These are two sets of promises a database can make about how it treats your data. ACID is the traditional one from relational databases. BASE describes the looser approach many distributed systems take.

## ACID

ACID is four properties that together describe a reliable transaction.

Atomicity means a transaction either happens completely or not at all. If you move 100 from account A to account B, you never end up with the money removed from A and not added to B. If anything fails midway, the whole thing is rolled back.

Consistency means a transaction takes the database from one valid state to another. Rules like "balance can't be negative" or "every order must point to a real customer" hold before and after.

Isolation means concurrent transactions don't see each other's half-finished work. They behave as if they ran one at a time, to a degree you can choose (see [Transactions](06-transactions.md)).

Durability means once the database says a transaction is committed, it stays committed, even if the power goes out a millisecond later. Databases get this by writing to a log on disk before confirming.

Banking, payments, inventory and bookings need these guarantees.

## BASE

BASE is a deliberately relaxed counterpart, and the name is a bit of a joke against ACID.

Basically available means the system keeps responding even when parts of it fail, though answers might be incomplete. Soft state means the data may change over time even without new input, as replicas catch up. Eventually consistent means that if no new updates arrive, all copies will end up the same, but not necessarily right away.

Think of a like counter on a post. If one user sees 1,041 and another sees 1,043 for a few seconds, nobody is harmed. Allowing that lets the system stay fast and available across many machines and regions.

## Choosing

| | ACID | BASE |
|---|---|---|
| Priority | Correctness | Availability and scale |
| Consistency | Immediate | Eventual |
| Typical setting | Money, orders, inventory | Feeds, counters, caches, analytics |
| Typical systems | PostgreSQL, MySQL | Cassandra, DynamoDB |

It's not either-or for a whole product. A shop might process the payment with ACID guarantees and show the "people viewing this" counter with BASE ones. The related question of how consistency trades against availability when a network fails is covered in [CAP and PACELC](05-cap-and-pacelc.md).

<!-- nav:start -->
---

Previous: [Normalization and Denormalization](03-normalization-and-denormalization.md) | Next: [CAP and PACELC](05-cap-and-pacelc.md) | [All topics](../README.md)
<!-- nav:end -->
