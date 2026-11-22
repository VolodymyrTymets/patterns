// Target
type RecipientType =
    | {
          email: string;
      }
    | {
          phone: string;
      };
interface ISender {
    send: (message: string, to: RecipientType) => void;
}

// Client
class NotificationSender {
    constructor(private readonly sender: ISender) {}
    send(message: string, to: RecipientType): void {
        this.sender.send(message, to);
    }
}
// Adaptee
class ThirdPartySmsApi {
    sendText(phone: string, message: string): void {
        console.log(`Sending SMS: ${message} to ${phone}`);
    }
}
// Adapter
class SmsApiAdapter implements ISender {
    constructor(private readonly api: ThirdPartySmsApi) {}
    send(message: string, to: RecipientType): void {
        if (!('phone' in to)) {
            throw new Error('Recipient must have a phone number');
        }
        this.api.sendText(to.phone, message);
    }
}

const main = () => {
    const smsSender = new SmsApiAdapter(new ThirdPartySmsApi());
    const sender = new NotificationSender(smsSender);
    sender.send('Hello World!', { phone: '1234567890' });
};
main();
