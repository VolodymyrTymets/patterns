## Decorator actors

```
┌─────┬─────────────────────┬──────────────────────────────────────────────────┬──────────────────────────────┐
│  #  │        Role         │                    What it is                    │       In my example          │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 1   │ Component           │ Common interface for plain objects and their     │ ISender                      │
│     │                     │ decorators; the client only knows this type      │ send(message, to)            │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 2   │ Concrete Component  │ Basic object that does the real work and that    │ EmailSender                  │
│     │                     │ can be wrapped by decorators                     │ SmsSender                    │
│     │                     │                                                  │ WhatsappSender               │
│     │                     │                                                  │ FlakySmsSender               │
│     │                     │                                                  │ (fails N times, then sends;  │
│     │                     │                                                  │ used to demo RetrySender)    │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 3   │ Base Decorator      │ Implements the Component interface, holds a     │ SenderDecorator              │
│     │                     │ reference to a wrapped Component and delegates   │ (holds an ISender, forwards  │
│     │                     │ every call to it                                 │ send to it)                  │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 4   │ Concrete Decorator  │ Adds behavior before or after delegating to the  │ LoggingSender                │
│     │                     │ wrapped Component, without changing its class    │ RetrySender                  │
│     │                     │                                                  │ (retries up to maxAttempts)  │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 5   │ Client              │ Wraps a Component in one or more decorators in   │ main()                       │
│     │                     │ the order it needs and uses the result as a      │ (stacks decorators around a  │
│     │                     │ normal Component                                 │ sender, calls send)          │
└─────┴─────────────────────┴──────────────────────────────────────────────────┴──────────────────────────────┘
```

### Key point

Behavior is added to an object at runtime by wrapping it, not by subclassing. A **Decorator**
implements the same **Component** interface as the object it wraps, so the client cannot tell
the difference, and decorators can be stacked in any order
(`new LoggingSender(new RetrySender(new EmailSender()))`). Each decorator does its extra work
(log, retry) and then forwards `send` to the wrapped sender. In the example `RetrySender`
wraps a `FlakySmsSender` that fails twice, so the send succeeds on the third attempt, and the
same `RetrySender` is reused around an `EmailSender` without changing either class. This avoids a class explosion
such as `LoggingEmailSender`, `RetryEmailSender`, `LoggingRetrySmsSender`, ... for every
combination of features and senders.

### Decorator vs Composite

The structure looks similar (both implement the Component interface and hold Components), but
the intent differs:

- **Composite** holds many children and combines their results, so a group behaves like a
  single object.
- **Decorator** wraps exactly one object and adds responsibilities to it, without changing
  its interface.

### Decorator vs Adapter

- **Adapter** changes the interface of an existing object so it fits what the client expects.
- **Decorator** keeps the same interface and only adds behavior.

### `@` decorator variant (TypeScript and Python)

`decorators.ts` and `decorators.py` show the same idea with the native `@` syntax (TC39
decorators in TS 5+, no `tsconfig` flag needed; plain function decorators in Python). The
roles map differently, because a decorator wraps a **method** instead of an object:

| Role in the class version | In `decorators.ts` / `decorators.py`                              |
| ------------------------- | ----------------------------------------------------------------- |
| Component                 | `ISender` / `Sender`                                              |
| Concrete Component        | `EmailSender`, `FlakySmsSender` (their `send` method is wrapped)  |
| Base + Concrete Decorator | `@Logging` (decorator), `@Retry(maxAttempts)` (decorator factory) |
| Client                    | `main()`                                                          |

- A decorator is a function that takes the original method and returns a replacement that
  adds behavior and then calls the original.
- `@Retry(3)` is a **decorator factory**: it takes its own parameter and returns the decorator.
- Decorators are applied bottom-up, so with `@Logging` above `@Retry()` the logging wraps the
  retry.
- The wrapping happens once, when the class is defined. A class decorated this way always has
  that behavior, whereas the class-based version lets the client choose and reorder
  decorators for each object at runtime.

Python specifics:

- A Python decorator is a function that takes the method and returns a wrapper. The wrapper
  must accept `self` as its first argument (`wrapper(self, message, to)`), because the
  decorated function becomes a method of the class. Without it, calling
  `sender.send(message=..., to=...)` fails with `got multiple values for argument 'message'`.
- `functools.wraps` keeps the name and docstring of the original method on the wrapper.
- `@Retry(max_attempts=3)` is a decorator factory, the same as in TypeScript: `Retry(3)` runs
  first and returns the decorator, which `@` then applies.
- Decorators apply bottom-up, the same as in TypeScript, so `@Logging` above `@Retry()` wraps
  the retry.
