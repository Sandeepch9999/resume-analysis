from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.match_result import MatchAnalysisRequest, MatchResultResponse
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

@router.post("/analyze", response_model=MatchResultResponse, status_code=status.HTTP_201_CREATED)
def analyze_resume_jd(
    request: MatchAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze resume against job description."""
    try:
        service = AnalysisService()
        match_result = service.analyze_resume_jd_match(
            db, request.resume_id, request.job_description_id, current_user.id
        )
        return match_result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/results", response_model=List[MatchResultResponse])
def get_match_results(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all match results for the current user."""
    service = AnalysisService()
    results = service.get_match_results(db, current_user.id)
    return results

@router.get("/results/{result_id}", response_model=MatchResultResponse)
def get_match_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific match result by ID."""
    service = AnalysisService()
    result = service.get_match_result_by_id(db, result_id, current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match result not found"
        )
    return result

