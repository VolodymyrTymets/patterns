type RecipientType = {
    email?: string;
    phone?: string;
};
enum NotificationT {
    email = 'email',
    sms = 'sms',
    whatsapp = 'whatsapp',
}
// Subsystem classes
interface ISender {
    formatMessage(message: string): string;
    send(message: string, to: RecipientType): void;
}
class EmailSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!to.email) {
            throw new Error('Recipient must have an email');
        }
        console.log(`Sending email to ${to.email}: ${message}`);
    }
    formatMessage(message: string): string {
        return `EMAIL: ${message}`;
    }
}
class SmsSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!to.phone) {
            throw new Error('Recipient must have a phone number');
        }
        console.log(`Sending SMS to ${to.phone}: ${message}`);
    }
    formatMessage(message: string): string {
        return `TEXT: ${message}`;
    }
}
class WhatsappSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!to.phone) {
            throw new Error('Recipient must have a phone number');
        }
        console.log(`Sending Whatsapp to ${to.phone}: ${message}`);
    }
    formatMessage(message: string): string {
        return `Whatsapp: ${message}`;
    }
}
// Facade
class NotificationFacade {
    private senders: Record<NotificationT, ISender>;
    constructor() {
        this.senders = {
            [NotificationT.email]: new EmailSender(),
            [NotificationT.sms]: new SmsSender(),
            [NotificationT.whatsapp]: new WhatsappSender(),
        };
    }
    notify(
        notificationType: NotificationT,
        message: string,
        to: RecipientType,
    ): void {
        const sender = this.senders[notificationType];
        if (!sender) {
            throw new Error('Invalid notification type');
        }
        sender.send(sender.formatMessage(message), to);
    }
}

// Client
const main = () => {
    const notification = new NotificationFacade();

    notification.notify(NotificationT.email, 'Hello World!', {
        email: 'test@gmail.com',
    });
    notification.notify(NotificationT.sms, 'Hello World!', {
        phone: '+3232839239',
    });
    notification.notify(NotificationT.whatsapp, 'Hello World!', {
        phone: '+3232839239',
    });
};
main();
