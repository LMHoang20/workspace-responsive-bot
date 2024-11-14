from app.pubsub.__interface import Publisher
from app.pubsub.publisher import WorkspacePublisher

def get_publisher(*args, **kwargs) -> Publisher:
    return WorkspacePublisher(*args, **kwargs)