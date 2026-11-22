type RecipientType =
    | {
          email: string;
      }
    | {
          phone: string;
      };

// Abstraction
class Notification {
    constructor(private readonly sender: ISender) {}
    notify(message: string, to: RecipientType): void {
        this.sender.send(message, to);
    }
}

// Refined Abstraction
class AlertNotification extends Notification {
    private formatMessage(message: string): string {
        return `Alert: ${message}`;
    }
    notify(message: string, to: RecipientType) {
        super.notify(this.formatMessage(message), to);
    }
}

class ReminderNotification extends Notification {
    private formatMessage(message: string): string {
        return `Reminder: ${message}`;
    }
    notify(message: string, to: RecipientType) {
        super.notify(this.formatMessage(message), to);
    }
}

// Implementor
interface ISender {
    send: (message: string, to: RecipientType) => void;
}
// Concrete Implementor
class EmailSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!('email' in to)) {
            throw new Error('Recipient must have an email');
        }
        console.log(`Sending email to ${to.email}: ${message}`);
    }
}
class SmsSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!('phone' in to)) {
            throw new Error('Recipient must have a phone number');
        }
        console.log(`Sending SMS to ${to.phone}: ${message}`);
    }
}
// Client
const main = () => {
    const alert = new AlertNotification(new EmailSender());
    alert.notify('Hello World!', { email: 'test@gmail.com' });

    const reminder = new ReminderNotification(new SmsSender());
    reminder.notify('Hello World!', { phone: '1234567890' });
};
main();
