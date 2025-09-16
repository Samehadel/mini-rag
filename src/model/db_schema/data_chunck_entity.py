from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class DataChunckEntity(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    chunck_business_entity_id: ObjectId
    chunck_metadata: dict
    chunck_text: str = Field(..., min_length=1)
    chunck_index: int = Field(..., ge=0)

    class Config():
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                'key': [
                    ('chunck_business_entity_id', 1)
                ],
                'name': 'chunck_business_entity_id_index_1',
                'unique': False
            }

        ]