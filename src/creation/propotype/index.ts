// Prototype
interface INotification {
    readonly recipient: string;
    readonly body: string;
    clone: () => INotification;
}

interface IEmailNotification extends INotification {
    readonly subject: string;
}
type MetadataType = {
    readonly timestamp: Date;
};
interface ILogNotification extends IEmailNotification {
    readonly metadata: MetadataType;
}

// Concrete Prototype
// Every class implements clone() itself and returns its own type, so a copy keeps the concrete class
class Notification implements INotification {
    constructor(
        readonly recipient: string,
        readonly body: string,
    ) {}
    clone(): Notification {
        return new Notification(this.recipient, this.body);
    }
}
class SmsNotification extends Notification {
    clone(): SmsNotification {
        return new SmsNotification(this.recipient, this.body);
    }
}
class EmailNotification extends Notification implements IEmailNotification {
    constructor(
        recipient: string,
        body: string,
        readonly subject: string,
    ) {
        super(recipient, body);
    }
    clone(): EmailNotification {
        return new EmailNotification(this.recipient, this.body, this.subject);
    }
}
class LogNotification extends EmailNotification implements ILogNotification {
    readonly metadata: MetadataType;
    constructor(
        recipient: string,
        body: string,
        subject: string,
        metadata: MetadataType,
    ) {
        super(recipient, body, subject);
        // Date is mutable, so the copy gets its own instance and does not share it with the original
        this.metadata = { timestamp: new Date(metadata.timestamp) };
    }
    clone(): LogNotification {
        return new LogNotification(
            this.recipient,
            this.body,
            this.subject,
            this.metadata,
        );
    }
}

// Client: knows only INotification and creates new objects by cloning registered prototypes
class LogService {
    private readonly notifications: INotification[] = [];
    constructor(private readonly prototypes: Record<string, INotification>) {}

    create(name: string): INotification {
        const prototype = this.prototypes[name];
        if (!prototype) {
            throw new Error(`Unknown prototype: ${name}`);
        }
        const notification = prototype.clone();
        this.notifications.push(notification);
        return notification;
    }
    log(): void {
        for (const n of this.notifications) {
            console.log(n);
        }
    }
}

const main = () => {
    const recipient = 'test@gmail.com';
    const body = 'Hello World!';
    const logService = new LogService({
        sms: new SmsNotification(recipient, body),
        email: new EmailNotification(recipient, body, 'Greeting'),
        log: new LogNotification(recipient, body, 'Greeting', {
            timestamp: new Date(),
        }),
    });
    logService.create('log');
    logService.create('email');
    logService.create('sms');
    logService.create('log');
    logService.log();
};
main();
