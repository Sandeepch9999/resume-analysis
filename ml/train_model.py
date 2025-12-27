"""
Training script for enhanced resume matching model.
This is an optional enhancement to improve matching accuracy.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os
from typing import List, Dict, Tuple

class ResumeMatchingModelTrainer:
    """
    Trainer for resume-job description matching model.
    This can be used to improve match classification accuracy.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        self.model = None
        self.is_trained = False
    
    def prepare_features(self, resume_texts: List[str], jd_texts: List[str]) -> np.ndarray:
        """
        Prepare features from resume and job description pairs.
        
        Args:
            resume_texts: List of resume texts
            jd_texts: List of job description texts
            
        Returns:
            Feature matrix
        """
        # Combine texts for TF-IDF
        combined_texts = [f"{resume} {jd}" for resume, jd in zip(resume_texts, jd_texts)]
        
        # Fit and transform
        tfidf_features = self.vectorizer.fit_transform(combined_texts).toarray()
        
        # Additional features
        additional_features = []
        for resume, jd in zip(resume_texts, jd_texts):
            # Length features
            resume_len = len(resume.split())
            jd_len = len(jd.split())
            
            # Skill overlap (simplified)
            resume_words = set(resume.lower().split())
            jd_words = set(jd.lower().split())
            overlap = len(resume_words & jd_words) / max(len(jd_words), 1)
            
            additional_features.append([
                resume_len,
                jd_len,
                resume_len / max(jd_len, 1),  # Length ratio
                overlap  # Word overlap ratio
            ])
        
        # Combine TF-IDF and additional features
        additional_features = np.array(additional_features)
        features = np.hstack([tfidf_features, additional_features])
        
        return features
    
    def train(
        self,
        resume_texts: List[str],
        jd_texts: List[str],
        labels: List[str],
        test_size: float = 0.2,
        model_type: str = 'random_forest'
    ) -> Dict:
        """
        Train the matching model.
        
        Args:
            resume_texts: List of resume texts
            jd_texts: List of job description texts
            labels: List of labels ('Good Match', 'Partial Match', 'Poor Match')
            test_size: Proportion of data for testing
            model_type: 'random_forest' or 'gradient_boosting'
            
        Returns:
            Training metrics dictionary
        """
        # Prepare features
        X = self.prepare_features(resume_texts, jd_texts)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Initialize model
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model_type: {model_type}")
        
        # Train
        print("Training model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        self.is_trained = True
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
    
    def predict(self, resume_text: str, jd_text: str) -> Tuple[str, float]:
        """
        Predict match status for a resume-JD pair.
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            
        Returns:
            Tuple of (predicted_label, confidence_score)
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare features
        X = self.prepare_features([resume_text], [jd_text])
        
        # Predict
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        confidence = max(probabilities)
        
        return prediction, confidence
    
    def save_model(self, model_dir: str = 'models'):
        """Save the trained model and vectorizer."""
        if not self.is_trained:
            raise ValueError("No trained model to save.")
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        joblib.dump(self.model, os.path.join(model_dir, 'matching_model.pkl'))
        
        # Save vectorizer
        joblib.dump(self.vectorizer, os.path.join(model_dir, 'vectorizer.pkl'))
        
        print(f"Model saved to {model_dir}/")
    
    def load_model(self, model_dir: str = 'models'):
        """Load a trained model and vectorizer."""
        model_path = os.path.join(model_dir, 'matching_model.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Model files not found in {model_dir}/")
        
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.is_trained = True
        
        print(f"Model loaded from {model_dir}/")


def create_sample_training_data():
    """
    Create sample training data.
    In production, you would collect real data from your application.
    """
    # Sample data - replace with real data from your database
    sample_data = {
        'resume_texts': [
            "Experienced Python developer with 5 years in web development. Proficient in Django, Flask, and React.",
            "Java developer with Spring Boot experience. Knowledge of microservices architecture.",
            "Frontend developer specializing in React and Vue.js. 3 years of experience.",
        ],
        'jd_texts': [
            "Looking for a Python developer with Django experience. Must know React and have 3+ years experience.",
            "Senior Java developer needed. Spring Boot, microservices, and cloud experience required.",
            "Frontend developer position. React, Vue.js, and modern JavaScript required.",
        ],
        'labels': [
            'Good Match',
            'Good Match',
            'Good Match',
        ]
    }
    
    return sample_data


def main():
    print("=" * 50)
    print("Resume Matching Model Trainer")
    print("=" * 50)
    
    # Create trainer
    trainer = ResumeMatchingModelTrainer()
    
    # --- CHANGE: Load from CSV instead of sample data ---
    csv_path = "resume_data.csv" # Ensure this file is in backend/ml/
    
    if os.path.exists(csv_path):
        print(f"Loading data from {csv_path}...")
        try:
            df = pd.read_csv(csv_path)
            
            # map CSV columns to expected keys
            # Ensure your CSV has columns: 'resume_text', 'jd_text', 'label'
            training_data = {
                'resume_texts': df['resume_text'].fillna("").tolist(),
                'jd_texts': df['jd_text'].fillna("").tolist(),
                'labels': df['label'].tolist()
            }
            print(f"Loaded {len(training_data['resume_texts'])} examples.")
            
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return
    else:
        # Fallback to sample data if CSV doesn't exist
        print("CSV not found. Generating sample data for testing...")
        training_data = create_sample_training_data()

    # --- CHANGE: Removed the '< 10' check so it runs even with small data ---
    
    # Train model
    try:
        metrics = trainer.train(
            resume_texts=training_data['resume_texts'],
            jd_texts=training_data['jd_texts'],
            labels=training_data['labels'],
            model_type='random_forest'
        )
        
        print("\n" + "=" * 50)
        print("Training Results")
        print("=" * 50)
        print(f"Accuracy: {metrics['accuracy']:.2%}")
        
        # Save model
        trainer.save_model(model_dir='models') # This saves to backend/ml/models/
        print("\n✅ Model training completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Training failed: {str(e)}")

if __name__ == "__main__":
    main()