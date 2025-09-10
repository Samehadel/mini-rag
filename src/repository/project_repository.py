from .base_repository import BaseRepository
from model.enums import CollectionNames
from model.db_schema import Project

class ProjectRepository(BaseRepository):
    def __init__(self, db_client):
        super().__init__(db_client, CollectionNames.COLLECTION_PROJECTS_NAME.value)
    

    async def save(self, project: Project):
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id
        
        return project

    async def find_by_application_id_or_create(self, application_id: str):
        self.logger.info(f"Finding project by application id: {application_id}")
        record = await self.collection.find_one({
            'application_id': application_id
        })

        if record is None:
            project = Project(application_id=application_id)
            project = await self.save(project)

            return project

        self.logger.info(f"Project found by application id: {application_id}")
        return Project(**record)


    async def find_all(self, page: int = 0, page_size: int = 10):
        total_document_count = await self.collection.count_documents({})
        
        total_pages = self.calculate_total_pages(total_document_count, page_size)
        
        cursor = self.collection.find(
            {},
            skip=page * page_size,
            limit=page_size
        )
        
        projects = []

        async for record in cursor:
            projects.append(
                Project(**record)
            )
            

        return projects, total_pages
        