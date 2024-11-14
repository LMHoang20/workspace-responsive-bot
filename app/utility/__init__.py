import threading
import random

from functools import wraps

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def synchronized(func):
    lock = threading.Lock()  # Lock object to synchronize access
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    
    return wrapper

def extract_text(a, b):
    prefix_len = 0
    while prefix_len < len(a) and prefix_len < len(b) and a[prefix_len] == b[prefix_len]:
        prefix_len += 1
    
    suffix_len = 0
    while suffix_len < len(a) - prefix_len and suffix_len < len(b) - prefix_len and a[-(suffix_len + 1)] == b[-(suffix_len + 1)]:
        suffix_len += 1

    return a[prefix_len:len(a) - suffix_len]

def unique_string():
    no_char = 6
    random_number = random.randint(0, 10**no_char)
    random_number = str(random_number).zfill(no_char)
    return f"\0{random_number}\0"