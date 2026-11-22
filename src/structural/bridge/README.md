## Bridge actors

```
┌─────┬─────────────────────┬──────────────────────────────────────────────────┬──────────────────────────────┐
│  #  │        Role         │                    What it is                    │       In my example          │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 1   │ Abstraction         │ High-level control layer; holds a reference to   │ Notification                 │
│     │                     │ an Implementor and delegates the real work to    │ notify(message, to)          │
│     │                     │ it instead of doing it itself                    │ (holds an ISender)           │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 2   │ Refined Abstraction │ Variant of the Abstraction that changes the      │ AlertNotification            │
│     │                     │ high-level logic, still working only through     │ ReminderNotification         │
│     │                     │ the Implementor interface                        │ (format the message)         │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 3   │ Implementor         │ Interface for the implementation side; does not  │ ISender                      │
│     │                     │ have to match the Abstraction's interface        │ send(message, to)            │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 4   │ Concrete            │ Platform-specific implementations of the         │ EmailSender                  │
│     │ Implementor         │ Implementor interface                            │ SmsSender                    │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 5   │ Client              │ Chooses a Refined Abstraction and a Concrete     │ main()                       │
│     │                     │ Implementor, links them and uses the result      │ (injects a sender into a     │
│     │                     │                                                  │ notification, calls notify)  │
└─────┴─────────────────────┴──────────────────────────────────────────────────┴──────────────────────────────┘
```

### Key point

A class that varies in two independent ways (what kind of notification, and how it is
delivered) is split into two hierarchies connected by composition. The **Abstraction** holds
a reference to an **Implementor** and delegates delivery to it, so either side can be
extended without touching the other. M notification types and N senders need M + N classes
instead of M × N (`AlertEmail`, `AlertSms`, `ReminderEmail`, ...). The client picks the
combination at runtime.

### Bridge vs Adapter

The code looks similar (one object wraps another), but the intent differs:

- **Adapter** is applied after the fact to make an existing, incompatible class fit an
  interface the client already expects.
- **Bridge** is designed up front so abstraction and implementation can vary independently.
