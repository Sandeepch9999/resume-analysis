from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SkillResponse(BaseModel):
    id: int
    skill_name: str
    is_present: bool
    is_required: bool
    
    class Config:
        from_attributes = True

class SyllabusResponse(BaseModel):
    id: int
    topic: str
    description: Optional[str]
    priority: Optional[str]
    
    class Config:
        from_attributes = True

class InterviewQuestionResponse(BaseModel):
    id: int
    question: str
    category: Optional[str]
    
    class Config:
        from_attributes = True

class LearningResourceResponse(BaseModel):
    id: int
    title: str
    url: Optional[str]
    resource_type: Optional[str]
    description: Optional[str]
    
    class Config:
        from_attributes = True

class MatchResultResponse(BaseModel):
    id: int
    resume_id: int
    job_description_id: int
    similarity_score: float
    match_status: str
    correction_suggestions: Optional[str]
    created_at: datetime
    skills: List[SkillResponse] = []
    syllabus_items: List[SyllabusResponse] = []
    interview_questions: List[InterviewQuestionResponse] = []
    learning_resources: List[LearningResourceResponse] = []
    
    class Config:
        from_attributes = True

class MatchAnalysisRequest(BaseModel):
    resume_id: int
    job_description_id: int

