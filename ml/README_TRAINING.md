# Model Training Guide

## Current System (No Training Required)

The current implementation uses **unsupervised methods** that work immediately:

- ✅ **TF-IDF Vectorization** - No training needed
- ✅ **Cosine Similarity** - Mathematical calculation
- ✅ **Keyword Matching** - Rule-based extraction

**These work out of the box!**

---

## When to Add Training

Training is **optional** and only needed if you want to:

1. **Improve accuracy** - Better match predictions
2. **Learn from data** - Use historical results to improve
3. **Customize for your domain** - Adapt to specific industries/roles

---

## How to Train (Optional)

### Step 1: Collect Training Data

You need labeled examples:
- Resume text
- Job description text
- Match label: "Good Match", "Partial Match", or "Poor Match"

**Ways to collect data:**
1. Manually label existing analyses
2. Collect user feedback on match quality
3. Use historical data with known outcomes
4. Start with 50-100 examples (more is better)

### Step 2: Prepare Training Data

Create a CSV or load from database:

```python
# Example structure
training_data = {
    'resume_texts': [...],
    'jd_texts': [...],
    'labels': ['Good Match', 'Partial Match', ...]
}
```

### Step 3: Run Training

```bash
cd ml
python train_model.py
```

### Step 4: Use Trained Model

The system will automatically use the trained model if available, otherwise falls back to TF-IDF.

---

## Training Script Usage

```python
from ml.train_model import ResumeMatchingModelTrainer

# Initialize trainer
trainer = ResumeMatchingModelTrainer()

# Train with your data
metrics = trainer.train(
    resume_texts=your_resume_texts,
    jd_texts=your_jd_texts,
    labels=your_labels,
    model_type='random_forest'  # or 'gradient_boosting'
)

# Save model
trainer.save_model()

# Use for prediction
prediction, confidence = trainer.predict(resume_text, jd_text)
```

---

## Integration with Existing System

The trained model integrates seamlessly:

1. Train model → saves to `ml/models/`
2. System automatically detects and uses trained model
3. Falls back to TF-IDF if no trained model exists

**No code changes needed in the main application!**

---

## Requirements for Training

Add to `backend/requirements.txt`:
```
scikit-learn==1.3.2  # Already included
joblib==1.3.2        # For model saving
```

---

## Example: Collecting Training Data from Database

```python
# Script to export training data from your database
from app.core.database import SessionLocal
from app.models.match_result import MatchResult
from app.models.resume import Resume
from app.models.job_description import JobDescription

db = SessionLocal()

# Get all match results
results = db.query(MatchResult).all()

training_data = []
for result in results:
    resume = db.query(Resume).filter(Resume.id == result.resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == result.job_description_id).first()
    
    if resume and jd:
        training_data.append({
            'resume_text': resume.extracted_text,
            'jd_text': jd.description,
            'label': result.match_status  # Use existing classification
        })

# Save to CSV or use directly for training
```

---

## Important Notes

1. **Training is optional** - The system works without it
2. **More data = better results** - Aim for 100+ examples
3. **Label quality matters** - Ensure accurate labels
4. **Regular retraining** - Retrain as you collect more data
5. **Domain-specific** - Train on data similar to your use case

---

## Quick Start (Without Training)

**You don't need to train anything!** The system works immediately:

1. Start the backend
2. Upload resumes
3. Create job descriptions
4. Analyze - it works!

Training is only for **improving accuracy** over time.

