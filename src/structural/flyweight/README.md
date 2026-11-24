## Flyweight actors

```
┌─────┬─────────────────────┬──────────────────────────────────────────────────┬──────────────────────────────┐
│  #  │         Role        │                    What it is                    │ In my example                │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 1   │ Flyweight           │ Holds the shared, immutable (intrinsic) state;   │ NotificationTemplate         │
│     │                     │ takes the extrinsic state as method arguments    │ (name, subject, body)        │
│     │                     │                                                  │ renderSubject / renderBody   │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 2   │ Flyweight Factory   │ Creates flyweights and keeps them in a pool;     │ TemplateFactory              │
│     │                     │ returns the existing one when the key matches    │ getTemplate(name)            │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 3   │ Context             │ Holds the extrinsic (unique) state and a         │ Notification                 │
│     │                     │ reference to a shared flyweight                  │ (recipient, params,          │
│     │                     │                                                  │ template, send())            │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 4   │ Client              │ Gets flyweights only from the factory and        │ Notifier, main()             │
│     │                     │ supplies the extrinsic state                     │ (collect many notifications, │
│     │                     │                                                  │ check the pool size)         │
└─────┴─────────────────────┴──────────────────────────────────────────────────┴──────────────────────────────┘
```

### Key point

Many objects share the same heavy, unchanging data instead of each keeping its own copy. The
state is split in two: **intrinsic** (shared, immutable, stored in the **Flyweight**) and
**extrinsic** (unique per object, kept in the **Context** or passed in by the client). A
**Flyweight Factory** hands out flyweights and reuses an existing one when the same key is
requested, so the client never creates them with `new`. In the example, five `Notification`
objects each hold only a recipient and params, and all of them point to four shared
`NotificationTemplate` instances (`welcome`, `reset-password`, `intro`, `goodbye`) that
contain the subject and body text. Both `welcome` notifications use the same instance:
`TemplateFactory.getTemplate(TemplateTypes.welcome)` returns it every time, so memory stays
flat as the number of notifications grows. `renderSubject` and `renderBody` throw on a
missing param instead of printing an empty placeholder.

Use it when an application creates a huge number of similar objects and most of their state
can be made shared and immutable. The trade-off is more complex code (state is split in two)
and a lookup on each use, so apply it only when memory is really a problem. A flyweight must
be immutable, otherwise a change made by one client would show up for all the others.

### Flyweight vs Singleton

- **Singleton** guarantees one instance of a class.
- **Flyweight** keeps one instance per distinct state (per key), and there can be many of them.

### Flyweight vs Factory

- A plain **Factory** creates a new object on every call.
- A **Flyweight Factory** is also a cache: it looks in the pool first and creates an object
  only when the key is new.

### Flyweight vs Composite

They are often combined: the shared leaves of a **Composite** tree can be flyweights to save
memory. A **Composite** is about structure (part-whole), a **Flyweight** is about sharing.
