from google.cloud import pubsub_v1

from app.pubsub.__interface import Subscriber
from app.credential.credential import CredentialStore

class SubscriberPull(Subscriber):
    def __init__(self, subscription_id) -> None:
        self.client = pubsub_v1.SubscriberClient()
        
        self.subscription_path = self.client.subscription_path(
            CredentialStore().get_project_id(), 
            subscription_id
        )
        
    def start(self, callback):    
        streaming_pull_future = self.client.subscribe(
            self.subscription_path, 
            callback=callback
        )
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
    
if __name__ == '__main__':
    from publisher import WorkspacePublisher
    from app.config import TOPIC_ID, EVENT_TYPES, SUBSCRIPTION_ID

    pub = WorkspacePublisher(TOPIC_ID, EVENT_TYPES)
    pub.start()

    def callback(message):
        message.ack()
        data = message.data.decode("utf-8")
        print(f"Received message: {data}")

    sub = SubscriberPull(SUBSCRIPTION_ID)
    sub.start(callback)
