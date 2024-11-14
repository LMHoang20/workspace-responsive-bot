from app.pubsub.__interface import Publisher

from app.service.chat import Chat
from app.service.workspace import Workspace

class WorkspacePublisher(Publisher):
    def __init__(self, topic_id, event_types) -> None:
        self.topic_id = topic_id
        self.event_types = event_types
        
    def start(self):
        self.space_subscription_map = {}

        joined_spaces: list = Chat().list_joined_spaces()
        listened_spaces = Workspace().list_listened_spaces(self.event_types)
        
        for subscription in listened_spaces:
            space_id = subscription['targetResource'].split('/')[-1]
            if space_id not in [space['name'].split('/')[-1] for space in joined_spaces]:
                Workspace().unlisten(subscription['name'])
            
        for space in joined_spaces:
            space_id = space['name'].split('/')[-1]
            subscription_name = Workspace().listen(space_id, self.event_types, self.topic_id)
            self.space_subscription_map[space_id] = subscription_name

    def added_to_space(self, space_id):
        subscription_name = Workspace().listen(space_id, self.event_types, self.topic_id)
        self.space_subscription_map[space_id] = subscription_name

    def removed_from_space(self, space_id):
        subscription_name = self.space_subscription_map[space_id]
        Workspace().unlisten(subscription_name)
        self.space_subscription_map.pop(space_id)
    
