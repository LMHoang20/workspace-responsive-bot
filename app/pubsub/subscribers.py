from app.pubsub.__interface import Subscriber

def get_subscriber(name: str, *args, **kwargs) -> Subscriber:
    if name == 'pull':
        from app.pubsub.subscriber_pull import SubscriberPull
        return SubscriberPull(*args, **kwargs)
    elif name == 'push':
        from app.pubsub.subscriber_push import SubscriberPush
        return SubscriberPush(*args, **kwargs)
    else:
        raise ValueError(f'Unknown subscriber: {name}')
