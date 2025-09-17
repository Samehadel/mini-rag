from model.db_schema.data_chunck_entity import DataChunckEntity
from .base_repository import BaseRepository
from bson.objectid import ObjectId
from model import DataChunckEntity
from model.enums import CollectionNames
from pymongo import InsertOne 

class ChunckRepository(BaseRepository):
    def __init__(self, db_client):
        super().__init__(db_client, CollectionNames.COLLECTION_DATA_CHUNKS_NAME.value)

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_indexes()
        
        return instance

    async def init_indexes(self):
        indexes = DataChunckEntity.get_indexes()
        for index in indexes:
            await self.collection.create_index(
                index['key'], 
                name=index['name'], 
                unique=index['unique']
            )
    
    async def save(self, chunck: DataChunckEntity):
        result = await self.collection.insert_one(chunck.dict(by_alias=True, exclude_unset=True))
        chunck.id = result.inserted_id
        
        return chunck

    async def saveall(self, chuncks: list, batch_size: int = 100):
        for i in range(0, len(chuncks), batch_size):
            batch = chuncks[i:i + batch_size]
            
            operations = [
                InsertOne(chunck.dict(by_alias=True, exclude_unset=True)) 
                for chunck in batch
            ]

            await self.collection.bulk_write(operations)
        
        return len(chuncks)

    async def get_chunck(self, chunck_id: str):
        objectId = ObjectId(chunck_id)
        
        record = self.collection.find_one({
            '_id': objectId
        })

        if record is None:
            return None
        
        return DataChunck(**record)

    async def find_all(self, application_id: str, page: int = 0, page_size: int = 10):
        application_id_object = ObjectId(application_id)
        
        total_document_count = await self.collection.count_documents({
            'chunck_project_id': application_id_object
        })
        
        total_pages = self.calculate_total_pages(total_document_count, page_size)
        cursor = self.collection.find(
            {
                'chunck_project_id': application_id_object
            },
            skip=page * page_size,
            limit=page_size
        )
        
        chuncks = []
        async for record in cursor:
            chuncks.append(
                DataChunckEntity(**record)
            )
            
        return chuncks, total_pages

    async def delete_chuncks_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({
            'chunck_project_id': project_id
        })
        self.logger.info(f"Deleted {result.deleted_count} chuncks for project id: {project_id}")
        return result.deleted_count