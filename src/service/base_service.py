from helper.config import Settings, get_settings
import os

class BaseService:
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.upload_dir = os.path.join(self.base_dir, 'assets/files')