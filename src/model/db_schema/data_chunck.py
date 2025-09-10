from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional

class DataChunck(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    chunck_application_id: ObjectId
    chunck_metadata: dict
    chunck_text: str = Field(..., min_length=1)
    chunck_index: int = Field(..., ge=0)

    class Config():
        arbitrary_types_allowed = True