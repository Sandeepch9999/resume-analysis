"""
Script to load and use a trained model (if available).
This integrates trained models into the existing system.
"""

import os
import numpy as np
import joblib
from typing import Dict
from ml.matcher import ResumeMatcher
from ml.skill_extractor import SkillExtractor

class TrainedResumeMatcher(ResumeMatcher):
    """
    Enhanced matcher that can use trained models if available.
    Falls back to original TF-IDF method if no trained model exists.
    """
    
    def __init__(self, use_trained_model: bool = True):
        super().__init__()
        self.trained_model = None
        self.trained_vectorizer = None
        self.use_trained = False
        
        if use_trained_model:
            self._load_trained_model()
    
    def _load_trained_model(self):
        """Load trained model if it exists."""
        model_dir = 'models'
        model_path = os.path.join(model_dir, 'matching_model.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            try:
                self.trained_model = joblib.load(model_path)
                self.trained_vectorizer = joblib.load(vectorizer_path)
                self.use_trained = True
                print("✅ Loaded trained model")
            except Exception as e:
                print(f"⚠️  Could not load trained model: {e}")
                print("   Using default TF-IDF method")
        else:
            print("ℹ️  No trained model found. Using default TF-IDF method.")
    
    def analyze_match(self, resume_text: str, jd_text: str) -> Dict:
        """
        Analyze match using trained model if available, otherwise use default method.
        """
        if self.use_trained and self.trained_model:
            return self._analyze_with_trained_model(resume_text, jd_text)
        else:
            return super().analyze_match(resume_text, jd_text)
    
    def _analyze_with_trained_model(self, resume_text: str, jd_text: str) -> Dict:
        """Analyze using trained model."""
        # Prepare features (same as training)
        combined_text = f"{resume_text} {jd_text}"
        tfidf_features = self.trained_vectorizer.transform([combined_text]).toarray()
        
        # Additional features
        resume_words = len(resume_text.split())
        jd_words = len(jd_text.split())
        resume_word_set = set(resume_text.lower().split())
        jd_word_set = set(jd_text.lower().split())
        overlap = len(resume_word_set & jd_word_set) / max(len(jd_word_set), 1)
        
        additional_features = np.array([[
            resume_words,
            jd_words,
            resume_words / max(jd_words, 1),
            overlap
        ]])
        
        # Combine features
        import numpy as np
        features = np.hstack([tfidf_features, additional_features])
        
        # Predict
        match_status = self.trained_model.predict(features)[0]
        probabilities = self.trained_model.predict_proba(features)[0]
        similarity_score = max(probabilities) * 100  # Convert to percentage
        
        # Extract skills (using original method)
        resume_skills = SkillExtractor.extract_skills_from_text(resume_text)
        jd_skills = SkillExtractor.extract_skills_from_jd(jd_text)
        missing_skills = SkillExtractor.find_missing_skills(resume_skills, jd_skills)
        present_skills = SkillExtractor.find_present_skills(resume_skills, jd_skills)
        
        # Generate suggestions
        correction_suggestions = self.generate_correction_suggestions(
            resume_text, jd_text, similarity_score
        )
        
        return {
            "similarity_score": round(similarity_score, 2),
            "match_status": match_status,
            "correction_suggestions": correction_suggestions,
            "resume_skills": list(resume_skills),
            "jd_skills": list(jd_skills),
            "missing_skills": list(missing_skills),
            "present_skills": list(present_skills)
        }

