from abc import abstractmethod, ABC
from typing import List, Protocol

# Product
class Sender(Protocol):
    def send(self, message: str) -> None:
        pass
# Concrete products
class EmailSender(Sender):
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")
# Concrete products
class SMSSender(Sender):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")

# Creator
class Notification(ABC):
    @abstractmethod
    def create_sender(self) -> Sender:
        pass

    def send(self, message: str) -> None:
        sender = self.create_sender()
        sender.send(message=message)

# Concrete creator
class EmailNotification(Notification):
    def create_sender(self) -> Sender:
        return EmailSender()
# Concrete creator
class SMSNotification(Notification):
    def create_sender(self) -> Sender:
        return SMSSender()

def main():
    senders: List[Notification] = [
        EmailNotification(),
        SMSNotification()
    ]
    for sender in senders:
        sender.send(message="Hello, world!")

if __name__ == '__main__':
    main()