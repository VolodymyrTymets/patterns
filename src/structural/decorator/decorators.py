# Decorator pattern with the native Python `@` syntax.
# Here a decorator wraps a method of the Component instead of wrapping the object.
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Protocol


# Recipients
@dataclass(frozen=True)
class PhoneRecipient:
    phone_number: str


@dataclass(frozen=True)
class EmailRecipient:
    email: str


Recipient = PhoneRecipient | EmailRecipient


# Component
class Sender(Protocol):
    def send(self, message: str, to: Recipient) -> None:
        pass


SendMethod = Callable[[Sender, str, Recipient], None]


# Concrete Decorators (method decorators)
def Logging(func: SendMethod) -> SendMethod:
    @wraps(func)
    def wrapper(self: Sender, message: str, to: Recipient) -> None:
        print(f"Logging: {message}")
        func(self, message, to)

    return wrapper


# Decorator factory: takes its own parameter, returns the decorator
def Retry(max_attempts: int = 3) -> Callable[[SendMethod], SendMethod]:
    def decorator(func: SendMethod) -> SendMethod:
        @wraps(func)
        def wrapper(self: Sender, message: str, to: Recipient) -> None:
            for attempt in range(1, max_attempts + 1):
                try:
                    func(self, message, to)
                    return
                except Exception:
                    print(f"Attempt {attempt}/{max_attempts} failed")
                    if attempt == max_attempts:
                        raise

        return wrapper

    return decorator


# Concrete Components (decorators are applied bottom-up: Retry first, then Logging)
class EmailSender(Sender):
    @Logging
    @Retry()
    def send(self, message: str, to: Recipient) -> None:
        if not isinstance(to, EmailRecipient):
            raise ValueError("Recipient must have an email")
        print(f"Sending email to {to.email}: {message}")


# Fails the first `failures` calls, then sends (to demo @Retry)
class FlakySmsSender(Sender):
    def __init__(self, failures: int) -> None:
        self.failures = failures

    @Logging
    @Retry(3)
    def send(self, message: str, to: Recipient) -> None:
        if self.failures > 0:
            self.failures -= 1
            raise ConnectionError("Network error")
        if not isinstance(to, PhoneRecipient):
            raise ValueError("Recipient must have a phone number")
        print(f"Sending SMS to {to.phone_number}: {message}")


# Client
def main() -> None:
    FlakySmsSender(2).send("Hello World!", PhoneRecipient(phone_number="+312323435345"))
    EmailSender().send("Hello World!", EmailRecipient(email="test@gmail.com"))


if __name__ == "__main__":
    main()
