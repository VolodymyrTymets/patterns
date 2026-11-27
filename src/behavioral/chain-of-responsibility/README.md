## Chain of Responsibility actors

```
┌─────┬─────────────────────┬──────────────────────────────────────────────────┬──────────────────────────────┐
│  #  │         Role        │                    What it is                    │ In my example                │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 1   │ Handler Interface   │ Common interface for all handlers: handle a      │ Sender (ISender in TS)       │
│     │                     │ request and set the next handler in the chain    │ set_next / setNext(sender)   │
│     │                     │                                                  │ send(message, to)            │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 2   │ Base Handler        │ Optional abstract class with the shared code:    │ BaseHandler                  │
│     │                     │ stores the next handler and forwards the request │                              │
│     │                     │ to it                                            │                              │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 3   │ Concrete Handlers   │ Each one decides whether it can handle the       │ EmailSender (email)          │
│     │                     │ request, does its work, and/or passes the        │ WhatsappSender               │
│     │                     │ request on                                       │ (has_whatsapp and phone)     │
│     │                     │                                                  │ SmsSender (phone)            │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 4   │ Client              │ Builds the chain and sends the request to the    │ NotificationService, main()  │
│     │                     │ first handler; it does not know who handles it   │ (email -> whatsapp -> sms)   │
└─────┴─────────────────────┴──────────────────────────────────────────────────┴──────────────────────────────┘
```

### Key point

**Chain of Responsibility** passes a request along a chain of handlers. Each handler either
handles the request or passes it to the next one. The sender of the request is not tied to a
particular receiver: it only talks to the first handler. In the example, `EmailSender`,
`WhatsappSender` and `SmsSender` all extend `BaseHandler`:

- **Handle:** if the recipient meets the handler's condition (an email, a phone number with
  WhatsApp, or a phone number), the handler sends the message and the chain stops.
- **Pass on:** otherwise the handler forwards the request to the next one.
- **End of chain:** if no handler can process the request, `BaseHandler` reports it, so the
  message is not lost silently.
- **Order:** `WhatsappSender` comes before `SmsSender` because its condition is narrower; SMS
  is the fallback for any other phone number.

The order of the chain is set by the client at runtime, so handlers can be added, removed or
reordered without changing the other handlers. A handler may also do part of the work and
still pass the request on (as in middleware or logging chains). Use this pattern when more
than one object can handle a request and the right one is not known in advance, or when
checks must run in a specific order.

### Chain of Responsibility vs Decorator

Both link objects with the same interface and pass the call along, but the intent differs:

- **Decorator** adds behavior around a call and normally always forwards it to the wrapped
  object.
- **Chain of Responsibility** lets any handler stop the request, and handlers act
  independently of each other.

### Chain of Responsibility vs Proxy

- **Proxy** stands in for one object and controls access to it.
- **Chain of Responsibility** links several handlers, and any of them may be the receiver.

### Chain of Responsibility vs Composite

- **Composite** organizes objects into a tree and treats a group like a single object.
- **Chain of Responsibility** is often used with it: a component passes an unhandled request
  up to its parent.
