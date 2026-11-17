from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Metadata:
    timestamp: datetime


# Prototype
class Notification(ABC):
    def __init__(self, recipient: str, body: str) -> None:
        self.recipient = recipient
        self.body = body

    @abstractmethod
    def clone(self) -> "Notification":
        pass

    def __str__(self) -> str:
        fields = ", ".join(f"{name}={value}" for name, value in vars(self).items())
        return f"{type(self).__name__}({fields})"


# Concrete Prototype
# Every class implements clone() itself and returns its own type, so a copy keeps the concrete class
class SMSNotification(Notification):
    def clone(self) -> "SMSNotification":
        return SMSNotification(self.recipient, self.body)


class EmailNotification(Notification):
    def __init__(self, recipient: str, body: str, subject: str) -> None:
        super().__init__(recipient, body)
        self.subject = subject

    def clone(self) -> "EmailNotification":
        return EmailNotification(self.recipient, self.body, self.subject)


class LogNotification(EmailNotification):
    def __init__(self, recipient: str, body: str, subject: str, metadata: Metadata) -> None:
        super().__init__(recipient, body, subject)
        # Metadata is frozen and datetime is immutable, so the copy can safely share it
        self.metadata = metadata

    def clone(self) -> "LogNotification":
        return LogNotification(self.recipient, self.body, self.subject, self.metadata)


# Client: knows only Notification and creates new objects by cloning registered prototypes
class LogService:
    def __init__(self, prototypes: dict[str, Notification]) -> None:
        self.prototypes = prototypes
        self.notifications: list[Notification] = []

    def create(self, name: str) -> Notification:
        if name not in self.prototypes:
            raise ValueError(f"Prototype {name} not found")
        notification = self.prototypes[name].clone()
        self.notifications.append(notification)
        return notification

    def log(self) -> None:
        for notification in self.notifications:
            print(notification)


def main() -> None:
    recipient = "test@gmail.com"
    body = "Hello World!"
    log_service = LogService(
        prototypes={
            "email": EmailNotification(recipient, body, "Greeting"),
            "sms": SMSNotification(recipient, body),
            "log": LogNotification(recipient, body, "Greeting", Metadata(datetime.now())),
        }
    )
    log_service.create("email")
    log_service.create("sms")
    first_log = log_service.create("log")
    second_log = log_service.create("log")
    log_service.log()
    print("clones are independent objects:", first_log is not second_log)


if __name__ == "__main__":
    main()
