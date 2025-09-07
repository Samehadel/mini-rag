import random
import string

class StringService():
    def __init__(self):
        pass

    def generate_random_string(self, length: int=15):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        