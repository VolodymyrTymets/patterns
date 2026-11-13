## Explain
```
  ┌─────┬─────────────────┬───────────────────────────────────────────────────┬────────────────────────┐   
  │  #  │      Role       │                    What it is                     │     In my example      │   
  ├─────┼─────────────────┼───────────────────────────────────────────────────┼────────────────────────┤   
  │ 1   │ Product         │ The interface for the objects the factory method  │ Sender                 │   
  │     │                 │ creates                                           │                        │   
  ├─────┼─────────────────┼───────────────────────────────────────────────────┼────────────────────────┤   
  │ 2   │ ConcreteProduct │ A class that implements Product                   │ EmailSender, SmsSender │   
  ├─────┼─────────────────┼───────────────────────────────────────────────────┼────────────────────────┤   
  │     │                 │ An abstract class that declares the factory       │                        │   
  │ 3   │ Creator         │ method, returning a Product. It may also hold     │ Notification           │   
  │     │                 │ business logic that uses the product.             │                        │   
  ├─────┼─────────────────┼───────────────────────────────────────────────────┼────────────────────────┤   
  │ 4   │ ConcreteCreator │ A subclass that overrides the factory method to   │ EmailNotification,     │   
  │     │                 │ return a specific ConcreteProduct                 │ SmsNotification        │   
  └─────┴─────────────────┴───────────────────────────────────────────────────┴────────────────────────┘   
```