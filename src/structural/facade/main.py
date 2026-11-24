from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class NotificationT(Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"


# Recipients
@dataclass(frozen=True)
class Recipient:
    phone_number: str | None = None
    email: str | None = None


# Subsystem classes
class Sender(Protocol):
    def format_message(self, message: str) -> str:
        pass

    def send(self, message: str, to: Recipient) -> None:
        pass


class EmailSender(Sender):
    def format_message(self, message: str) -> str:
        return f"EMAIL: {message}"

    def send(self, message: str, to: Recipient) -> None:
        if to.email is None:
            raise ValueError("Invalid recipient type")
        print(f"Sending email to {to.email}: {message}")


class SmsSender(Sender):
    def format_message(self, message: str) -> str:
        return f"TEXT: {message}"

    def send(self, message: str, to: Recipient) -> None:
        if to.phone_number is None:
            raise ValueError("Invalid recipient type")
        print(f"Sending SMS to {to.phone_number}: {message}")


class WhatsappSender(Sender):
    def format_message(self, message: str) -> str:
        return f"Whatsapp: {message}"

    def send(self, message: str, to: Recipient) -> None:
        if to.phone_number is None:
            raise ValueError("Invalid recipient type")
        print(f"Sending Whatsapp to {to.phone_number}: {message}")


# Facade
class NotificationFacade:
    def __init__(self) -> None:
        self.senders: dict[NotificationT, Sender] = {
            NotificationT.EMAIL: EmailSender(),
            NotificationT.SMS: SmsSender(),
            NotificationT.WHATSAPP: WhatsappSender(),
        }

    def notify(self, notification_type: NotificationT, message: str, to: Recipient) -> None:
        sender = self.senders.get(notification_type)
        if sender is None:
            raise ValueError("Invalid notification type")
        sender.send(message=sender.format_message(message), to=to)


# Client
def main() -> None:
    notification = NotificationFacade()

    notification.notify(
        notification_type=NotificationT.EMAIL,
        message="Hello World!",
        to=Recipient(email="test@gmail.com"),
    )
    notification.notify(
        notification_type=NotificationT.SMS,
        message="Hello World!",
        to=Recipient(phone_number="+3232839239"),
    )
    notification.notify(
        notification_type=NotificationT.WHATSAPP,
        message="Hello World!",
        to=Recipient(phone_number="+3232839239"),
    )


if __name__ == "__main__":
    main()
