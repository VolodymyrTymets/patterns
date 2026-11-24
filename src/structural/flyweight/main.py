import re
from enum import Enum

TemplateParams = dict[str, str]


class TemplateTypes(Enum):
    WELCOME = "welcome"
    RESET_PASSWORD = "reset-password"
    INTRO = "intro"
    GOODBYE = "goodbye"


# Flyweight (shared, immutable state: name, subject, body)
class NotificationTemplate:
    def __init__(self, name: str, subject: str, body: str) -> None:
        self._name = name
        self._subject = subject
        self._body = body

    # Extrinsic state (params) comes from the caller and is never stored
    def render_body(self, params: TemplateParams) -> str:
        return self._fill(self._body, params)

    def render_subject(self, params: TemplateParams) -> str:
        return self._fill(self._subject, params)

    def _fill(self, text: str, params: TemplateParams) -> str:
        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            if key not in params:
                raise ValueError(f"Missing param: {key}")
            return params[key]

        return re.sub(r"{(\w+)}", replace, text)


# Flyweight Factory
class TemplateFactory:
    def __init__(self) -> None:
        self._pool: dict[TemplateTypes, NotificationTemplate] = {}

    def get_template(self, name: TemplateTypes) -> NotificationTemplate:
        template = self._pool.get(name)
        if template is None:
            template = self._create_template(name)
            self._pool[name] = template
        return template

    @property
    def size(self) -> int:
        return len(self._pool)

    def _create_template(self, name: TemplateTypes) -> NotificationTemplate:
        match name:
            case TemplateTypes.WELCOME:
                return NotificationTemplate(
                    "welcome", "Welcome, {name}!", "Hi {name}, confirm here: {link}"
                )
            case TemplateTypes.RESET_PASSWORD:
                return NotificationTemplate(
                    "reset-password",
                    "Reset password, {name}!",
                    "Hi {name}, reset password here: {link}",
                )
            case TemplateTypes.INTRO:
                return NotificationTemplate("intro", "Intro, {name}!", "Hi {name}")
            case TemplateTypes.GOODBYE:
                return NotificationTemplate(
                    "goodbye", "Bye, {name}!", "Hi {name}, we hope you are back: {link}"
                )
            case _:
                raise ValueError("Invalid template name")


# Context (extrinsic state: to, params; shares a template)
class Notification:
    def __init__(self, template: NotificationTemplate, to: str, params: TemplateParams) -> None:
        self._template = template
        self._to = to
        self._params = params

    def get_recipient(self) -> str:
        return self._to

    def get_subject(self) -> str:
        return self._template.render_subject(self._params)

    def get_body(self) -> str:
        return self._template.render_body(self._params)


# Client
class Notifier:
    def __init__(self, template_factory: TemplateFactory) -> None:
        self._template_factory = template_factory
        self._notifications: list[Notification] = []

    def collect(self, template: TemplateTypes, to: str, params: TemplateParams) -> None:
        template_instance = self._template_factory.get_template(template)
        self._notifications.append(Notification(template_instance, to, params))

    def notify(self) -> None:
        for notification in self._notifications:
            subject = notification.get_subject()
            print(
                f'Sending "{subject}" to {notification.get_recipient()}: {notification.get_body()}'
            )
        print(
            f"{len(self._notifications)} notifications, "
            f"{self._template_factory.size} templates in the pool"
        )


def main() -> None:
    factory = TemplateFactory()
    notifier = Notifier(factory)
    notifier.collect(
        TemplateTypes.WELCOME,
        "john@example.com",
        {"name": "John", "link": "https://example.com/confirm/john"},
    )
    notifier.collect(
        TemplateTypes.WELCOME,
        "kate@example.com",
        {"name": "Kate", "link": "https://example.com/confirm/kate"},
    )
    notifier.collect(
        TemplateTypes.RESET_PASSWORD,
        "jane@example.com",
        {"name": "Jane", "link": "https://example.com/reset/jane"},
    )
    notifier.collect(TemplateTypes.INTRO, "bob@example.com", {"name": "Bob"})
    notifier.collect(
        TemplateTypes.GOODBYE,
        "alice@example.com",
        {"name": "Alice", "link": "https://example.com/return/alice"},
    )
    notifier.notify()
    print(
        "Same template instance:",
        factory.get_template(TemplateTypes.WELCOME) is factory.get_template(TemplateTypes.WELCOME),
    )


if __name__ == "__main__":
    main()
