from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    match_result_id = Column(Integer, ForeignKey("match_results.id"), nullable=False)
    question = Column(Text, nullable=False)
    category = Column(String, nullable=True)  # "Technical", "Behavioral", "System Design"
    
    match_result = relationship("MatchResult", back_populates="interview_questions")

