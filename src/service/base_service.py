from helper.config import Settings, get_settings
import os

class BaseService:
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.upload_dir = os.path.join(self.base_dir, 'assets/files')
        self.vector_db_dir = os.path.join(self.base_dir, 'assets/database')

    def get_database_path(self, db_name: str):

        database_path = os.path.join(
            self.vector_db_dir, 
            db_name
        )

        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path
        