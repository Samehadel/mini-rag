from .base_service import BaseService
import os
from .string_service import StringService
import re

class ProjectService(BaseService):
    def __init__(self):
        super().__init__()
        self.string_service = StringService()

    def build_file_dir(self, application_id: str, file_name: str):
        project_dir = os.path.join(
            self.upload_dir, application_id
        )
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        file_name = self.generate_unique_file_name(file_name)
        return os.path.join(project_dir, file_name)


    def generate_unique_file_name(self, file_name: str):
        cleaned_file_name = self.get_clean_file_name(file_name)
        random_string = self.string_service.generate_random_string()

        # make sure file name is unique
        while os.path.exists(os.path.join(self.upload_dir, f"{random_string}_{cleaned_file_name}")):
            random_string = self.string_service.generate_random_string()
        
        return f"{random_string}_{cleaned_file_name}"

    def get_clean_file_name(self, file_name: str):
        # remove special characters except underscore and space
        cleaned_file_name = re.sub(r'[^\w.]', '', file_name.strip())

        # replace space with underscore
        cleaned_file_name = cleaned_file_name.replace(' ', '_')
        
        return cleaned_file_name
        
    