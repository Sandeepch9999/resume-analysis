"""
Complete training script - ready to use!
Run: python train.py
"""

import sys
from pathlib import Path
import json
import numpy as np

# Add backend to path for imports
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from ml.train_model import ResumeMatchingModelTrainer

def load_training_data():
    """Load training data from JSON file."""
    data_file = Path(__file__).parent / 'training_data.json'
    
    if not data_file.exists():
        print("❌ training_data.json not found!")
        print("\nTo create training data:")
        print("1. Run: python collect_training_data.py (from ml directory)")
        print("2. Or manually create training_data.json with your data")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def main():
    """Main training function."""
    print("=" * 60)
    print("Resume Matching Model Training")
    print("=" * 60)
    
    # Step 1: Load training data
    print("\n📊 Step 1: Loading training data...")
    training_data = load_training_data()
    
    if not training_data:
        return
    
    resume_texts = training_data.get('resume_texts', [])
    jd_texts = training_data.get('jd_texts', [])
    labels = training_data.get('labels', [])
    
    # Validate data
    if len(resume_texts) != len(jd_texts) or len(resume_texts) != len(labels):
        print("❌ Error: Mismatched data lengths!")
        print(f"   Resumes: {len(resume_texts)}, JDs: {len(jd_texts)}, Labels: {len(labels)}")
        return
    
    if len(resume_texts) == 0:
        print("❌ Error: No training data found!")
        return
    
    print(f"   ✅ Loaded {len(resume_texts)} training examples")
    
    # Show label distribution
    from collections import Counter
    label_counts = Counter(labels)
    print(f"\n   Label distribution:")
    for label, count in label_counts.items():
        print(f"      {label}: {count}")
    
    # Check minimum data requirement
    if len(resume_texts) < 20:
        print("\n⚠️  Warning: Less than 20 examples may result in poor model performance.")
        response = input("   Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("   Training cancelled.")
            return
    
    # Step 2: Initialize trainer
    print("\n🤖 Step 2: Initializing model trainer...")
    trainer = ResumeMatchingModelTrainer()
    print("   ✅ Trainer initialized")
    
    # Step 3: Train model
    print("\n🎯 Step 3: Training model...")
    print("   This may take a few minutes...")
    
    try:
        metrics = trainer.train(
            resume_texts=resume_texts,
            jd_texts=jd_texts,
            labels=labels,
            test_size=0.2,  # 20% for testing
            model_type='random_forest'  # or 'gradient_boosting'
        )
        
        print("\n" + "=" * 60)
        print("Training Results")
        print("=" * 60)
        print(f"✅ Accuracy: {metrics['accuracy']:.2%}")
        
        # Show detailed metrics
        print("\n📈 Classification Report:")
        report = metrics['classification_report']
        for label in ['Good Match', 'Partial Match', 'Poor Match']:
            if label in report:
                precision = report[label]['precision']
                recall = report[label]['recall']
                f1 = report[label]['f1-score']
                support = report[label]['support']
                print(f"   {label}:")
                print(f"      Precision: {precision:.2%}")
                print(f"      Recall: {recall:.2%}")
                print(f"      F1-Score: {f1:.2%}")
                print(f"      Support: {support}")
        
        # Step 4: Save model
        print("\n💾 Step 4: Saving model...")
        model_dir = Path(__file__).parent / 'models'
        trainer.save_model(str(model_dir))
        print(f"   ✅ Model saved to: {model_dir}/")
        print(f"      - matching_model.pkl")
        print(f"      - vectorizer.pkl")
        
        print("\n" + "=" * 60)
        print("✅ Training Complete!")
        print("=" * 60)
        print("\nThe model will be automatically used by the application.")
        print("Restart your backend server to load the new model.")
        
    except Exception as e:
        print(f"\n❌ Training failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Check that all labels are: 'Good Match', 'Partial Match', or 'Poor Match'")
        print("2. Ensure you have at least 3 examples of each label")
        print("3. Check that resume_texts and jd_texts are not empty")

if __name__ == "__main__":
    main()

