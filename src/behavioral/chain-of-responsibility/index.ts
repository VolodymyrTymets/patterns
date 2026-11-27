// Recipients
type Recipient = {
    phoneNumber?: string;
    email?: string;
    hasWhatsapp?: boolean;
};

// Handler Interface
interface ISender {
    send(message: string, to: Recipient): void;
    setNext(sender: ISender): void;
}

// Base Handler
abstract class BaseHandler implements ISender {
    private nextHandler: ISender | null = null;

    setNext(sender: ISender): void {
        this.nextHandler = sender;
    }

    send(message: string, to: Recipient): void {
        if (this.nextHandler !== null) {
            this.nextHandler.send(message, to);
        } else {
            console.log(
                `No handler could send the message to ${JSON.stringify(to)}: ${message}`,
            );
        }
    }
}

// Concrete Handlers
class EmailSender extends BaseHandler {
    send(message: string, to: Recipient): void {
        if (to.email) {
            console.log(`Sending email to ${to.email}: ${message}`);
        } else {
            super.send(message, to);
        }
    }
}

class SmsSender extends BaseHandler {
    send(message: string, to: Recipient): void {
        if (to.phoneNumber) {
            console.log(`Sending SMS to ${to.phoneNumber}: ${message}`);
        } else {
            super.send(message, to);
        }
    }
}

class WhatsappSender extends BaseHandler {
    send(message: string, to: Recipient): void {
        if (to.hasWhatsapp && to.phoneNumber) {
            console.log(`Sending Whatsapp to ${to.phoneNumber}: ${message}`);
        } else {
            super.send(message, to);
        }
    }
}

// Client
class NotificationService {
    private readonly sender: ISender = new EmailSender();

    constructor() {
        const waSender = new WhatsappSender();
        const smsSender = new SmsSender();
        waSender.setNext(smsSender);
        this.sender.setNext(waSender);
    }

    sendNotification(message: string, to: Recipient): void {
        this.sender.send(message, to);
    }
}

const main = () => {
    const service = new NotificationService();
    const recipients: Record<string, Recipient> = {
        'Email only': { email: 'test@gmail.com' },
        'Phone only': { phoneNumber: '+380000000000' },
        'Email and phone': {
            email: 'test@gmail.com',
            phoneNumber: '+380000000000',
        },
        'Phone with WhatsApp': {
            phoneNumber: '+380000000000',
            hasWhatsapp: true,
        },
        'No contacts': {},
    };
    for (const [name, recipient] of Object.entries(recipients)) {
        console.log(`--- ${name}`);
        service.sendNotification('Hello World!', recipient);
    }
};
main();
