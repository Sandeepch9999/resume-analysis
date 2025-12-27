from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Tuple, Dict, List
from ml.skill_extractor import SkillExtractor

class ResumeMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
    
    def calculate_similarity(self, resume_text: str, jd_text: str) -> float:
        """Calculate cosine similarity between resume and job description."""
        try:
            # Combine texts for fitting
            texts = [resume_text, jd_text]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage
            similarity_percentage = similarity * 100
            
            return round(similarity_percentage, 2)
        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def classify_match(self, similarity_score: float) -> str:
        """Classify match status based on similarity score."""
        if similarity_score >= 70:
            return "Good Match"
        elif similarity_score >= 40:
            return "Partial Match"
        else:
            return "Poor Match"
    
    def generate_correction_suggestions(self, resume_text: str, jd_text: str, similarity_score: float) -> str:
        """Generate correction suggestions based on analysis."""
        suggestions = []
        
        # Extract skills
        resume_skills = SkillExtractor.extract_skills_from_text(resume_text)
        jd_skills = SkillExtractor.extract_skills_from_jd(jd_text)
        missing_skills = SkillExtractor.find_missing_skills(resume_skills, jd_skills)
        present_skills = SkillExtractor.find_present_skills(resume_skills, jd_skills)
        
        # Skill-based suggestions
        if missing_skills:
            suggestions.append(f"Missing Skills: Add the following skills to your resume: {', '.join(list(missing_skills)[:10])}")
        
        if present_skills:
            suggestions.append(f"Matched Skills: You have {len(present_skills)} matching skills: {', '.join(list(present_skills)[:10])}")
        
        # Score-based suggestions
        if similarity_score < 40:
            suggestions.append("Overall: Your resume needs significant improvement. Focus on aligning your experience with the job requirements.")
        elif similarity_score < 70:
            suggestions.append("Overall: Your resume is partially aligned. Consider highlighting more relevant experience and skills.")
        else:
            suggestions.append("Overall: Your resume is well-aligned with the job description. Minor tweaks may help improve your chances.")
        
        # Keyword optimization
        suggestions.append("Tip: Use keywords from the job description naturally throughout your resume, especially in the skills and experience sections.")
        
        return "\n".join(suggestions)
    
    def analyze_match(self, resume_text: str, jd_text: str) -> Dict:
        """Complete match analysis."""
        similarity_score = self.calculate_similarity(resume_text, jd_text)
        match_status = self.classify_match(similarity_score)
        correction_suggestions = self.generate_correction_suggestions(resume_text, jd_text, similarity_score)
        
        # Extract skills for detailed analysis
        resume_skills = SkillExtractor.extract_skills_from_text(resume_text)
        jd_skills = SkillExtractor.extract_skills_from_jd(jd_text)
        missing_skills = SkillExtractor.find_missing_skills(resume_skills, jd_skills)
        present_skills = SkillExtractor.find_present_skills(resume_skills, jd_skills)
        
        return {
            "similarity_score": similarity_score,
            "match_status": match_status,
            "correction_suggestions": correction_suggestions,
            "resume_skills": list(resume_skills),
            "jd_skills": list(jd_skills),
            "missing_skills": list(missing_skills),
            "present_skills": list(present_skills)
        }

