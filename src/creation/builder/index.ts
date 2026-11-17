// Product
interface INotification {
    readonly recipient: string;
    readonly subject: string;
    readonly body: string;
}
// Builder
interface INotificationBuilder {
    setRecipient: (recipient: string) => this;
    setSubject: (subject: string) => this;
    setBody: (body: string) => this;
    build: () => INotification;
    reset: () => this;
}

// Base builder: shared steps, only the recipient validation differs per variant
abstract class NotificationBuilder implements INotificationBuilder {
    private recipient = '';
    private subject = '';
    private body = '';

    protected abstract assertRecipient(recipient: string): void;

    setRecipient(recipient: string): this {
        this.assertRecipient(recipient);
        this.recipient = recipient;
        return this;
    }
    setSubject(subject: string): this {
        this.subject = subject;
        return this;
    }
    setBody(body: string): this {
        this.body = body;
        return this;
    }
    reset(): this {
        this.recipient = '';
        this.subject = '';
        this.body = '';
        return this;
    }
    build(): INotification {
        if (!this.recipient) {
            throw new Error('Recipient is required');
        }
        if (!this.body) {
            throw new Error('Body is required');
        }
        const notification: INotification = {
            recipient: this.recipient,
            subject: this.subject,
            body: this.body
        };
        // the builder is ready for the next product and never shares state with the one returned
        this.reset();
        return notification;
    }
}

// ConcreteBuilder
class EmailNotificationBuilder extends NotificationBuilder {
    protected assertRecipient(recipient: string): void {
        if (!recipient) {
            throw new Error('Recipient is required');
        }
        if (recipient.length > 254) {
            throw new Error('Recipient must be at most 254 characters');
        }
        if (!/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(recipient)) {
            throw new Error('Invalid email address');
        }
    }
}
class SmsNotificationBuilder extends NotificationBuilder {
    protected assertRecipient(recipient: string): void {
        if (!recipient) {
            throw new Error('Recipient is required');
        }
        if (!/^[0-9]+$/.test(recipient)) {
            throw new Error('Recipient must contain digits only');
        }
        if (recipient.length < 10 || recipient.length > 11) {
            throw new Error('Recipient must be 10 or 11 digits long');
        }
    }
}

// Director
class NotificationDirector {
    private builder: INotificationBuilder;
    constructor(builder: INotificationBuilder) {
        this.builder = builder;
    }
    constructNotification(recipient: string, body: string, subject?: string): INotification {
        this.builder.reset().setRecipient(recipient);
        if (subject) {
            this.builder.setSubject(subject);
        }
        return this.builder.setBody(body).build();
    }
}
// Client
const main = () => {
    const emailNotification = new NotificationDirector(new EmailNotificationBuilder()).constructNotification('test@gmail.com', 'Hello World!', 'Greeting');
    const smsNotification = new NotificationDirector(new SmsNotificationBuilder()).constructNotification('1234567890', 'Hello World!');
    console.log('email: ', emailNotification, 'sms: ', smsNotification, '');
}
main();
