## Singleton actors

```
  ┌─────┬───────────┬──────────────────────────────────────────────────┬─────────────────────────────┐
  │  #  │   Role    │                   What it is                     │       In my example         │
  ├─────┼───────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 1   │ Singleton │ Class that allows only one instance, hides its   │ NotificationService         │
  │     │           │ constructor and exposes a way to get that        │ (getInstance in TS,         │
  │     │           │ instance                                         │ __new__ in Python)          │
  ├─────┼───────────┼──────────────────────────────────────────────────┼─────────────────────────────┤
  │ 2   │ Client    │ Gets the shared instance instead of creating     │ OrderModule, AuthModule     │
  │     │           │ its own, so all clients see the same state       │                             │
  └─────┴───────────┴──────────────────────────────────────────────────┴─────────────────────────────┘
```

### Key point

The instance is created lazily on the first request and then reused. In TypeScript the
constructor is `private`, so `new NotificationService()` does not compile. In Python
`__new__` returns the stored instance, so `NotificationService()` always gives the same
object. `OrderModule` and `AuthModule` never see each other, yet both write into the same
`notifications` list.
