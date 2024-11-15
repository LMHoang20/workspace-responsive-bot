import json

from app.pubsub.publishers import get_publisher
from app.pubsub.subscribers import get_subscriber
from app.translator.translators import get_translator

from app.config import USING_MODEL, SUBSCRIPTION_TYPE, SUBSCRIPTION_ID, TOPIC_ID, EVENT_TYPES
from app.handler import EventHandler
from app.utility import synchronized

@synchronized
def callback(message, handler: EventHandler):
    print(message)
    try:
        message_data = message.data.decode("utf-8")
        event = json.loads(message_data)
    except Exception as e:
        print(f'Bad Request: {e}')
        message.nack()

    message.ack()
    try:
        handler.handle_event(event)
    except Exception as e:
        print(f'Error: {e}')

def main():
    translator = get_translator(USING_MODEL)
    subscriber = get_subscriber(SUBSCRIPTION_TYPE, SUBSCRIPTION_ID)
    publisher = get_publisher(TOPIC_ID, EVENT_TYPES)

    handler = EventHandler(translator, publisher, subscriber)
    publisher.start()
    subscriber.start(lambda message: callback(message, handler))

if __name__ == '__main__':
    main()
