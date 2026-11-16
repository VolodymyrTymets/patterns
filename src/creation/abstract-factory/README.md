## Abstract Factory actors
```
  ┌─────┬──────────────────┬──────────────────────────────────────────────────┬─────────────────────────────┐
  │  #  │       Role       │                   What it is                     │       In my example         │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 1   │ AbstractProduct  │ Declares an interface for one kind of product in │ Sender, Formatter           │
  │     │                  │ a family of distinct but related products        │                             │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 2   │ ConcreteProduct  │ An implementation of an abstract product,        │ EmailSender,                │
  │     │                  │ grouped by variant. Every abstract product must  │ EmailFormatter,             │
  │     │                  │ be implemented in every variant                  │ SmsSender, SmsFormatter     │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 3   │ AbstractFactory  │ Interface that declares a creation method for    │ NotificationFactory         │
  │     │                  │ each abstract product                            │                             │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 4   │ ConcreteFactory  │ Implements the creation methods of the abstract  │ EmailNotificationFactory,   │
  │     │                  │ factory. Each one matches a single variant and   │ SmsNotificationFactory      │
  │     │                  │ creates only products of that variant            │                             │
  ├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 5   │ Client           │ Uses factories and products only through their   │ Code that receives a        │
  │     │                  │ abstract interfaces, so it works with any        │ NotificationFactory and     │
  │     │                  │ concrete factory / product variant               │ calls createSender /        │
  │     │                  │                                                  │ createFormatter             │
  └─────┴──────────────────┴──────────────────────────────────────────────────┴─────────────────────────────┘
```

### Key point
Concrete factories instantiate concrete products, but the signatures of their creation
methods return the corresponding **abstract** products. This way the client is never
coupled to the specific variant it gets from a factory.
