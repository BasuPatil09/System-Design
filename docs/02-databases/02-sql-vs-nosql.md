# SQL vs NoSQL

The two names get used as if they were opposite camps, but they're better seen as different tools. "NoSQL" is a loose label for any database that isn't a traditional relational one, and it covers several quite different designs.

## What SQL databases give you

You get a fixed schema, powerful queries including joins across tables, and ACID transactions (see [ACID and BASE](04-acid-and-base.md)). You can ask questions you didn't plan for when you designed the tables, which is a huge advantage when requirements change. The cost is that scaling writes beyond one machine takes real effort, since joins and transactions get hard once data is spread out.

## The NoSQL families

| Family | Shape of data | Examples | Fits well |
|---|---|---|---|
| Key-value | A key and an opaque value | Redis, DynamoDB | Sessions, caches, counters, shopping carts |
| Document | Nested JSON-like documents | MongoDB, Firestore | Product catalogues, user profiles |
| Wide-column | Rows with flexible columns grouped in families | Cassandra, HBase | Time series, huge write volumes, activity logs |
| Graph | Nodes and edges | Neo4j | Social networks, recommendations, fraud rings |

Most of these were built to spread across many machines easily, and many loosen consistency to do it. They usually want you to design around your queries ahead of time. In a document store you often embed related data inside one document, so a single read gets everything. That's fast, but if you later need a query nobody planned for, it can be painful.

## How to choose

Start from the access pattern, not the brand. Ask what you read, how you read it, and how much consistency you need.

If the data is structured, you need joins or transactions, and the volume fits on one primary with some replicas, use a relational database. That covers a surprising number of products, and it's the safer default.

Reach for NoSQL when there's a clear reason: a simple key lookup at huge scale, a very high write rate, data with no stable schema, or a graph-shaped problem. Many real systems use both, for example PostgreSQL for orders and payments, Redis for sessions, and Elasticsearch for search. Each extra store is more to run, monitor and keep in sync, so don't add one for fashion.

There's also a middle group sometimes called NewSQL, such as CockroachDB and Google Spanner, which aim to give SQL and transactions on top of a database that scales out. They remove some trade-offs but come with their own costs in latency and operations.

<!-- nav:start -->
---

Previous: [Databases and DBMS](01-databases-and-dbms.md) | Next: [Normalization and Denormalization](03-normalization-and-denormalization.md) | [All topics](../README.md)
<!-- nav:end -->
