from dataclasses import dataclass
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


# Concrete Component
class EmailSender(Sender):
    def send(self, message: str, to: Recipient) -> None:
        if not isinstance(to, EmailRecipient):
            raise ValueError("Recipient must have an email")
        print(f"Sending email to {to.email}: {message}")


class SmsSender(Sender):
    def send(self, message: str, to: Recipient) -> None:
        if not isinstance(to, PhoneRecipient):
            raise ValueError("Recipient must have a phone number")
        print(f"Sending SMS to {to.phone_number}: {message}")


class WhatsappSender(Sender):
    def send(self, message: str, to: Recipient) -> None:
        if not isinstance(to, PhoneRecipient):
            raise ValueError("Recipient must have a phone number")
        print(f"Sending Whatsapp to {to.phone_number}: {message}")


# Fails the first `failures` calls, then behaves like SmsSender (to demo RetrySender)
class FlakySmsSender(SmsSender):
    def __init__(self, failures: int) -> None:
        self.failures = failures

    def send(self, message: str, to: Recipient) -> None:
        if self.failures > 0:
            self.failures -= 1
            raise ConnectionError("Network error")
        super().send(message, to)


# Base Decorator
class SenderDecorator(Sender):
    def __init__(self, sender: Sender) -> None:
        self.sender = sender

    def send(self, message: str, to: Recipient) -> None:
        self.sender.send(message, to)


# Concrete Decorator
class LoggingSender(SenderDecorator):
    def send(self, message: str, to: Recipient) -> None:
        print(f"Logging: {message}")
        super().send(message, to)


class RetrySender(SenderDecorator):
    def __init__(self, sender: Sender, max_attempts: int = 3) -> None:
        super().__init__(sender)
        self.max_attempts = max_attempts

    def send(self, message: str, to: Recipient) -> None:
        for attempt in range(1, self.max_attempts + 1):
            try:
                super().send(message, to)
                return
            except Exception:
                print(f"Attempt {attempt}/{self.max_attempts} failed")
                if attempt == self.max_attempts:
                    raise


# Client
def main() -> None:
    # Two decorators stacked around a sender that fails twice before it works
    sms = LoggingSender(RetrySender(FlakySmsSender(2), 3))
    sms.send("Hello World!", PhoneRecipient(phone_number="+312323435345"))

    # The same decorator reused around a different sender
    email = RetrySender(EmailSender())
    email.send("Hello World!", EmailRecipient(email="test@gmail.com"))

    # Stacking order is free: here logging is wrapped by the retry, not the other way round
    whatsapp = RetrySender(LoggingSender(WhatsappSender()), 2)
    whatsapp.send("Hello World!", PhoneRecipient(phone_number="+312323435345"))


if __name__ == "__main__":
    main()
