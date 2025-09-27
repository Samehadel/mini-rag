from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    project_id: str
    chunck_size: Optional[int] = 200
    overlap_size: Optional[int] = 20
    do_reset: Optional[bool] = False