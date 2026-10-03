# Scalability

A system is scalable if it can handle more load by adding resources, without being redesigned. "Load" might be users, requests per second, data volume, or all three.

## Two ways to grow

Vertical scaling means using a bigger machine, with more CPU, more RAM and faster disks. It's simple because nothing about the software changes. But there's a ceiling on how big a single machine gets, the price rises steeply near the top, and you still have one box that can fail.

Horizontal scaling means adding more machines and sharing the work. There's almost no ceiling and each machine is cheap, but now you have to coordinate them. Requests need a [load balancer](05-load-balancing.md), and data may need to be split across machines.

The practical rule is to go vertical while it's easy and cheap, and plan for horizontal before you hit the wall.

## What makes horizontal scaling possible

Stateless servers are the big one. If a server keeps nothing between requests, any server can handle any request, and adding another is trivial. Session data, uploaded files and anything else that has to be remembered goes into a shared store instead.

The data layer is harder, because state has to live somewhere. That's why so much of this guide is about databases.

## Where bottlenecks move

You fix one bottleneck and the next one shows up. A typical path looks like this:

1. Slow queries. Add [indexes](../02-databases/08-indexes.md) and fix bad queries.
2. Too many reads. Add a [cache](07-caching.md) and [read replicas](../02-databases/09-replication.md).
3. Too many writes, or too much data for one machine. [Shard](../02-databases/10-sharding.md) the database.
4. Slow work inside requests. Move it to a [queue](../03-architecture/02-message-brokers-and-queues.md) and process it in the background.
5. Global users. Use a [CDN](08-cdn.md) and run in several regions.

Each step adds complexity, so don't take a step until measurements say you need it. Plenty of products serve millions of users from one well-tuned database with a cache in front.

## Measuring it

Throughput is how much work is done per second. Latency is how long one request takes. Report latency as percentiles, like p50, p95 and p99, rather than the average. An average of 100 ms can hide the fact that 1 in 100 users waits five seconds, and with a big user base that's a lot of unhappy people.

<!-- nav:start -->
---

Previous: [Availability](10-availability.md) | Next: [Storage](12-storage.md) | [All topics](../README.md)
<!-- nav:end -->
