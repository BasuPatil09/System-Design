# REST, GraphQL and gRPC

These are three popular ways for programs to talk to each other over a network. They make different trade-offs.

## REST

REST models an API as resources identified by URLs, manipulated with the standard HTTP methods. `GET /users/42` reads a user, `POST /users` creates one, `PUT` replaces, `DELETE` removes. Responses are usually JSON, and status codes say what happened: 200 for success, 404 for not found, 429 for too many requests.

It's simple, works with every client and tool, and takes full advantage of HTTP caching. Its weak spots are fetching too much or too little. A mobile screen might need data from three endpoints, or get ten fields when it wants two.

Some habits make REST APIs better. Use cursor-based pagination for large lists, because page numbers break when items are added mid-browse. Make `GET`, `PUT` and `DELETE` idempotent, and let clients send an idempotency key with `POST` so a retried payment isn't charged twice. Version the API so you can change it without breaking existing clients.

## GraphQL

With GraphQL there's one endpoint, and the client sends a query describing exactly the fields it wants. The server returns that shape and nothing else.

```graphql
query {
  user(id: 42) {
    name
    orders(last: 3) { total }
  }
}
```

It solves over-fetching and lets front-end teams change what they ask for without waiting for new endpoints. It has a strongly typed schema. The costs are on the server side. Caching is harder because everything goes through one `POST` endpoint, a careless query can ask for an enormous amount of nested data, and naive resolvers can fire a database query per item, the well-known N+1 problem. You end up needing query depth limits and batching tools.

## gRPC

gRPC defines services and messages in `.proto` files, and generates client and server code in many languages. Messages are encoded in Protocol Buffers, a compact binary format, and sent over HTTP/2. It's fast, strictly typed, and supports streaming in either direction.

It's an excellent choice for calls between internal services, where speed and strict contracts matter. It's a poor fit for public APIs consumed by browsers, since browsers can't speak it directly without a proxy layer (gRPC-Web), and binary messages are harder to inspect by hand.

## Which to pick

| | REST | GraphQL | gRPC |
|---|---|---|---|
| Format | JSON over HTTP | JSON over HTTP | Protobuf over HTTP/2 |
| Contract | Optional (OpenAPI) | Typed schema | Required `.proto` |
| Caching | Easy, uses HTTP | Hard | Manual |
| Streaming | Awkward | Via subscriptions | Built in |
| Best for | Public APIs | Varied clients with complex screens | Service-to-service |

It's common to mix them: REST or GraphQL at the edge facing clients, gRPC between services inside.

<!-- nav:start -->
---

Previous: [API Gateway](09-api-gateway.md) | Next: [Long Polling, WebSockets and Server-Sent Events](11-long-polling-websockets-sse.md) | [All topics](../README.md)
<!-- nav:end -->
