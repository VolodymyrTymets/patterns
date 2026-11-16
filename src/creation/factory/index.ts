// Product
interface ISender {
    send: (message: string) => void;
}

// Concrete products
class EmailSender implements ISender {
    send(message: string): void {
        console.log(`Sending email: ${message}`);
    }
}
// Concrete products
class SmsSender implements ISender {
    send(message: string): void {
        console.log(`Sending SMS: ${message}`);
    }
}

// Creator
abstract class Notification {
    protected abstract createSender(): ISender;

    send(message: string): void {
        const sender = this.createSender();
        sender.send(message);
    }
}
// Concrete creators
class EmailNotification extends Notification {
    protected createSender(): ISender {
        return new EmailSender();
    }
}

class SmsNotification extends Notification {
    protected createSender(): ISender {
        return new SmsSender();
    }
}


const main = () => {
    const sendes: Notification[] = [
        new EmailNotification(),
        new SmsNotification()
    ]
    sendes.forEach(sender => sender.send('Hello World!'));
}
main();