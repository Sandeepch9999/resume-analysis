from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class PreparationPlan(Base):
    __tablename__ = "preparation_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=True)
    match_result_id = Column(Integer, ForeignKey("match_results.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    total_estimated_days = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    phases = relationship("PreparationPhase", back_populates="plan", cascade="all, delete-orphan")

class PreparationPhase(Base):
    __tablename__ = "preparation_phases"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("preparation_plans.id"), nullable=False)
    phase_number = Column(Integer, nullable=False)
    phase_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    estimated_days = Column(Integer, nullable=True)
    order_index = Column(Integer, nullable=False)
    
    plan = relationship("PreparationPlan", back_populates="phases")
    topics = relationship("PhaseTopic", back_populates="phase", cascade="all, delete-orphan")

class PhaseTopic(Base):
    __tablename__ = "phase_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    phase_id = Column(Integer, ForeignKey("preparation_phases.id"), nullable=False)
    topic_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    practice_tasks = Column(Text, nullable=True)
    estimated_hours = Column(Float, nullable=True)
    order_index = Column(Integer, nullable=False)
    
    phase = relationship("PreparationPhase", back_populates="topics")

