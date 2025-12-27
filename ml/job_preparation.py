from typing import List, Dict
from ml.skill_extractor import SkillExtractor

class JobPreparationGenerator:
    # Learning resources database
    LEARNING_RESOURCES = {
        'python': [
            {'title': 'Python Official Documentation', 'url': 'https://docs.python.org/3/', 'type': 'Documentation'},
            {'title': 'Real Python Tutorials', 'url': 'https://realpython.com/', 'type': 'Article'},
            {'title': 'Python Crash Course', 'url': 'https://www.youtube.com/results?search_query=python+crash+course', 'type': 'Video'}
        ],
        'react': [
            {'title': 'React Official Documentation', 'url': 'https://react.dev/', 'type': 'Documentation'},
            {'title': 'React Tutorial for Beginners', 'url': 'https://www.youtube.com/results?search_query=react+tutorial', 'type': 'Video'},
            {'title': 'React Best Practices', 'url': 'https://react.dev/learn', 'type': 'Article'}
        ],
        'machine learning': [
            {'title': 'Machine Learning Course by Andrew Ng', 'url': 'https://www.coursera.org/learn/machine-learning', 'type': 'Course'},
            {'title': 'Scikit-learn Documentation', 'url': 'https://scikit-learn.org/stable/', 'type': 'Documentation'},
            {'title': 'Hands-On Machine Learning', 'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/', 'type': 'Article'}
        ],
        'aws': [
            {'title': 'AWS Official Documentation', 'url': 'https://docs.aws.amazon.com/', 'type': 'Documentation'},
            {'title': 'AWS Certified Solutions Architect', 'url': 'https://aws.amazon.com/certification/certified-solutions-architect-associate/', 'type': 'Course'},
            {'title': 'AWS Tutorial for Beginners', 'url': 'https://www.youtube.com/results?search_query=aws+tutorial', 'type': 'Video'}
        ],
        'docker': [
            {'title': 'Docker Official Documentation', 'url': 'https://docs.docker.com/', 'type': 'Documentation'},
            {'title': 'Docker Tutorial for Beginners', 'url': 'https://www.youtube.com/results?search_query=docker+tutorial', 'type': 'Video'},
            {'title': 'Docker Deep Dive', 'url': 'https://www.pluralsight.com/courses/docker-deep-dive', 'type': 'Course'}
        ]
    }
    
    @staticmethod
    def generate_syllabus(jd_skills: List[str], missing_skills: List[str]) -> List[Dict]:
        """Generate syllabus topics based on job requirements."""
        syllabus = []
        
        # High priority for missing skills
        for skill in missing_skills[:5]:  # Top 5 missing skills
            syllabus.append({
                'topic': f'Learn {skill.title()}',
                'description': f'Master {skill} to meet job requirements. Focus on practical implementation and best practices.',
                'priority': 'High'
            })
        
        # Medium priority for present skills (to strengthen)
        for skill in jd_skills[:3]:  # Top 3 required skills
            if skill not in missing_skills:
                syllabus.append({
                    'topic': f'Advanced {skill.title()}',
                    'description': f'Deepen your knowledge of {skill} with advanced concepts and real-world applications.',
                    'priority': 'Medium'
                })
        
        # General topics
        syllabus.extend([
            {
                'topic': 'System Design Fundamentals',
                'description': 'Understand scalable system architecture, design patterns, and best practices.',
                'priority': 'Medium'
            },
            {
                'topic': 'Interview Preparation',
                'description': 'Practice coding problems, system design questions, and behavioral interviews.',
                'priority': 'High'
            }
        ])
        
        return syllabus[:8]  # Limit to 8 topics
    
    @staticmethod
    def generate_interview_questions(jd_skills: List[str]) -> List[Dict]:
        """Generate interview questions based on required skills."""
        questions = []
        
        # Technical questions based on skills
        for skill in jd_skills[:5]:
            questions.append({
                'question': f'Explain your experience with {skill}. Can you describe a project where you used {skill}?',
                'category': 'Technical'
            })
            questions.append({
                'question': f'What are the key concepts and best practices you follow when working with {skill}?',
                'category': 'Technical'
            })
        
        # General technical questions
        questions.extend([
            {
                'question': 'Describe a challenging technical problem you solved and how you approached it.',
                'category': 'Technical'
            },
            {
                'question': 'How do you ensure code quality and maintainability in your projects?',
                'category': 'Technical'
            },
            {
                'question': 'Tell me about a time when you had to learn a new technology quickly for a project.',
                'category': 'Behavioral'
            },
            {
                'question': 'Describe a situation where you had to work under pressure to meet a deadline.',
                'category': 'Behavioral'
            },
            {
                'question': 'How do you handle disagreements with team members or stakeholders?',
                'category': 'Behavioral'
            },
            {
                'question': 'Design a scalable system to handle millions of requests per second.',
                'category': 'System Design'
            }
        ])
        
        return questions[:15]  # Limit to 15 questions
    
    @staticmethod
    def generate_learning_resources(jd_skills: List[str], missing_skills: List[str]) -> List[Dict]:
        """Generate learning resources based on skills."""
        resources = []
        
        # Resources for missing skills (high priority)
        for skill in missing_skills[:5]:
            skill_lower = skill.lower()
            if skill_lower in JobPreparationGenerator.LEARNING_RESOURCES:
                resources.extend(JobPreparationGenerator.LEARNING_RESOURCES[skill_lower])
            else:
                # Generic resource if specific not found
                resources.append({
                    'title': f'{skill.title()} Learning Guide',
                    'url': f'https://www.google.com/search?q={skill}+tutorial',
                    'type': 'Article',
                    'description': f'Comprehensive guide to learn {skill}'
                })
        
        # Resources for present skills
        for skill in jd_skills[:3]:
            if skill not in missing_skills:
                skill_lower = skill.lower()
                if skill_lower in JobPreparationGenerator.LEARNING_RESOURCES:
                    resources.extend(JobPreparationGenerator.LEARNING_RESOURCES[skill_lower][:1])  # One resource per skill
        
        # General resources
        resources.extend([
            {
                'title': 'LeetCode - Practice Coding Problems',
                'url': 'https://leetcode.com/',
                'type': 'Article',
                'description': 'Practice coding interview problems'
            },
            {
                'title': 'System Design Primer',
                'url': 'https://github.com/donnemartin/system-design-primer',
                'type': 'Article',
                'description': 'Learn system design concepts'
            }
        ])
        
        return resources[:12]  # Limit to 12 resources

