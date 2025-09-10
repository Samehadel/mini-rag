from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    application_id: str

    @validator("application_id")
    def validate(cls, value):
        if not value.isalnum():
            raise ValueError("application_id must be alphanumeric")
        return value

    class Config(): 
        arbitrary_types_allowed = True
