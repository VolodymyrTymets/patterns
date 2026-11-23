## Composite actors

```
┌─────┬─────────────────────┬──────────────────────────────────────────────────┬──────────────────────────────┐
│  #  │        Role         │                    What it is                    │       In my example          │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 1   │ Component           │ Common interface for both simple and composite   │ ISender                      │
│     │                     │ elements; the client only knows this type        │ send(message, to)            │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 2   │ Leaf                │ Basic element with no children; does the real    │ EmailSender                  │
│     │                     │ work itself                                      │ SmsSender                    │
│     │                     │                                                  │ WhatsappSender               │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 3   │ Composite           │ Holds child Components (leaves or other          │ BroadcastSender              │
│     │ (Container)         │ composites) and implements the Component         │ send(message, to)            │
│     │                     │ interface by delegating to every child           │ add(sender) / remove(sender) │
├─────┼─────────────────────┼──────────────────────────────────────────────────┼──────────────────────────────┤
│ 4   │ Client              │ Works with any element through the Component     │ main()                       │
│     │                     │ interface, without caring if it is a leaf or     │ (builds the tree, calls      │
│     │                     │ a composite                                      │ send once on the root)       │
└─────┴─────────────────────┴──────────────────────────────────────────────────┴──────────────────────────────┘
```

### Key point

Objects are arranged into a tree, and a single element and a group of elements are treated
the same way. A **Composite** implements the same **Component** interface as its **Leaves**
and forwards each call to its children, which may themselves be composites. The client calls
`send` once on the root and does not need to know whether it is talking to one sender or a
whole tree of them (in the example a root `BroadcastSender` contains an `EmailSender` and a
nested `BroadcastSender` that holds an `SmsSender` and a `WhatsappSender`). Use it when the structure is naturally recursive
(part-whole hierarchy) and you want to avoid `if leaf / else loop` checks in client code.

### Composite vs Bridge

Both rely on composition, but the intent differs:

- **Bridge** splits one class into two hierarchies (abstraction and implementation) held by
  a single reference, so they vary independently.
- **Composite** holds a collection of objects of the same interface and builds a tree, so a
  group behaves like a single object.
