from app.pubsub.__interface import Subscriber
from app.pubsub.subscriber_pull import SubscriberPull
from app.pubsub.subscriber_push import SubscriberPush

def get_subscriber(name: str, *args, **kwargs) -> Subscriber:
    if name == 'pull':
        return SubscriberPull(*args, **kwargs)
    elif name == 'push':
        return SubscriberPush(*args, **kwargs)
    else:
        raise ValueError(f'Unknown subscriber: {name}')