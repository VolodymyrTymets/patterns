import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


# Product
@dataclass(frozen=True)
class Notification:
    recipient: str
    subject: str
    body: str


# Builder
class NotificationBuilder(ABC):
    @abstractmethod
    def set_recipient(self, recipient: str) -> Self:
        pass

    @abstractmethod
    def set_subject(self, subject: str) -> Self:
        pass

    @abstractmethod
    def set_body(self, body: str) -> Self:
        pass

    @abstractmethod
    def build(self) -> Notification:
        pass

    @abstractmethod
    def reset(self) -> Self:
        pass


# Base builder: shared steps, only the recipient validation differs per variant
class BaseNotificationBuilder(NotificationBuilder):
    def __init__(self) -> None:
        self.recipient = ""
        self.subject = ""
        self.body = ""

    @abstractmethod
    def assert_recipient(self, recipient: str) -> None:
        pass

    def set_recipient(self, recipient: str) -> Self:
        self.assert_recipient(recipient)
        self.recipient = recipient
        return self

    def set_subject(self, subject: str) -> Self:
        self.subject = subject
        return self

    def set_body(self, body: str) -> Self:
        self.body = body
        return self

    def reset(self) -> Self:
        self.recipient = ""
        self.subject = ""
        self.body = ""
        return self

    def build(self) -> Notification:
        if not self.recipient:
            raise ValueError("Recipient is required")
        if not self.body:
            raise ValueError("Body is required")
        notification = Notification(recipient=self.recipient, subject=self.subject, body=self.body)
        # the builder is ready for the next product and never shares state with the one returned
        self.reset()
        return notification


# ConcreteBuilder
class EmailNotificationBuilder(BaseNotificationBuilder):
    def assert_recipient(self, recipient: str) -> None:
        if not recipient:
            raise ValueError("Recipient is required")
        if len(recipient) > 254:
            raise ValueError("Recipient must be at most 254 characters")
        if not re.fullmatch(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", recipient):
            raise ValueError("Invalid email address")


# ConcreteBuilder
class SMSNotificationBuilder(BaseNotificationBuilder):
    def assert_recipient(self, recipient: str) -> None:
        if not recipient:
            raise ValueError("Recipient is required")
        if not re.fullmatch(r"[0-9]+", recipient):
            raise ValueError("Recipient must contain digits only")
        if not 10 <= len(recipient) <= 11:
            raise ValueError("Recipient must be 10 or 11 digits long")


# Director
class NotificationDirector:
    def __init__(self, builder: NotificationBuilder) -> None:
        self.builder = builder

    def construct_notification(
        self, recipient: str, body: str, subject: str | None = None
    ) -> Notification:
        self.builder.reset().set_recipient(recipient)
        if subject:
            self.builder.set_subject(subject)
        return self.builder.set_body(body).build()


# Client
def main() -> None:
    email_notification = NotificationDirector(EmailNotificationBuilder()).construct_notification(
        recipient="test@gmail.com", body="Hello World!", subject="Greeting"
    )
    sms_notification = NotificationDirector(SMSNotificationBuilder()).construct_notification(
        recipient="1234567890", body="Hello World!"
    )
    print("email: ", email_notification)
    print("sms:", sms_notification)


if __name__ == "__main__":
    main()
