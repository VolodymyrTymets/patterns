// Decorator pattern with the native TypeScript `@` syntax (TC39 decorators, TS 5+).
// Here a decorator wraps a method of the Component instead of wrapping the object.
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

type SendMethod = (message: string, to: RecipientType) => void;

// Concrete Decorators (method decorators)
function Logging(target: SendMethod): SendMethod {
    return function (this: unknown, message, to) {
        console.log(`Logging: ${message}`);
        target.call(this, message, to);
    };
}

// Decorator factory: takes its own parameter, returns the decorator
function Retry(maxAttempts: number = 3) {
    return function (target: SendMethod): SendMethod {
        return function (this: unknown, message, to) {
            for (let attempt = 1; attempt <= maxAttempts; attempt++) {
                try {
                    target.call(this, message, to);
                    return;
                } catch (error) {
                    console.log(`Attempt ${attempt}/${maxAttempts} failed`);
                    if (attempt === maxAttempts) {
                        throw error;
                    }
                }
            }
        };
    };
}

// Concrete Components (decorators are applied bottom-up: Retry first, then Logging)
class EmailSender implements ISender {
    @Logging
    @Retry()
    send(message: string, to: RecipientType): void {
        if (!('email' in to)) {
            throw new Error('Recipient must have an email');
        }
        console.log(`Sending email to ${to.email}: ${message}`);
    }
}

// Fails the first `failures` calls, then sends (to demo @Retry)
class FlakySmsSender implements ISender {
    constructor(private failures: number) {}

    @Logging
    @Retry(3)
    send(message: string, to: RecipientType): void {
        if (this.failures > 0) {
            this.failures--;
            throw new Error('Network error');
        }
        if (!('phone' in to)) {
            throw new Error('Recipient must have a phone number');
        }
        console.log(`Sending SMS to ${to.phone}: ${message}`);
    }
}

// Client
const main = () => {
    new FlakySmsSender(2).send('Hello World!', { phone: '+312323435345' });
    new EmailSender().send('Hello World!', { email: 'test@gmail.com' });
};
main();
