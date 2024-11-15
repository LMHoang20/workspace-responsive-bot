from app.pubsub.__interface import Publisher


def get_publisher(*args, **kwargs) -> Publisher:
    from app.pubsub.publisher import WorkspacePublisher
    return WorkspacePublisher(*args, **kwargs)
