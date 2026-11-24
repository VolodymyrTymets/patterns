## Proxy actors

```
┌─────┬─────────────────────┬──────────────────────────────────────────────────┬──────────────────────────────┐
│  #  │         Role        │                    What it is                    │ In my example                │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 1   │ Service Interface   │ Common interface for the real service and its    │ ISender                      │
│     │                     │ proxy; the client only knows this type           │ send(message, to)            │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 2   │ Real Service        │ Does the real, often expensive work. It does     │ EmailSender                  │
│     │                     │ not know that a proxy sits in front of it        │ (opens an SMTP connection    │
│     │                     │                                                  │ when it is created)          │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 3   │ Proxy               │ Implements the same interface, holds or creates  │ EmailSenderProxy(role)       │
│     │                     │ the real service and controls access to it,      │ send(message, to)            │
│     │                     │ then delegates the call                          │ (lazy creation, role check)  │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 4   │ Client              │ Works with the service only through the          │ main()                       │
│     │                     │ interface, so a proxy can replace the real one   │ (calls send on the proxy)    │
└─────┴─────────────────────┴──────────────────────────────────────────────────┴──────────────────────────────┘
```

### Key point

A **Proxy** stands in for another object and controls access to it. It implements the same
**Service Interface** as the **Real Service**, so the client cannot tell the difference, and
every call goes through the proxy first. The proxy can do something before or after
forwarding the call, or decide not to forward it at all. In the example, `EmailSenderProxy`
implements `ISender` and does two things:

- **Lazy creation (virtual proxy):** the real `EmailSender` is expensive to create (it opens
  an SMTP connection), so the proxy creates it on the first `send`, not when the proxy is
  built. If `send` is never called, the connection is never opened.
- **Access control (protection proxy):** the proxy checks the caller's role and throws if it
  is not allowed to send, so the real `EmailSender` does not need to know about permissions.

Other common kinds are a **caching proxy** (return a stored result), a **logging proxy**
(record each call) and a **remote proxy** (a local object that talks to a service on another
machine). Use a proxy when you need to add access control, lazy loading, caching or logging
around an object without changing it or its clients.

### Proxy vs Decorator

The structure is almost the same (same interface, holds another object), but the intent
differs:

- **Decorator** adds new behavior to an object, and the client decides how to stack
  decorators.
- **Proxy** controls access to an object and usually manages its lifecycle itself (it
  creates the real service), so the client does not build the real object at all.

### Proxy vs Facade

- **Facade** gives a new, simpler interface to a group of objects.
- **Proxy** keeps the same interface as one object and stands in for it.

### Proxy vs Adapter

- **Adapter** changes the interface of an object so it fits the client.
- **Proxy** keeps the interface and controls access to the object.
