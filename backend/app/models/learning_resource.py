from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class LearningResource(Base):
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    match_result_id = Column(Integer, ForeignKey("match_results.id"), nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=True)
    resource_type = Column(String, nullable=True)  # "Article", "Video", "Course", "Documentation"
    description = Column(Text, nullable=True)
    
    match_result = relationship("MatchResult", back_populates="learning_resources")

