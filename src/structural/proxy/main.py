from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class Role(Enum):
    ADMIN = "admin"
    GUEST = "guest"


# Recipients
@dataclass(frozen=True)
class Recipient:
    phone_number: str | None = None
    email: str | None = None


# Service Interface
class Sender(Protocol):
    def send(self, message: str, to: Recipient) -> None:
        pass


# Real Service
class EmailSender(Sender):
    def __init__(self) -> None:
        # Expensive to create, so the proxy delays it until the first send
        print("Connecting to SMTP server...")

    def send(self, message: str, to: Recipient) -> None:
        if to.email is None:
            raise ValueError("Invalid recipient type")
        print(f"Sending email to {to.email}: {message}")


# Proxy
class EmailSenderProxy(Sender):
    def __init__(self, role: Role) -> None:
        self._role = role
        self._sender: Sender | None = None

    def _check_access(self) -> None:
        if self._role is not Role.ADMIN:
            raise PermissionError(f"Role '{self._role.value}' is not allowed to send")

    def send(self, message: str, to: Recipient) -> None:
        self._check_access()
        # Lazy creation: the real sender is built on the first send only
        if self._sender is None:
            self._sender = EmailSender()
        self._sender.send(message=message, to=to)


# Client
def main() -> None:
    admin_sender = EmailSenderProxy(Role.ADMIN)
    print("Proxy created, nothing is connected yet")
    admin_sender.send(message="Hello World!", to=Recipient(email="test@gmail.com"))
    admin_sender.send(message="Hello again!", to=Recipient(email="test2@gmail.com"))

    guest_sender = EmailSenderProxy(Role.GUEST)
    try:
        guest_sender.send(message="Hello World!", to=Recipient(email="test@gmail.com"))
    except PermissionError as error:
        print(f"Rejected: {error}")


if __name__ == "__main__":
    main()
