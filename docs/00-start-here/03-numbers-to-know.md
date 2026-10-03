# Numbers Worth Remembering

Back-of-the-envelope math is how you decide whether a design is reasonable before you build anything. You don't need precision. You need to be right within a factor of ten.

## Time and traffic

A day has 86,400 seconds, which is close enough to 100,000 for quick math. That gives you a shortcut for turning daily totals into per-second rates.

| Requests per day | Roughly per second |
|---|---|
| 1 million | 12 |
| 100 million | 1,200 |
| 1 billion | 12,000 |

Traffic isn't flat. Peak load is often two to five times the daily average, so size for the peak.

## Data sizes

| Unit | Approximate size | Power of two |
|---|---|---|
| 1 KB | thousand bytes | 2^10 |
| 1 MB | million bytes | 2^20 |
| 1 GB | billion bytes | 2^30 |
| 1 TB | trillion bytes | 2^40 |
| 1 PB | quadrillion bytes | 2^50 |

A plain text character is about 1 byte. A tweet-sized post with metadata is a few hundred bytes. A compressed photo is around 200 KB to 3 MB, and a minute of compressed video is tens of megabytes.

## Latency

These are rough, order-of-magnitude figures. Hardware improves, but the ratios between them have stayed similar for years.

| Operation | Time |
|---|---|
| Read from memory | ~100 ns |
| Read from SSD (random) | ~100 µs |
| Round trip inside one datacenter | ~0.5 ms |
| Read from spinning disk (seek) | ~10 ms |
| Round trip across continents | ~100 to 150 ms |

The lesson is that memory is about a thousand times faster than SSD, and the network between regions is slower than almost anything on one machine. That's the whole reason caches and CDNs exist.

## A worked example

Say a photo app has 10 million daily users and each uploads one 2 MB photo.

Storage per day is 10M × 2 MB = 20 TB. Over a year that's about 7.3 PB, before replicas. If you keep three copies, call it 22 PB.

Upload rate is 10M / 86,400 ≈ 116 per second on average. If peak is four times that, plan for roughly 500 uploads per second, or about 1 GB/s of incoming bandwidth. One server can't take that, so you already know uploads need several servers and a storage system built for large files.

That took thirty seconds and already shaped the design.

<!-- nav:start -->
---

Previous: [How to Approach a Design Interview](02-interview-approach.md) | Next: [IP Address](../01-fundamentals/01-ip.md) | [All topics](../README.md)
<!-- nav:end -->
