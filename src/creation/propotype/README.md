## Prototype actors

```
  ┌─────┬───────────────────┬──────────────────────────────────────────────────┬─────────────────────────────┐
  │  #  │       Role        │                   What it is                     │       In my example         │
  ├─────┼───────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 1   │ Prototype         │ Interface that declares the cloning method, so   │ INotification (clone)       │
  │     │                   │ objects can be copied without knowing their      │                             │
  │     │                   │ concrete class                                   │                             │
  ├─────┼───────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 2   │ ConcretePrototype │ Implements clone() by creating a new object of   │ Notification,               │
  │     │                   │ its own class and copying its own state into it, │ SmsNotification,            │
  │     │                   │ including fields that only it knows about        │ EmailNotification (subject),│
  │     │                   │                                                  │ LogNotification (metadata)  │
  ├─────┼───────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 3   │ Client            │ Creates new objects by cloning a prototype       │ LogService, which holds     │
  │     │                   │ instead of calling constructors of concrete      │ registered prototypes and   │
  │     │                   │ classes                                          │ create(name) clones them    │
  └─────┴───────────────────┴──────────────────────────────────────────────────┴─────────────────────────────┘
```

### Key point

`clone()` is declared on the interface but implemented by every concrete class, so a copy
always has the same concrete type as the original (a `LogNotification` clones into a
`LogNotification`). The client never depends on the concrete class. Nested state, such as
`metadata`, is copied into a new object so the clone does not share it with the original.
