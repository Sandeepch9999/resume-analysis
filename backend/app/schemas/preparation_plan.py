from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PhaseTopicResponse(BaseModel):
    id: int
    topic_name: str
    description: Optional[str]
    practice_tasks: Optional[str]
    estimated_hours: Optional[float]
    order_index: int
    
    class Config:
        from_attributes = True

class PreparationPhaseResponse(BaseModel):
    id: int
    phase_number: int
    phase_name: str
    description: Optional[str]
    estimated_days: Optional[int]
    order_index: int
    topics: List[PhaseTopicResponse] = []
    
    class Config:
        from_attributes = True

class PreparationPlanResponse(BaseModel):
    id: int
    user_id: int
    job_description_id: Optional[int]
    match_result_id: Optional[int]
    title: str
    description: Optional[str]
    total_estimated_days: Optional[int]
    created_at: datetime
    phases: List[PreparationPhaseResponse] = []
    
    class Config:
        from_attributes = True

class JobPreparationPlanRequest(BaseModel):
    job_description_id: Optional[int] = None
    match_result_id: Optional[int] = None
    job_description_text: Optional[str] = None

