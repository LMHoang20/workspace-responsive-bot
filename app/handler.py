from app.translator.__interface import Translator
from app.pubsub.publisher import Publisher
from app.pubsub.subscriber_pull import Subscriber

from app.service.chat import Chat

class EventHandler:
    def __init__(self, translator: Translator, publisher: Publisher, subscriber: Subscriber) -> None:
        self.translator = translator
        self.publisher = publisher
        self.subscriber = subscriber

    def handle_event(self, event):
        match event.get('type', 'SPACE_MESSAGE'):
            case 'MESSAGE':
                self.handle_message(event)
            case 'SPACE_MESSAGE':
                self.handle_message(event)
            case 'ADDED_TO_SPACE':
                self.handle_added_to_space(event)
            case 'REMOVED_FROM_SPACE':
                self.handle_removed_from_space(event)
            case _:
                print(f'Unknown event type: {event}')

    def handle_message(self, event):
        if event['message']['sender']['type'] != 'HUMAN':
            return
        message = event.get('message', {})
        text = message.get('formattedText') or message.get('argumentText') or message.get('text')
        if not text:
            return
        print(f'Received message: {event}')
        translated = self.translator.translate(text)
        if translated == text:
            print(f'No need to translate: {text}')
            return
        response = Chat().send_message(
            text=translated,
            space_name=event['message']['space']['name'],
            thread_name=event['message']['thread']['name']
        )
        print(f'Sent message: {response}')

    def handle_added_to_space(self, event):
        space_id = event['space']['name'].split('/')[-1]
        self.publisher.added_to_space(space_id)
        print(f'Added to space: {space_id}')

    def handle_removed_from_space(self, event):
        space_id = event['space']['name'].split('/')[-1]
        self.publisher.removed_from_space(space_id)
        print(f'Removed from space: {space_id}')
