## Adapter actors

```
┌─────┬──────────────────┬──────────────────────────────────────────────────┬─────────────────────────────┐
│  #  │       Role       │                    What it is                    │        In my example        │
├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
│ 1   │ Target           │ Interface the client expects and works with;     │ ISender                     │
│     │                  │ the contract every adapter must implement        │ send(message, to)           │
├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
│ 2   │ Client           │ Contains the business logic and talks to         │ NotificationSender          │
│     │                  │ other objects only through the Target            │ (receives an ISender)       │
│     │                  │ interface, never to the Adaptee directly         │                             │
├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
│ 3   │ Adaptee          │ Useful existing class (legacy / third-party)     │ ThirdPartySmsApi            │
│     │                  │ with an interface incompatible with Target;      │ sendText(phone, message)    │
│     │                  │ cannot or should not be modified                 │                             │
├─────┼──────────────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
│ 4   │ Adapter          │ Implements Target and wraps an Adaptee;          │ SmsApiAdapter               │
│     │                  │ translates Target calls into calls the           │ send(message, to) becomes   │
│     │                  │ Adaptee understands (and converts data)          │ sendText(to.phone, message) │
└─────┴──────────────────┴──────────────────────────────────────────────────┴─────────────────────────────┘
```

### Key point

The client depends only on the **Target** interface. The adapter implements that interface
and holds a reference to the adaptee, translating each call (method names, argument shapes,
return values) into what the adaptee expects. The adaptee stays untouched and the client
never learns it is talking to an incompatible class.
