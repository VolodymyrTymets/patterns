enum Role {
    admin = 'admin',
    guest = 'guest',
}
type RecipientType = {
    email?: string;
    phone?: string;
};
// Service Interface
interface ISender {
    send(message: string, to: RecipientType): void;
}
// Real Service
class EmailSender implements ISender {
    constructor() {
        // Expensive to create, so the proxy delays it until the first send
        console.log('Connecting to SMTP server...');
    }
    send(message: string, to: RecipientType): void {
        if (!to.email) {
            throw new Error('Recipient must have an email');
        }
        console.log(`Sending email to ${to.email}: ${message}`);
    }
}
// Proxy
class EmailSenderProxy implements ISender {
    private sender: ISender | null = null;
    constructor(private readonly role: Role) {}
    private checkAccess(): void {
        if (this.role !== Role.admin) {
            throw new Error(`Role '${this.role}' is not allowed to send`);
        }
    }
    send(message: string, to: RecipientType): void {
        this.checkAccess();
        // Lazy creation: the real sender is built on the first send only
        if (this.sender === null) {
            this.sender = new EmailSender();
        }
        this.sender.send(message, to);
    }
}
// Client
const main = () => {
    const adminSender = new EmailSenderProxy(Role.admin);
    console.log('Proxy created, nothing is connected yet');
    adminSender.send('Hello World!', { email: 'test@gmail.com' });
    adminSender.send('Hello again!', { email: 'test2@gmail.com' });

    const guestSender = new EmailSenderProxy(Role.guest);
    try {
        guestSender.send('Hello World!', { email: 'test@gmail.com' });
    } catch (error) {
        console.log(`Rejected: ${(error as Error).message}`);
    }
};
main();
