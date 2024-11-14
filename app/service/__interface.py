from app.utility import SingletonMeta

class Service(metaclass=SingletonMeta):
    def __init__(self) -> None:
        raise NotImplementedError
    
