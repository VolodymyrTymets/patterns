from dataclasses import dataclass
from typing import Protocol


# Target
@dataclass(frozen=True)
class PhoneRecipient:
    phone_number: str


@dataclass(frozen=True)
class EmailRecipient:
    email: str


class Sender(Protocol):
    def send(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        pass


# Client
class NotificationSender:
    def __init__(self, sender: Sender):
        self.sender = sender

    def send(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        self.sender.send(message=message, to=to)


# Adaptee
class ThirdPartySmsApi:
    def send_text(self, phone: str, message: str) -> None:
        print(f"Sending SMS: {message} to {phone}")


# Adapter
class SmsApiAdapter(Sender):
    def __init__(self, third_party_sms_api: ThirdPartySmsApi):
        self.third_party_sms_api = third_party_sms_api

    def send(self, message: str, to: PhoneRecipient | EmailRecipient) -> None:
        if not isinstance(to, PhoneRecipient):
            raise ValueError("Invalid recipient type")
        self.third_party_sms_api.send_text(to.phone_number, message)


def main() -> None:
    sms_sender = SmsApiAdapter(ThirdPartySmsApi())
    sender = NotificationSender(sms_sender)
    sender.send(message="Hello, world!", to=PhoneRecipient(phone_number="1234567890"))


if __name__ == "__main__":
    main()
