// Product: what the singleton stores
interface INotification {
    readonly recipient: string;
    readonly body: string;
}

interface INotificationService {
    send: (notification: INotification) => void;
    logAll: () => void;
}

// Singleton: one shared instance, reachable only through getInstance()
class NotificationService implements INotificationService {
    private static instance: NotificationService | undefined;
    private readonly notifications: INotification[] = [];

    // Private constructor: clients cannot call `new NotificationService()`
    private constructor() {}

    static getInstance(): NotificationService {
        // Lazy initialization: the instance is created on the first call only
        NotificationService.instance ??= new NotificationService();
        return NotificationService.instance;
    }

    private log(...args: unknown[]): void {
        console.log(`[${NotificationService.name}] `, ...args);
    }

    send(notification: INotification): void {
        this.notifications.push(notification);
        this.log(
            `Notification sent to ${notification.recipient}: ${notification.body}`,
        );
    }

    logAll(): void {
        for (const n of this.notifications) {
            this.log(n);
        }
    }
}

// Clients: independent parts of the app that share the same instance
class OrderModule {
    placeOrder(): void {
        NotificationService.getInstance().send({
            recipient: 'test@gmail.com',
            body: 'Order placed',
        });
    }
}
class AuthModule {
    signIn(): void {
        NotificationService.getInstance().send({
            recipient: 'test@gmail.com',
            body: 'Signed in',
        });
    }
}

const main = () => {
    new OrderModule().placeOrder();
    new AuthModule().signIn();
    // Both modules wrote into the same instance
    console.log(
        'same instance:',
        NotificationService.getInstance() === NotificationService.getInstance(),
    );
    NotificationService.getInstance().logAll();
};
main();
