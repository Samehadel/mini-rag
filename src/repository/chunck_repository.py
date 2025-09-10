from .base_repository import BaseRepository
from bson.objectid import ObjectId
from model.db_schema import DataChunck
from model.enums import CollectionNames
from pymongo import InsertOne 

class ChunckRepository(BaseRepository):
    def __init__(self, db_client):
        super().__init__(db_client, CollectionNames.COLLECTION_DATA_CHUNKS_NAME.value)

    async def save(self, chunck: DataChunck):
        result = await self.collection.insert_one(chunck.dict(by_alias=True, exclude_unset=True))
        chunck.id = result.inserted_id
        
        return chunck

    async def saveall(self, chuncks: list, batch_size: int = 100):

        for i in range(0, len(chuncks), batch_size):
            batch = chuncks[i:i + batch_size]
            
            operations = [
                InsertOne(chunck.dict()) 
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
            'chunck_application_id': application_id_object
        })
        
        total_pages = self.calculate_total_pages(total_document_count, page_size)
        cursor = self.collection.find(
            {
                'chunck_application_id': application_id_object
            },
            skip=page * page_size,
            limit=page_size
        )
        
        chuncks = []
        async for record in cursor:
            chuncks.append(
                DataChunck(**record)
            )
            
        return chuncks, total_pages