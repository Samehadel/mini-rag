from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class AssetEntity(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: Optional[int] = Field(ge=0, default=None)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config():
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                'key': [
                    ('project_id', 1)
                ],
                'name': 'asset_project_id_index_1',
                'unique': True
            },
            {
                'key': [
                    ('project_id', 1),
                    ('asset_name', 1)
                ],
                'name': 'asset_project_id_name_index_1',
                'unique': True
            }
        ]