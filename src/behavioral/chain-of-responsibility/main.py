from dataclasses import dataclass
from typing import Protocol, Self


# Recipients
@dataclass(frozen=True)
class Recipient:
    phone_number: str | None = None
    email: str | None = None
    has_whatsapp: bool = False


# Handler Interface
class Sender(Protocol):
    def send(self, message: str, to: Recipient) -> None:
        pass

    def set_next(self, sender: Self):
        pass


# Base Handler
class BaseHandler(Sender):
    next_handler: Sender | None = None

    def set_next(self, sender: Self):
        self.next_handler = sender

    def send(self, message: str, to: Recipient) -> None:
        if self.next_handler is not None:
            self.next_handler.send(message, to)
        else:
            print(f"No handler could send the message to {to}: {message}")


# Concrete Handlers
class EmailSender(BaseHandler):
    def send(self, message: str, to: Recipient) -> None:
        if to.email:
            print(f"Sending email to {to.email}: {message}")
        else:
            super().send(message, to)


class SmsSender(BaseHandler):
    def send(self, message: str, to: Recipient) -> None:
        if to.phone_number:
            print(f"Sending SMS to {to.phone_number}: {message}")
        else:
            super().send(message, to)


class WhatsappSender(BaseHandler):
    def send(self, message: str, to: Recipient) -> None:
        if to.has_whatsapp and to.phone_number:
            print(f"Sending Whatsapp to {to.phone_number}: {message}")
        else:
            super().send(message, to)


# Client
class NotificationService:
    def __init__(self) -> None:
        self.sender = EmailSender()
        wa_sender = WhatsappSender()
        sms_sender = SmsSender()
        wa_sender.set_next(sms_sender)
        self.sender.set_next(wa_sender)

    def send_notification(self, message: str, to: Recipient) -> None:
        self.sender.send(message, to)


def main() -> None:
    service = NotificationService()
    recipients = {
        "Email only": Recipient(email="test@gmail.com"),
        "Phone only": Recipient(phone_number="+380000000000"),
        "Email and phone": Recipient(email="test@gmail.com", phone_number="+380000000000"),
        "Phone with WhatsApp": Recipient(phone_number="+380000000000", has_whatsapp=True),
        "No contacts": Recipient(),
    }
    for case, recipient in recipients.items():
        print(f"--- {case}")
        service.send_notification("Hello World!", recipient)


if __name__ == "__main__":
    main()
