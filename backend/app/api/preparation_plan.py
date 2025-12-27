from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.job_description import JobDescription
from app.models.match_result import MatchResult
from app.schemas.preparation_plan import (
    PreparationPlanResponse,
    JobPreparationPlanRequest
)
from app.services.preparation_plan_service import PreparationPlanService

router = APIRouter(prefix="/api/job-preparation-plan", tags=["job-preparation-plan"])

@router.post("/", response_model=PreparationPlanResponse, status_code=status.HTTP_201_CREATED)
def create_preparation_plan(
    request: JobPreparationPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job preparation plan."""
    jd_text = None
    missing_skills = None
    
    # Get job description text
    if request.job_description_id:
        jd = db.query(JobDescription).filter(
            JobDescription.id == request.job_description_id,
            JobDescription.user_id == current_user.id
        ).first()
        if not jd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job description not found"
            )
        jd_text = jd.description
    elif request.job_description_text:
        jd_text = request.job_description_text
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either job_description_id or job_description_text is required"
        )
    
    # Get missing skills from match result if available
    if request.match_result_id:
        match_result = db.query(MatchResult).join(JobDescription).filter(
            MatchResult.id == request.match_result_id,
            JobDescription.user_id == current_user.id
        ).first()
        if match_result:
            # Extract missing skills from match result
            from app.models.skill import Skill
            missing_skills_objs = db.query(Skill).filter(
                Skill.match_result_id == match_result.id,
                Skill.is_required == True,
                Skill.is_present == False
            ).all()
            missing_skills = [skill.skill_name for skill in missing_skills_objs]
    
    # Generate plan structure
    plan_data = PreparationPlanService.generate_plan_structure(jd_text, missing_skills)
    
    # Create plan in database
    plan = PreparationPlanService.create_plan(
        db=db,
        user_id=current_user.id,
        plan_data=plan_data,
        job_description_id=request.job_description_id,
        match_result_id=request.match_result_id
    )
    
    return plan

@router.get("/", response_model=List[PreparationPlanResponse])
def get_preparation_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all preparation plans for the current user."""
    plans = PreparationPlanService.get_user_plans(db, current_user.id)
    return plans

@router.get("/{plan_id}", response_model=PreparationPlanResponse)
def get_preparation_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific preparation plan by ID."""
    plan = PreparationPlanService.get_plan_by_id(db, plan_id, current_user.id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preparation plan not found"
        )
    return plan

