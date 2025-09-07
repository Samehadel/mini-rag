from .BaseController import BaseController
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def build_project_dir(self, application_id: str):
        project_dir = os.path.join(
            self.upload_dir, application_id
        )
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        
        return project_dir
        
    