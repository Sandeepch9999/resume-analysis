from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResumeCreate(BaseModel):
    filename: str

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    extracted_text: Optional[str]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

