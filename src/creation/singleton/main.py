from dataclasses import dataclass
from typing import Protocol, Self


@dataclass(frozen=True)
class Notification:
    recipient: str
    body: str


class NotificationServiceProtocol(Protocol):
    def send(self, notification: Notification) -> None:
        pass

    def log_all(self) -> None:
        pass


# Singleton: one shared instance, returned every time the class is called
class NotificationService(NotificationServiceProtocol):
    _instance: Self | None = None
    notifications: list[Notification]

    def __new__(cls):
        # Lazy initialization: the instance is created on the first call only
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.notifications = []
        return cls._instance

    def _log(self, *args, **kwargs) -> None:
        print(f"[{NotificationService.__name__}] ", *args, **kwargs)

    def send(self, notification: Notification) -> None:
        self.notifications.append(notification)
        self._log(f"Notification sent to {notification.recipient}: {notification.body}")

    def log_all(self) -> None:
        for notification in self.notifications:
            self._log(notification)


# Clients: independent parts of the app that share the same instance
class OrderModule:
    def place_order(self) -> None:
        NotificationService().send(Notification("test@gmail.com", "Order placed"))


class AuthModule:
    def sign_in(self) -> None:
        NotificationService().send(Notification("test@gmail.com", "Signed in"))


def main() -> None:
    OrderModule().place_order()
    AuthModule().sign_in()
    # Both modules wrote into the same instance
    print("same instance:", NotificationService() is NotificationService())
    NotificationService().log_all()


if __name__ == "__main__":
    main()
