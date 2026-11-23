type RecipientType =
    | {
          email: string;
      }
    | {
          phone: string;
      };
// Component
interface ISender {
    send: (message: string, to: RecipientType) => void;
}
// Concrete Component
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
class WhatsappSender implements ISender {
    send(message: string, to: RecipientType): void {
        if (!('phone' in to)) {
            throw new Error('Recipient must have a phone number');
        }
        console.log(`Sending Whatsapp to ${to.phone}: ${message}`);
    }
}
// Fails the first `failures` calls, then behaves like SmsSender (to demo RetrySender)
class FlakySmsSender extends SmsSender {
    constructor(private failures: number) {
        super();
    }
    send(message: string, to: RecipientType): void {
        if (this.failures > 0) {
            this.failures--;
            throw new Error('Network error');
        }
        super.send(message, to);
    }
}
// Base Decorator
class SenderDecorator implements ISender {
    protected readonly sender: ISender;
    constructor(sender: ISender) {
        this.sender = sender;
    }
    send(message: string, to: RecipientType): void {
        this.sender.send(message, to);
    }
}
// Concrete Decorator
class LoggingSender extends SenderDecorator {
    send(message: string, to: RecipientType): void {
        console.log(`Logging: ${message}`);
        super.send(message, to);
    }
}
class RetrySender extends SenderDecorator {
    constructor(
        sender: ISender,
        private readonly maxAttempts: number = 3,
    ) {
        super(sender);
    }
    send(message: string, to: RecipientType): void {
        for (let attempt = 1; attempt <= this.maxAttempts; attempt++) {
            try {
                super.send(message, to);
                return;
            } catch (error) {
                console.log(`Attempt ${attempt}/${this.maxAttempts} failed`);
                if (attempt === this.maxAttempts) {
                    throw error;
                }
            }
        }
    }
}

// Client
const main = () => {
    // Two decorators stacked around a sender that fails twice before it works
    const sms = new LoggingSender(new RetrySender(new FlakySmsSender(2), 3));
    sms.send('Hello World!', { phone: '+312323435345' });

    // The same decorator reused around a different sender
    const email = new RetrySender(new EmailSender());
    email.send('Hello World!', { email: 'test@gmail.com' });

    // Stacking order is free: here logging is wrapped by the retry, not the other way round
    const whatsapp = new RetrySender(
        new LoggingSender(new WhatsappSender()),
        2,
    );
    whatsapp.send('Hello World!', { phone: '+312323435345' });
};
main();
