from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class MatchResult(Base):
    __tablename__ = "match_results"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    match_status = Column(String, nullable=False)  # "Good Match", "Partial Match", "Poor Match"
    correction_suggestions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resume = relationship("Resume", back_populates="match_results")
    job_description = relationship("JobDescription", back_populates="match_results")
    skills = relationship("Skill", back_populates="match_result", cascade="all, delete-orphan")
    syllabus_items = relationship("Syllabus", back_populates="match_result", cascade="all, delete-orphan")
    interview_questions = relationship("InterviewQuestion", back_populates="match_result", cascade="all, delete-orphan")
    learning_resources = relationship("LearningResource", back_populates="match_result", cascade="all, delete-orphan")

