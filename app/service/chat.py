from googleapiclient.discovery import build

from app.credential.credential import CredentialStore

from app.service.__interface import Service

class Chat(Service):
    def __init__(self):
        self.client = build(
            'chat',
            'v1',
            credentials=CredentialStore().get_service_account(),
        )
    
    def __call__(cls):
        return cls.client

    def list_joined_spaces(self):
        spaceTypes = ['GROUP_CHAT', 'SPACE']
        filter = ' OR '.join([f'spaceType = "{spaceType}"' for spaceType in spaceTypes])
        response = self.client.spaces().list(filter=filter).execute()
        spaces = response.get('spaces', [])
        if response.get('nextPageToken'):
            response = self.client.spaces().list(
                pageToken=response['nextPageToken'],
                filter=filter
            ).execute()
            spaces += response.get('spaces', [])
        return spaces
    
    def get_space(self, space_id):
        space_name = f'spaces/{space_id}'
        return self.client.spaces().get(name=space_name).execute()
    
    def send_message(self, text, space_name, thread_name):
        body = {
            'text': text,
            'thread': {
                'name': thread_name
            },
            'threadReply': True
        }

        # Send the translated text back to the chat
        return self.client.spaces().messages().create(
            parent=space_name,
            threadKey=thread_name,
            messageReplyOption='REPLY_MESSAGE_OR_FAIL',
            body=body
        ).execute()
    
if __name__ == '__main__':
    print(Chat().list_joined_spaces())
    