from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    match_result_id = Column(Integer, ForeignKey("match_results.id"), nullable=False)
    skill_name = Column(String, nullable=False)
    is_present = Column(Boolean, default=False)
    is_required = Column(Boolean, default=True)
    
    match_result = relationship("MatchResult", back_populates="skills")

