from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.models.user import User
from ml.resume_parser import ResumeParser
import os
import aiofiles
from pathlib import Path

class ResumeService:
    UPLOAD_DIR = Path("uploads/resumes")
    
    def __init__(self):
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    async def save_resume(self, db: Session, user_id: int, filename: str, file_content: bytes) -> Resume:
        """Save resume file and extract text."""
        # Generate unique filename
        file_path = self.UPLOAD_DIR / f"{user_id}_{filename}"
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Extract text
        parser = ResumeParser()
        extracted_text = parser.extract_text(file_content, filename)
        
        # Save to database
        resume = Resume(
            user_id=user_id,
            filename=filename,
            file_path=str(file_path),
            extracted_text=extracted_text
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return resume
    
    def get_user_resumes(self, db: Session, user_id: int) -> list[Resume]:
        """Get all resumes for a user."""
        return db.query(Resume).filter(Resume.user_id == user_id).all()
    
    def get_resume_by_id(self, db: Session, resume_id: int, user_id: int) -> Resume:
        """Get resume by ID (with user ownership check)."""
        return db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()

