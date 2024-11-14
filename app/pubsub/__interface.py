class Subscriber:
    def __init__(self) -> None:
        raise NotImplementedError

    def start(self, callback):
        raise NotImplementedError


class Publisher:
    def __init__(self) -> None:
        raise NotImplementedError

    def start(self):
        raise NotImplementedError