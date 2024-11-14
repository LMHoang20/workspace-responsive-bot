from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest

from app.credential.credential import CredentialStore
from app.service.__interface import Service

class Workspace(Service):
    def __init__(self) -> None:
        self.client = build(
            'workspaceevents',
            'v1',
            credentials=CredentialStore().get_client_secrets(),
        )
    
    def __call__(cls):
        return cls.client
    
    def listen(self, space_id, event_types, topic_id):
        try:
            response: HttpRequest = self.client.subscriptions().create(body={
                'target_resource': get_target_resource(space_id),
                'event_types': event_types,
                'notification_endpoint': {'pubsub_topic': get_topic_name(topic_id)},
                'payload_options': {'include_resource': True},
            }).execute()
            subscription_name = response['response']['name']
            print(f'Listening to {space_id}: {subscription_name}')
            return subscription_name
        except HttpError as e:
            if e.reason != 'Subscription associated with the resource already exists.':
                raise e
            response = self.renew(e.error_details[0]['metadata']['current_subscription'])
            subscription_name = response['response']['name']
            print(f'Renew to {space_id}: {subscription_name}')
            return subscription_name
    
    def renew(self, subscription_id) -> HttpRequest:
        return self.client.subscriptions().patch(
            name=subscription_id,
            updateMask='ttl',
            body={
                'ttl': {'seconds': 0},
            }
        ).execute()

    def unlisten(self, subscription_name):
        self.client.subscriptions().delete(name=subscription_name).execute()
        print(f'Unlistening from {subscription_name}')

    def list_listened_spaces(self, event_types):
        FILTER = f' OR '.join([f'event_types:"{event_type}"' for event_type in event_types])
        response = self.client.subscriptions().list(filter=FILTER).execute()
        spaces = response.get('subscriptions', [])
        if response.get('nextPageToken'):
            response = self.client.subscriptions().list(
                pageToken=response['nextPageToken'],
                filter=FILTER
            ).execute()
            spaces += response.get('subscriptions', [])
        return spaces

def get_topic_name(topic_id):
    project_id = CredentialStore().get_project_id()
    return f"projects/{project_id}/topics/{topic_id}"

def get_target_resource(space_id):
    return '//chat.googleapis.com/spaces/' + space_id

if __name__ == '__main__':
    listened_spaces = Workspace().list_listened_spaces()
