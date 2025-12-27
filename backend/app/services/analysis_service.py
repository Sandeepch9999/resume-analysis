from sqlalchemy.orm import Session
from app.models.match_result import MatchResult
from app.models.skill import Skill
from app.models.syllabus import Syllabus
from app.models.interview_question import InterviewQuestion
from app.models.learning_resource import LearningResource
from app.models.resume import Resume
from app.models.job_description import JobDescription
from ml.matcher import ResumeMatcher
from ml.job_preparation import JobPreparationGenerator

class AnalysisService:
    def __init__(self):
        self.matcher = ResumeMatcher()
        self.preparation_generator = JobPreparationGenerator()
    
    def analyze_resume_jd_match(self, db: Session, resume_id: int, job_description_id: int, user_id: int) -> MatchResult:
        """Perform complete analysis of resume vs job description."""
        # Get resume and JD
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
        jd = db.query(JobDescription).filter(JobDescription.id == job_description_id, JobDescription.user_id == user_id).first()
        
        if not resume or not jd:
            raise ValueError("Resume or Job Description not found")
        
        if not resume.extracted_text:
            raise ValueError("Resume text not extracted")
        
        # Perform matching analysis
        analysis = self.matcher.analyze_match(resume.extracted_text, jd.description)
        
        # Create match result
        match_result = MatchResult(
            resume_id=resume_id,
            job_description_id=job_description_id,
            similarity_score=analysis['similarity_score'],
            match_status=analysis['match_status'],
            correction_suggestions=analysis['correction_suggestions']
        )
        db.add(match_result)
        db.flush()
        
        # Add skills
        all_jd_skills = set(analysis['jd_skills'])
        present_skills_set = set(analysis['present_skills'])
        missing_skills_set = set(analysis['missing_skills'])
        
        for skill_name in all_jd_skills:
            is_present = skill_name in present_skills_set
            skill = Skill(
                match_result_id=match_result.id,
                skill_name=skill_name,
                is_present=is_present,
                is_required=True
            )
            db.add(skill)
        
        # Generate and add syllabus
        syllabus_items = self.preparation_generator.generate_syllabus(
            analysis['jd_skills'],
            analysis['missing_skills']
        )
        for item in syllabus_items:
            syllabus = Syllabus(
                match_result_id=match_result.id,
                topic=item['topic'],
                description=item['description'],
                priority=item['priority']
            )
            db.add(syllabus)
        
        # Generate and add interview questions
        interview_questions = self.preparation_generator.generate_interview_questions(analysis['jd_skills'])
        for q in interview_questions:
            question = InterviewQuestion(
                match_result_id=match_result.id,
                question=q['question'],
                category=q['category']
            )
            db.add(question)
        
        # Generate and add learning resources
        learning_resources = self.preparation_generator.generate_learning_resources(
            analysis['jd_skills'],
            analysis['missing_skills']
        )
        for resource in learning_resources:
            lr = LearningResource(
                match_result_id=match_result.id,
                title=resource['title'],
                url=resource.get('url'),
                resource_type=resource.get('type'),
                description=resource.get('description')
            )
            db.add(lr)
        
        db.commit()
        db.refresh(match_result)
        
        return match_result
    
    def get_match_results(self, db: Session, user_id: int) -> list[MatchResult]:
        """Get all match results for a user."""
        return db.query(MatchResult).join(Resume).filter(Resume.user_id == user_id).all()
    
    def get_match_result_by_id(self, db: Session, match_result_id: int, user_id: int) -> MatchResult:
        """Get match result by ID (with user ownership check)."""
        return db.query(MatchResult).join(Resume).filter(
            MatchResult.id == match_result_id,
            Resume.user_id == user_id
        ).first()

