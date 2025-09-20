from .base_repository import BaseRepository
from model.enums import CollectionNames
from model.db_schema import AssetEntity

class AssetRepository(BaseRepository):
    def __init__(self, db_client):
        super().__init__(db_client, CollectionNames.COLLECTION_ASSET_NAME.value)
    
    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_indexes()
        
        return instance

    async def init_indexes(self):
        indexes = AssetEntity.get_indexes()
        for index in indexes:
            await self.collection.create_index(
                index['key'], 
                name=index['name'], 
                unique=index['unique']
            )
    
    async def save(self, asset: AssetEntity):
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id
        
        return asset

    async def find_by_project_id(self, project_id: str, type: str):
        self.logger.info(f"Finding assets by project id: {project_id}")
        records = self.collection.find({
            'project_id': project_id,
            'asset_type': type
        })

        return [
            AssetEntity(**record)
            async for record in records
        ]
