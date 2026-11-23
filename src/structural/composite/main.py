from dataclasses import dataclass
from typing import Protocol


# Recipients
@dataclass(frozen=True)
class Recipient:
    phone_number: str | None = None
    email: str | None = None


# Component
class Sender(Protocol):
    def send(self, message: str, to: Recipient) -> None:
        pass


# Leaf
class EmailSender(Sender):
    def send(self, message: str, to: Recipient) -> None:
        if to.email is None:
            raise ValueError("Invalid recipient type")
        print(f"Sending email to {to.email}: {message}")


class SmsSender(Sender):
    def send(self, message: str, to: Recipient) -> None:
        if to.phone_number is None:
            raise ValueError("Invalid recipient type")
        print(f"Sending SMS to {to.phone_number}: {message}")


class WhatsappSender(Sender):
    def send(self, message: str, to: Recipient) -> None:
        if to.phone_number is None:
            raise ValueError("Invalid recipient type")
        print(f"Sending Whatsapp to {to.phone_number}: {message}")


# Composite (Container)
class BroadcastSender(Sender):
    def __init__(self) -> None:
        self.senders: list[Sender] = []

    def add(self, sender: Sender) -> None:
        self.senders.append(sender)

    def remove(self, sender: Sender) -> None:
        if sender in self.senders:
            self.senders.remove(sender)

    def send(self, message: str, to: Recipient) -> None:
        for sender in self.senders:
            sender.send(message=message, to=to)


# Client
def main() -> None:
    sms_group = BroadcastSender()
    sms_group.add(SmsSender())
    sms_group.add(WhatsappSender())

    root = BroadcastSender()
    root.add(EmailSender())
    root.add(sms_group)  # a composite inside a composite

    root.send(
        message="Hello World!",
        to=Recipient(phone_number="+312323435345", email="test@gmail.com"),
    )


if __name__ == "__main__":
    main()
