from dataclasses import dataclass
from typing import Protocol


# Recipients
@dataclass(frozen=True)
class PhoneRecipient:
    phone_number: str


@dataclass(frozen=True)
class EmailRecipient:
    email: str


# Implementor
class Sender(Protocol):
    def send(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        pass


# Abstraction
class Notification:
    def __init__(self, sender: Sender):
        self.sender = sender

    def notify(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        self.sender.send(message=message, to=to)


# Refined Abstraction
class AlertNotification(Notification):
    def format_message(self, message: str) -> str:
        return f"ALERT: {message}"

    def notify(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        message = self.format_message(message)
        super().notify(message=message, to=to)


class ReminderNotification(Notification):
    def format_message(self, message: str) -> str:
        return f"REMINDER: {message}"

    def notify(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        message = self.format_message(message)
        super().notify(message=message, to=to)


# Concrete Implementor
class EmailSender(Sender):
    def send(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        if not isinstance(to, EmailRecipient):
            raise ValueError("Invalid recipient type")
        print(f"Sending email to {to.email}: {message}")


class SmsSender(Sender):
    def send(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        if not isinstance(to, PhoneRecipient):
            raise ValueError("Invalid recipient type")
        print(f"Sending SMS to {to.phone_number}: {message}")


# Client
def main() -> None:
    email = EmailRecipient(email="test@gmail.com")
    phone = PhoneRecipient(phone_number="1234567890")

    AlertNotification(sender=EmailSender()).notify(message="Hello World!", to=email)
    AlertNotification(sender=SmsSender()).notify(message="Hello World!", to=phone)
    ReminderNotification(sender=EmailSender()).notify(message="Hello World!", to=email)
    ReminderNotification(sender=SmsSender()).notify(message="Hello World!", to=phone)


if __name__ == "__main__":
    main()
