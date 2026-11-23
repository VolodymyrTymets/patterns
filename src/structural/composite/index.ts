type RecipientType = {
    email?: string;
    phone?: string;
};

// Component
interface ISender {
    send: (message: string, to: RecipientType) => void;
}
// Leaf
class EmailSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!to.email) {
            throw new Error('Recipient must have an email');
        }
        console.log(`Sending email to ${to.email}: ${message}`);
    }
}
class SmsSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!to.phone) {
            throw new Error('Recipient must have a phone number');
        }
        console.log(`Sending SMS to ${to.phone}: ${message}`);
    }
}
class WhatsappSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!to.phone) {
            throw new Error('Recipient must have a phone number');
        }
        console.log(`Sending Whatsapp to ${to.phone}: ${message}`);
    }
}
// Composite (Container)
class BroadcastSender implements ISender {
    private senders: ISender[] = [];
    add(sender: ISender): void {
        this.senders.push(sender);
    }
    remove(sender: ISender): void {
        const index = this.senders.indexOf(sender);
        if (index !== -1) {
            this.senders.splice(index, 1);
        }
    }
    send(message: string, to: RecipientType): void {
        this.senders.forEach((sender) => sender.send(message, to));
    }
}

// Client
const main = () => {
    const smsGroup = new BroadcastSender();
    smsGroup.add(new SmsSender());
    smsGroup.add(new WhatsappSender());

    const root = new BroadcastSender();
    root.add(new EmailSender());
    root.add(smsGroup); // a composite inside a composite

    root.send('Hello World!', {
        email: 'test@gmail.com',
        phone: '+312323435345',
    });
};
main();
