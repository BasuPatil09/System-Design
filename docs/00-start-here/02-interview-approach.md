# How to Approach a Design Interview

A design interview is open ended on purpose. Nobody expects you to build Twitter in 45 minutes. The interviewer wants to see how you think when the problem is vague, so a clear process matters more than a clever trick.

Here's an order that works for most questions.

1. Ask what the system must do. List the features you'll cover and say out loud what you're leaving out. "Post a message, follow someone, see a feed. No search, no ads."
2. Pin down the non-functional needs. How many users? Read heavy or write heavy? Is it fine if a post shows up two seconds late, or must everything be instantly consistent? How much downtime can you accept?
3. Do rough math. Requests per second, storage per year, bandwidth. It doesn't need to be exact. It only needs to tell you whether one database is enough or not.
4. Sketch the API and the data. A handful of endpoints and the main tables or collections. This forces you to decide what the system actually stores.
5. Draw the simple version first. Clients, a load balancer, some servers, a database. Walk one request through it from start to finish.
6. Find the bottleneck and fix it. Maybe reads overwhelm the database, so you add a cache. Maybe one table is too big, so you shard it. Explain why you picked each fix and what it costs.
7. Talk about failure. What if a server dies, a datacenter goes down, or a queue backs up?

Two habits help a lot. Think out loud so the interviewer can steer you, and when you choose something, name the alternative you rejected. "I'm using a relational database here because we need transactions on payments. If it were only a feed, I'd consider a wide-column store."

What tends to go badly is jumping straight to a fancy architecture before agreeing on requirements, or naming technologies without saying why. Kafka isn't an answer. It's an answer only when you can say what problem it solves in this design.

<!-- nav:start -->
---

Previous: [What Is System Design](01-what-is-system-design.md) | Next: [Numbers Worth Remembering](03-numbers-to-know.md) | [All topics](../README.md)
<!-- nav:end -->
