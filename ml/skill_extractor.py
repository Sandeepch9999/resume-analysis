import re
from typing import List, Set

class SkillExtractor:
    # Common technical skills database
    TECHNICAL_SKILLS = {
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'ruby', 'php',
        'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash',
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
        'spring', 'asp.net', 'laravel', 'next.js', 'nuxt.js', 'svelte',
        # Databases
        'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'oracle',
        'sqlite', 'dynamodb', 'neo4j', 'firebase',
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
        'terraform', 'ansible', 'ci/cd', 'linux', 'unix',
        # Data Science & ML
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'data analysis',
        # Mobile
        'android', 'ios', 'react native', 'flutter', 'xamarin',
        # Other
        'git', 'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'jira'
    }
    
    @staticmethod
    def extract_skills_from_text(text: str) -> Set[str]:
        """Extract skills from text using keyword matching."""
        text_lower = text.lower()
        found_skills = set()
        
        for skill in SkillExtractor.TECHNICAL_SKILLS:
            # Check for exact word match or phrase match
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        return found_skills
    
    @staticmethod
    def extract_skills_from_jd(jd_text: str) -> Set[str]:
        """Extract required skills from job description."""
        return SkillExtractor.extract_skills_from_text(jd_text)
    
    @staticmethod
    def find_missing_skills(resume_skills: Set[str], jd_skills: Set[str]) -> Set[str]:
        """Find skills required in JD but missing in resume."""
        return jd_skills - resume_skills
    
    @staticmethod
    def find_present_skills(resume_skills: Set[str], jd_skills: Set[str]) -> Set[str]:
        """Find skills that are both in resume and JD."""
        return resume_skills & jd_skills

