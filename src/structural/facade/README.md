## Facade actors

```
┌─────┬─────────────────────┬──────────────────────────────────────────────────┬──────────────────────────────┐
│  #  │        Role         │                    What it is                    │       In my example          │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 1   │ Facade              │ Gives one simple entry point to a complex        │ NotificationFacade           │
│     │                     │ subsystem; knows which subsystem classes to      │ notify(type, message, to)    │
│     │                     │ call and in what order                           │                              │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 2   │ Subsystem classes   │ Do the real work. They know nothing about the    │ EmailSender                  │
│     │                     │ facade and can still be used directly            │ SmsSender                    │
│     │                     │                                                  │ WhatsappSender               │
│     │                     │                                                  │ (each: formatMessage, send)  │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 3   │ Client              │ Talks to the facade instead of to every          │ main()                       │
│     │                     │ subsystem class                                  │ (calls notify per channel)   │
└─────┴─────────────────────┴──────────────────────────────────────────────────┴──────────────────────────────┘
```

### Key point

A **Facade** is a simplified interface to a group of classes. Without it, the client has to
create each subsystem object, know its API and call them in the right order. With it, the
client makes one call and the **Facade** does the wiring. In the example, `NotificationFacade`
creates the three senders, looks up the right one for the requested `NotificationT`, formats
the message with `formatMessage` and then calls `send`, so `main()` only calls
`notify(type, message, to)`.

The facade does not hide the subsystem: its classes stay public, and a client that needs
something the facade does not offer can still use `EmailSender` or `SmsSender` directly. It
also does not add new behavior, it only coordinates what already exists. Use it when a
subsystem is complex or has many dependencies and most clients need only a small part of it,
or to give layers of a system a single entry point and reduce coupling.

### Facade vs Adapter

- **Adapter** changes the interface of one object so it fits what the client expects.
- **Facade** defines a new, simpler interface over a whole group of objects.

### Facade vs Decorator

- **Decorator** keeps the same interface and adds behavior to one object.
- **Facade** has its own interface and adds no behavior, it only delegates to the subsystem.

### Facade vs Mediator

Both coordinate several classes, but the direction differs:

- **Mediator** sits between colleagues that know about it and talk through it, so the
  communication is two-way.
- **Facade** is one-way: the client calls it, it calls the subsystem, and the subsystem does
  not know the facade exists.
