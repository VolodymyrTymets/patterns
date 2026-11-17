// Product
interface ISender {
    send: (message: string) => void;
}
interface IFormatter {
    format: (message: string) => string;
}

// Concrete products
class EmailSender implements ISender {
    send(message: string): void {
        console.log(`Sending email: ${message}`);
    }
}
class EmailFormatter implements IFormatter {
    format(message: string): string {
        return `Email format: ${message}`;
    }
}
// Concrete products
class SmsSender implements ISender {
    send(message: string): void {
        console.log(`Sending SMS: ${message}`);
    }
}
class SmsFormatter implements IFormatter {
    format(message: string): string {
        return `SMS format: ${message}`;
    }
}

//  AbstractFactory
interface INotificationFactory {
    createSender: () => ISender;
    createFormatter: () => IFormatter;
}

//  Concrete Factory
class EmailNotificationFactory implements INotificationFactory {
    createSender(): ISender {
        return new EmailSender();
    }
    createFormatter(): IFormatter {
        return new EmailFormatter();
    }
}

class SmsNotificationFactory implements INotificationFactory {
    createSender(): ISender {
        return new SmsSender();
    }
    createFormatter(): IFormatter {
        return new SmsFormatter();
    }
}

// Client
interface INotificationService {
    send: (message: string) => void;
}
class NotificationService implements INotificationService {
    private sender: ISender;
    private formatter: IFormatter;
    constructor(factory: INotificationFactory) {
        this.sender = factory.createSender();
        this.formatter = factory.createFormatter();
    }
    send(message: string): void {
        const formattedMessage = this.formatter.format(message);
        this.sender.send(formattedMessage);
    }
}

const main = () => {
    const services: INotificationService[] = [
        new NotificationService(new EmailNotificationFactory()),
        new NotificationService(new SmsNotificationFactory()),
    ];
    services.forEach((service) => service.send('Hello World!'));
};
main();
