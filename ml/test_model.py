"""
Test script to verify trained model works correctly.
Run: python test_model.py
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from ml.load_trained_model import TrainedResumeMatcher

def test_model():
    """Test the trained model with sample data."""
    print("=" * 60)
    print("Testing Trained Model")
    print("=" * 60)
    
    # Initialize matcher (will auto-load trained model if available)
    print("\n🔍 Loading model...")
    try:
        matcher = TrainedResumeMatcher(use_trained_model=True)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Test cases
    test_cases = [
        {
            "name": "Good Match - Python Developer",
            "resume": "Experienced Python developer with 5 years in web development. Proficient in Django, Flask, React, PostgreSQL, and AWS. Strong background in REST APIs and microservices.",
            "jd": "Looking for a Python developer with Django experience. Must know React and have 3+ years experience. PostgreSQL and AWS knowledge required. REST API experience preferred."
        },
        {
            "name": "Partial Match - Java Developer",
            "resume": "Java developer with Spring Boot experience. Knowledge of microservices and basic cloud concepts.",
            "jd": "Senior Java developer needed. Spring Boot, microservices, Docker, Kubernetes, and extensive AWS experience required. 5+ years experience."
        },
        {
            "name": "Poor Match - Frontend Only",
            "resume": "Frontend developer specializing in React and Vue.js. 3 years of experience with modern JavaScript and CSS.",
            "jd": "Backend Python developer needed. Django, Flask, PostgreSQL, and system design experience required. 5+ years experience."
        }
    ]
    
    print("\n🧪 Running test cases...\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print("-" * 60)
        
        try:
            result = matcher.analyze_match(test['resume'], test['jd'])
            
            print(f"Match Status: {result['match_status']}")
            print(f"Similarity Score: {result['similarity_score']:.2f}%")
            print(f"Present Skills: {len(result['present_skills'])}")
            print(f"Missing Skills: {len(result['missing_skills'])}")
            
            if result['present_skills']:
                print(f"   Present: {', '.join(list(result['present_skills'])[:5])}")
            if result['missing_skills']:
                print(f"   Missing: {', '.join(list(result['missing_skills'])[:5])}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    print("=" * 60)
    print("✅ Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_model()

