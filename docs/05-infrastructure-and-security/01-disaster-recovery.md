# Disaster Recovery

High availability handles small failures, like a server or a disk. Disaster recovery (DR) covers the large ones: a whole datacenter or region going offline, a ransomware attack, a mistaken deletion of a production database. The question changes from "how do we avoid downtime?" to "how do we get back?"

## Two numbers that drive everything

Recovery time objective (RTO) is how long the business can accept being down. Recovery point objective (RPO) is how much recent data it can afford to lose, measured in time. An RPO of 15 minutes means that after recovery you may lose up to the last 15 minutes of data. An RPO of zero means no loss at all, which needs synchronous copies elsewhere.

```mermaid
flowchart LR
    A["Last good copy"] -->|"RPO: data lost"| B["Disaster"] -->|"RTO: time to recover"| C["Back in service"]
```

Both are business decisions with a price tag. Smaller numbers mean more infrastructure running all the time. Ask the owners what an hour of downtime actually costs before choosing.

## Strategies

These go from cheapest and slowest to most expensive and fastest.

| Strategy | What you keep ready | Typical RTO | Typical RPO |
|---|---|---|---|
| Backup and restore | Backups stored in another region | Hours | Hours |
| Pilot light | Data replicated, core services off or tiny | Tens of minutes | Minutes |
| Warm standby | Smaller but running copy of the whole system | Minutes | Seconds to minutes |
| Active-active | Full system live in two or more regions | Near zero | Near zero |

Backup and restore is simplest but slowest. A pilot light keeps the database replicated so data is current, and the application servers are created only when needed. Warm standby keeps a scaled-down but working copy that you scale up on failover. Active-active runs everywhere all the time, and failing over is mostly a matter of routing traffic away, but it's the hardest to build, since data has to stay consistent across regions.

## Backups

A common rule is 3-2-1: three copies of the data, on two different kinds of storage, with one off-site. Keep at least one copy immutable or offline so ransomware can't encrypt or delete it. Replication is not a backup. If someone deletes a table, replication faithfully deletes it everywhere within seconds.

## Practice

A plan that's never been tested is a hope. Run restore drills, time them, and compare against the RTO. Many teams find during their first drill that backups were incomplete, credentials were missing, or the runbook was out of date. Automate failover where you can, because during a real incident people are stressed and make mistakes. See [Availability](../01-fundamentals/10-availability.md) for the related day-to-day failure handling.

<!-- nav:start -->
---

Previous: [Observability](../04-design-toolkit/08-observability.md) | Next: [Virtual Machines and Containers](02-vms-and-containers.md) | [All topics](../README.md)
<!-- nav:end -->
