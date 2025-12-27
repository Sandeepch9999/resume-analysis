"""
Script to collect training data from your database.
Run this from the backend directory.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from app.core.database import SessionLocal
from app.models.match_result import MatchResult
from app.models.resume import Resume
from app.models.job_description import JobDescription
import json

def collect_training_data():
    """Collect training data from database."""
    db = SessionLocal()
    
    try:
        # Get all match results
        results = db.query(MatchResult).all()
        
        training_data = {
            'resume_texts': [],
            'jd_texts': [],
            'labels': []
        }
        
        print(f"Found {len(results)} match results in database...")
        
        for result in results:
            resume = db.query(Resume).filter(Resume.id == result.resume_id).first()
            jd = db.query(JobDescription).filter(JobDescription.id == result.job_description_id).first()
            
            if resume and jd and resume.extracted_text:
                training_data['resume_texts'].append(resume.extracted_text)
                training_data['jd_texts'].append(jd.description)
                training_data['labels'].append(result.match_status)
        
        # Save to JSON
        output_file = Path(__file__).parent / 'training_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Collected {len(training_data['resume_texts'])} training examples")
        print(f"   Saved to: {output_file}")
        
        # Show label distribution
        from collections import Counter
        label_counts = Counter(training_data['labels'])
        print(f"\nLabel distribution:")
        for label, count in label_counts.items():
            print(f"   {label}: {count}")
        
        if len(training_data['resume_texts']) < 20:
            print("\n⚠️  Warning: You have less than 20 examples.")
            print("   Consider adding more data for better model performance.")
            print("   You can:")
            print("   1. Run more analyses in the application")
            print("   2. Manually add examples to training_data.json")
        
        return training_data
        
    except Exception as e:
        print(f"❌ Error collecting data: {str(e)}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    collect_training_data()

