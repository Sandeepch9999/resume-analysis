from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Syllabus(Base):
    __tablename__ = "syllabus"
    
    id = Column(Integer, primary_key=True, index=True)
    match_result_id = Column(Integer, ForeignKey("match_results.id"), nullable=False)
    topic = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, nullable=True)  # "High", "Medium", "Low"
    
    match_result = relationship("MatchResult", back_populates="syllabus_items")

