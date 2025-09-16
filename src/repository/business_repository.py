from .base_repository import BaseRepository
from model.enums import CollectionNames
from model.db_schema import BusinessEntity

class BusinessRepository(BaseRepository):
    def __init__(self, db_client):
        super().__init__(db_client, CollectionNames.COLLECTION_BUSINESS_NAME.value)
    
    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_indexes()
        
        return instance

    async def init_indexes(self):
        indexes = BusinessEntity.get_indexes()
        for index in indexes:
            await self.collection.create_index(
                index['key'], 
                name=index['name'], 
                unique=index['unique']
            )
    
    async def save(self, business: BusinessEntity):
        result = await self.collection.insert_one(business.dict(by_alias=True, exclude_unset=True))
        business.id = result.inserted_id
        
        return business

    async def find_by_project_id_or_create(self, project_id: str):
        self.logger.info(f"Finding business by project id: {project_id}")
        record = await self.collection.find_one({
            'project_id': project_id
        })

        if record is None:
            business_entity = BusinessEntity(project_id=project_id)
            business_entity = await self.save(business_entity)

            return business_entity

        self.logger.info(f"Business found by project id: {project_id}")
        return BusinessEntity(**record)


    async def find_all(self, page: int = 0, page_size: int = 10):
        total_document_count = await self.collection.count_documents({})
        
        total_pages = self.calculate_total_pages(total_document_count, page_size)
        
        cursor = self.collection.find(
            {},
            skip=page * page_size,
            limit=page_size
        )
        
        businesses = []

        async for record in cursor:
            businesses.append(
                BusinessEntity(**record)
            )
            

        return businesses, total_pages
        