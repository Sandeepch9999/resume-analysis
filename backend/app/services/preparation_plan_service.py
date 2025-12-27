from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from app.models.preparation_plan import PreparationPlan, PreparationPhase, PhaseTopic
from app.models.user import User
from app.models.job_description import JobDescription
from app.models.match_result import MatchResult
from ml.skill_extractor import SkillExtractor
from ml.job_preparation import JobPreparationGenerator

class PreparationPlanService:
    """Service to generate structured job preparation plans."""
    
    # Skill to learning path mapping
    SKILL_LEARNING_PATHS = {
        'python': {
            'fundamentals': ['Python syntax', 'Data types', 'Control flow', 'Functions', 'Modules'],
            'core': ['OOP', 'File handling', 'Error handling', 'Libraries (pandas, numpy)', 'APIs'],
            'advanced': ['Design patterns', 'Async programming', 'Testing', 'Performance optimization'],
            'practice': ['Build REST API', 'Data analysis project', 'Web scraping', 'Code review']
        },
        'javascript': {
            'fundamentals': ['JS basics', 'DOM manipulation', 'Events', 'Functions', 'Arrays'],
            'core': ['ES6+ features', 'Async/await', 'Promises', 'Modules', 'APIs'],
            'advanced': ['React/Vue/Angular', 'State management', 'Testing', 'Build tools'],
            'practice': ['Build SPA', 'API integration', 'Component library', 'Portfolio project']
        },
        'java': {
            'fundamentals': ['Java basics', 'OOP concepts', 'Collections', 'Exceptions', 'I/O'],
            'core': ['Spring Framework', 'Spring Boot', 'REST APIs', 'Database integration', 'Maven/Gradle'],
            'advanced': ['Microservices', 'Cloud deployment', 'Security', 'Performance tuning'],
            'practice': ['Build REST service', 'Microservice project', 'Database design', 'Deployment']
        },
        'react': {
            'fundamentals': ['React basics', 'Components', 'Props', 'State', 'JSX'],
            'core': ['Hooks', 'Context API', 'Routing', 'Forms', 'API calls'],
            'advanced': ['State management (Redux)', 'Testing', 'Performance', 'SSR/Next.js'],
            'practice': ['Build portfolio', 'E-commerce app', 'Dashboard', 'Component library']
        },
        'aws': {
            'fundamentals': ['Cloud basics', 'AWS console', 'EC2', 'S3', 'IAM'],
            'core': ['VPC', 'RDS', 'Lambda', 'API Gateway', 'CloudFormation'],
            'advanced': ['Architecture patterns', 'Security best practices', 'Cost optimization', 'DevOps'],
            'practice': ['Deploy app to AWS', 'Set up CI/CD', 'Multi-tier architecture', 'Monitoring']
        },
        'docker': {
            'fundamentals': ['Docker basics', 'Images', 'Containers', 'Dockerfile', 'Docker commands'],
            'core': ['Docker Compose', 'Networking', 'Volumes', 'Multi-stage builds'],
            'advanced': ['Kubernetes basics', 'Orchestration', 'Production deployment', 'Security'],
            'practice': ['Containerize app', 'Multi-container setup', 'CI/CD integration', 'Production setup']
        },
        'machine learning': {
            'fundamentals': ['ML basics', 'Data preprocessing', 'Supervised learning', 'Evaluation metrics'],
            'core': ['Feature engineering', 'Model selection', 'Hyperparameter tuning', 'Libraries (sklearn, pandas)'],
            'advanced': ['Deep learning', 'Neural networks', 'Model deployment', 'MLOps'],
            'practice': ['Kaggle competition', 'End-to-end project', 'Model deployment', 'Portfolio']
        }
    }
    
    @staticmethod
    def extract_skills_from_jd(jd_text: str) -> List[str]:
        """Extract skills from job description."""
        return list(SkillExtractor.extract_skills_from_jd(jd_text))
    
    @staticmethod
    def generate_plan_structure(jd_text: str, missing_skills: Optional[List[str]] = None) -> Dict:
        """Generate structured preparation plan."""
        # Extract skills
        jd_skills = PreparationPlanService.extract_skills_from_jd(jd_text)
        
        # Determine missing skills
        if missing_skills is None:
            missing_skills = jd_skills  # If not provided, assume all JD skills need learning
        
        # Get primary skills (top 5)
        primary_skills = missing_skills[:5] if missing_skills else jd_skills[:5]
        
        # Generate phases
        phases = []
        
        # Phase 1: Fundamentals
        fundamentals_topics = []
        for skill in primary_skills:
            skill_lower = skill.lower()
            if skill_lower in PreparationPlanService.SKILL_LEARNING_PATHS:
                topics = PreparationPlanService.SKILL_LEARNING_PATHS[skill_lower]['fundamentals']
                fundamentals_topics.extend([f"{skill}: {topic}" for topic in topics[:2]])
        
        if not fundamentals_topics:
            fundamentals_topics = [
                "Programming fundamentals",
                "Basic syntax and concepts",
                "Development environment setup",
                "Version control (Git)",
                "Problem-solving basics"
            ]
        
        phases.append({
            'phase_number': 1,
            'phase_name': 'Fundamentals',
            'description': 'Build a strong foundation with core concepts and basics',
            'estimated_days': 7,
            'topics': [
                {
                    'topic_name': topic,
                    'description': f'Learn and practice {topic}',
                    'practice_tasks': f'Complete exercises and small projects on {topic}',
                    'estimated_hours': 8.0
                }
                for topic in fundamentals_topics[:5]
            ]
        })
        
        # Phase 2: Core Skills
        core_topics = []
        for skill in primary_skills:
            skill_lower = skill.lower()
            if skill_lower in PreparationPlanService.SKILL_LEARNING_PATHS:
                topics = PreparationPlanService.SKILL_LEARNING_PATHS[skill_lower]['core']
                core_topics.extend([f"{skill}: {topic}" for topic in topics[:2]])
        
        if not core_topics:
            core_topics = [
                "Advanced language features",
                "Framework/library usage",
                "API development",
                "Database integration",
                "Testing basics"
            ]
        
        phases.append({
            'phase_number': 2,
            'phase_name': 'Core Skills',
            'description': 'Master essential skills and technologies required for the role',
            'estimated_days': 14,
            'topics': [
                {
                    'topic_name': topic,
                    'description': f'Deep dive into {topic}',
                    'practice_tasks': f'Build projects using {topic}',
                    'estimated_hours': 12.0
                }
                for topic in core_topics[:5]
            ]
        })
        
        # Phase 3: Advanced Topics
        advanced_topics = []
        for skill in primary_skills[:3]:  # Top 3 skills
            skill_lower = skill.lower()
            if skill_lower in PreparationPlanService.SKILL_LEARNING_PATHS:
                topics = PreparationPlanService.SKILL_LEARNING_PATHS[skill_lower]['advanced']
                advanced_topics.extend([f"{skill}: {topic}" for topic in topics[:2]])
        
        if not advanced_topics:
            advanced_topics = [
                "Design patterns",
                "System architecture",
                "Performance optimization",
                "Security best practices",
                "Scalability concepts"
            ]
        
        phases.append({
            'phase_number': 3,
            'phase_name': 'Advanced Topics',
            'description': 'Explore advanced concepts and best practices',
            'estimated_days': 10,
            'topics': [
                {
                    'topic_name': topic,
                    'description': f'Master advanced {topic}',
                    'practice_tasks': f'Implement {topic} in real-world scenarios',
                    'estimated_hours': 10.0
                }
                for topic in advanced_topics[:4]
            ]
        })
        
        # Phase 4: Practice & Interview Preparation
        practice_tasks = []
        for skill in primary_skills[:3]:
            skill_lower = skill.lower()
            if skill_lower in PreparationPlanService.SKILL_LEARNING_PATHS:
                tasks = PreparationPlanService.SKILL_LEARNING_PATHS[skill_lower]['practice']
                practice_tasks.extend([f"{skill}: {task}" for task in tasks[:1]])
        
        if not practice_tasks:
            practice_tasks = [
                "Build a complete project",
                "Practice coding problems",
                "System design practice",
                "Mock interviews",
                "Portfolio preparation"
            ]
        
        phases.append({
            'phase_number': 4,
            'phase_name': 'Practice & Interview Preparation',
            'description': 'Apply knowledge through projects and prepare for interviews',
            'estimated_days': 14,
            'topics': [
                {
                    'topic_name': task,
                    'description': f'Complete {task}',
                    'practice_tasks': f'Work on {task} and document your progress',
                    'estimated_hours': 16.0
                }
                for task in practice_tasks[:5]
            ]
        })
        
        # Calculate total days
        total_days = sum(phase['estimated_days'] for phase in phases)
        
        return {
            'title': f'Job Preparation Plan',
            'description': f'Structured learning roadmap based on job requirements',
            'total_estimated_days': total_days,
            'phases': phases
        }
    
    @staticmethod
    def create_plan(
        db: Session,
        user_id: int,
        plan_data: Dict,
        job_description_id: Optional[int] = None,
        match_result_id: Optional[int] = None
    ) -> PreparationPlan:
        """Create preparation plan in database."""
        plan = PreparationPlan(
            user_id=user_id,
            job_description_id=job_description_id,
            match_result_id=match_result_id,
            title=plan_data['title'],
            description=plan_data.get('description'),
            total_estimated_days=plan_data.get('total_estimated_days')
        )
        db.add(plan)
        db.flush()
        
        # Create phases
        for phase_data in plan_data['phases']:
            phase = PreparationPhase(
                plan_id=plan.id,
                phase_number=phase_data['phase_number'],
                phase_name=phase_data['phase_name'],
                description=phase_data.get('description'),
                estimated_days=phase_data.get('estimated_days'),
                order_index=phase_data['phase_number']
            )
            db.add(phase)
            db.flush()
            
            # Create topics
            for idx, topic_data in enumerate(phase_data.get('topics', [])):
                topic = PhaseTopic(
                    phase_id=phase.id,
                    topic_name=topic_data['topic_name'],
                    description=topic_data.get('description'),
                    practice_tasks=topic_data.get('practice_tasks'),
                    estimated_hours=topic_data.get('estimated_hours'),
                    order_index=idx + 1
                )
                db.add(topic)
        
        db.commit()
        db.refresh(plan)
        return plan
    
    @staticmethod
    def get_user_plans(db: Session, user_id: int) -> List[PreparationPlan]:
        """Get all preparation plans for a user."""
        return db.query(PreparationPlan).filter(PreparationPlan.user_id == user_id).all()
    
    @staticmethod
    def get_plan_by_id(db: Session, plan_id: int, user_id: int) -> Optional[PreparationPlan]:
        """Get preparation plan by ID (with user ownership check)."""
        return db.query(PreparationPlan).filter(
            PreparationPlan.id == plan_id,
            PreparationPlan.user_id == user_id
        ).first()

