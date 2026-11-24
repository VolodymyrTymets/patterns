type TemplateParams = Record<string, string>;
enum TemplateTypes {
    welcome = 'welcome',
    resetPassword = 'reset-password',
    intro = 'intro',
    goodbye = 'goodbye',
}
// Flyweight (shared, immutable state: name, subject, body)
class NotificationTemplate {
    readonly name: string;
    readonly subject: string;
    readonly body: string;
    constructor(name: string, subject: string, body: string) {
        this.name = name;
        this.subject = subject;
        this.body = body;
    }
    // Extrinsic state (params) comes from the caller and is never stored
    renderBody(params: TemplateParams): string {
        return this.fill(this.body, params);
    }
    renderSubject(params: TemplateParams): string {
        return this.fill(this.subject, params);
    }
    private fill(text: string, params: TemplateParams): string {
        return text.replace(/{(\w+)}/g, (_, key: string) => {
            if (!(key in params)) {
                throw new Error(`Missing param: ${key}`);
            }
            return params[key];
        });
    }
}
// Flyweight Factory
class TemplateFactory {
    private pool = new Map<TemplateTypes, NotificationTemplate>();
    getTemplate(name: TemplateTypes): NotificationTemplate {
        let template = this.pool.get(name);
        if (!template) {
            template = this.createTemplate(name);
            this.pool.set(name, template);
        }
        return template;
    }
    get size(): number {
        return this.pool.size;
    }
    private createTemplate(name: TemplateTypes): NotificationTemplate {
        switch (name) {
            case TemplateTypes.welcome:
                return new NotificationTemplate(
                    'welcome',
                    'Welcome, {name}!',
                    'Hi {name}, confirm here: {link}',
                );
            case TemplateTypes.resetPassword:
                return new NotificationTemplate(
                    'reset-password',
                    'Reset password, {name}!',
                    'Hi {name}, reset password here: {link}',
                );
            case TemplateTypes.intro:
                return new NotificationTemplate(
                    'intro',
                    'Intro, {name}!',
                    'Hi {name}',
                );
            case TemplateTypes.goodbye:
                return new NotificationTemplate(
                    'goodbye',
                    'Bye, {name}!',
                    'Hi {name}, we hope you are back: {link}',
                );
            default:
                throw new Error('Invalid template name');
        }
    }
}
// Context (extrinsic state: to, params; shares a template)
class Notification {
    private readonly template: NotificationTemplate;
    private readonly to: string;
    private readonly params: TemplateParams;
    constructor(
        template: NotificationTemplate,
        to: string,
        params: TemplateParams,
    ) {
        this.template = template;
        this.to = to;
        this.params = params;
    }
    getRecipient(): string {
        return this.to;
    }
    getSubject(): string {
        return this.template.renderSubject(this.params);
    }
    getBody(): string {
        return this.template.renderBody(this.params);
    }
}
// Client
class Notifier {
    private readonly notifications: Notification[] = [];
    constructor(private readonly templateFactory: TemplateFactory) {}
    collect(template: TemplateTypes, to: string, params: TemplateParams): void {
        const templateInstance = this.templateFactory.getTemplate(template);
        this.notifications.push(new Notification(templateInstance, to, params));
    }
    notify(): void {
        for (const notification of this.notifications) {
            console.log(
                `Sending "${notification.getSubject()}" to ${notification.getRecipient()}: ${notification.getBody()}`,
            );
        }
        console.log(
            `${this.notifications.length} notifications, ${this.templateFactory.size} templates in the pool`,
        );
    }
}

const main = () => {
    const factory = new TemplateFactory();
    const notifier = new Notifier(factory);
    notifier.collect(TemplateTypes.welcome, 'john@example.com', {
        name: 'John',
        link: 'https://example.com/confirm/john',
    });
    notifier.collect(TemplateTypes.welcome, 'kate@example.com', {
        name: 'Kate',
        link: 'https://example.com/confirm/kate',
    });
    notifier.collect(TemplateTypes.resetPassword, 'jane@example.com', {
        name: 'Jane',
        link: 'https://example.com/reset/jane',
    });
    notifier.collect(TemplateTypes.intro, 'bob@example.com', {
        name: 'Bob',
    });
    notifier.collect(TemplateTypes.goodbye, 'alice@example.com', {
        name: 'Alice',
        link: 'https://example.com/return/alice',
    });
    notifier.notify();
    console.log(
        'Same template instance:',
        factory.getTemplate(TemplateTypes.welcome) ===
            factory.getTemplate(TemplateTypes.welcome),
    );
};
main();
