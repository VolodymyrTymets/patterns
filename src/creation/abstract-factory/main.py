from abc import abstractmethod, ABC
from typing import List, Protocol

# Abstract products
class Sender(Protocol):
    def send(self, message: str) -> None:
        pass
class Formatter(Protocol):
    def format(self, message: str) -> str:
        pass

# Concrete products
class EmailSender(Sender):
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")
class EmailFormatter(Formatter):
    def format(self, message: str) -> str:
        return f"Email format: {message}"

# Concrete products
class SmsSender(Sender):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")
class SmsFormatter(Formatter):
    def format(self, message: str) -> str:
        return f"SMS format: {message}"

# AbstractFactory
class NotificationFactory(ABC):
    @abstractmethod
    def create_sender(self) -> Sender:
        pass
    @abstractmethod
    def create_formatter(self) -> Formatter:
        pass

# Concrete factories
class EmailNotificationFactory(NotificationFactory):
    def create_sender(self) -> Sender:
        return EmailSender()
    def create_formatter(self) -> Formatter:
        return EmailFormatter()

class SmsNotificationFactory(NotificationFactory):
    def create_sender(self) -> Sender:
        return SmsSender()
    def create_formatter(self) -> Formatter:
        return SmsFormatter()

class Notification(Protocol):
    def send(self, message: str) -> None:
        pass

# Client
class NotificationService(Notification):
    def __init__(self, factory: NotificationFactory):
        self.sender = factory.create_sender()
        self.formatter = factory.create_formatter()

    def send(self, message: str) -> None:
        formatted_message = self.formatter.format(message)
        self.sender.send(formatted_message)


def main() -> None:
    services: List[Notification] = [
        NotificationService(EmailNotificationFactory()),
        NotificationService(SmsNotificationFactory())
    ]
    for service in services:
        service.send(message="Hello World!")

if __name__ == '__main__':
    main()
