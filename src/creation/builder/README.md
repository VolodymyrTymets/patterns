## Builder actors
```
  ┌─────┬──────────────────┬──────────────────────────────────────────────────┬─────────────────────────────┐
  │  #  │       Role       │                   What it is                     │       In my example         │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 1   │ Product          │ The complex object being constructed step by     │ Notification                │
  │     │                  │ step. Its parts are set only through the builder │                             │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 2   │ Builder          │ Interface that declares the construction steps   │ NotificationBuilder         │
  │     │                  │ common to all builders (and a way to get the     │ (setRecipient, setSubject,  │
  │     │                  │ result)                                          │ setBody, build)             │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 3   │ ConcreteBuilder  │ Implements the construction steps for one        │ EmailNotificationBuilder,   │
  │     │                  │ variant, keeps the product being assembled and   │ SmsNotificationBuilder      │
  │     │                  │ returns it when done                             │                             │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 4   │ Director         │ Optional. Defines the order in which the steps   │ NotificationDirector        │
  │     │                  │ are called, so ready-made configurations can be  │ (buildWelcome, buildAlert)  │
  │     │                  │ reused. Works only through the Builder interface │                             │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 5   │ Client           │ Picks a ConcreteBuilder, optionally passes it to │ Code that creates a builder │
  │     │                  │ a Director, then gets the finished product from  │ and calls build() to get a  │
  │     │                  │ the builder                                      │ Notification                │
  └─────┴──────────────────┴──────────────────────────────────────────────────┴─────────────────────────────┘
```

### Key point
The product is assembled step by step and is only handed out once it is complete, so the
client never sees a half-built object. The same construction process (Director) can produce
different representations just by swapping the ConcreteBuilder.
