from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobDescriptionCreate(BaseModel):
    title: str
    company: Optional[str] = None
    description: str

class JobDescriptionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    company: Optional[str]
    description: str
    created_at: datetime
    
    class Config:
        from_attributes = True

