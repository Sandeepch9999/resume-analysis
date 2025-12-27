# Step-by-Step Model Training Guide

Complete guide to train your resume matching model from scratch.

---

## 📋 Prerequisites

- ✅ Backend is set up and running
- ✅ Database has some match results (or you'll create manual data)
- ✅ Python dependencies installed (`pip install -r requirements.txt`)

---

## 🚀 Complete Training Process

### **STEP 1: Collect Training Data**

You have two options:

#### **Option A: Use Existing Database Data (Recommended)**

If you already have analyses in your database:

```bash
# Navigate to ml directory
cd ml

# Run data collection script
python collect_training_data.py
```

This will:
- Extract all resume-JD pairs from your database
- Use existing match_status as labels
- Save to `training_data.json`

**Output:**
```
Found 45 match results in database...
✅ Collected 45 training examples
   Saved to: ml/training_data.json

Label distribution:
   Good Match: 15
   Partial Match: 20
   Poor Match: 10
```

#### **Option B: Create Manual Training Data**

If you don't have enough data, create `ml/training_data.json` manually:

```json
{
  "resume_texts": [
    "Experienced Python developer with 5 years in web development. Proficient in Django, Flask, React, PostgreSQL, and AWS.",
    "Java developer with Spring Boot experience. Knowledge of microservices, Docker, and Kubernetes.",
    "Frontend developer specializing in React and Vue.js. 3 years of experience with modern JavaScript and TypeScript."
  ],
  "jd_texts": [
    "Looking for a Python developer with Django experience. Must know React and have 3+ years experience. PostgreSQL and AWS knowledge required.",
    "Senior Java developer needed. Spring Boot, microservices, Docker, and Kubernetes experience required. 5+ years experience.",
    "Frontend developer position. React, Vue.js, and modern JavaScript required. TypeScript knowledge preferred. Minimum 2 years experience."
  ],
  "labels": [
    "Good Match",
    "Good Match",
    "Good Match"
  ]
}
```

**Important:** 
- Need at least **20-30 examples** (ideally 50-100+)
- Labels must be: `"Good Match"`, `"Partial Match"`, or `"Poor Match"`
- Try to have balanced distribution of labels

---

### **STEP 2: Verify Training Data**

Check your data file:

```bash
cd ml
cat training_data.json  # or open in editor
```

Make sure:
- ✅ All arrays have same length
- ✅ Labels are correct format
- ✅ Text is not empty

---

### **STEP 3: Run Training**

```bash
# Make sure you're in ml directory
cd ml

# Run training script
python train.py
```

**What happens:**
1. Loads training data
2. Splits into train/test (80/20)
3. Trains Random Forest model
4. Evaluates performance
5. Saves model to `ml/models/`

**Expected Output:**
```
============================================================
Resume Matching Model Training
============================================================

📊 Step 1: Loading training data...
   ✅ Loaded 45 training examples

   Label distribution:
      Good Match: 15
      Partial Match: 20
      Poor Match: 10

🤖 Step 2: Initializing model trainer...
   ✅ Trainer initialized

🎯 Step 3: Training model...
   This may take a few minutes...

============================================================
Training Results
============================================================
✅ Accuracy: 85.00%

📈 Classification Report:
   Good Match:
      Precision: 90.00%
      Recall: 85.00%
      F1-Score: 87.50%
      Support: 12

💾 Step 4: Saving model...
   ✅ Model saved to: ml/models/
      - matching_model.pkl
      - vectorizer.pkl

============================================================
✅ Training Complete!
============================================================
```

---

### **STEP 4: Verify Model Files**

Check that model was saved:

```bash
ls -la ml/models/
```

You should see:
- `matching_model.pkl` - Trained model
- `vectorizer.pkl` - TF-IDF vectorizer

---

### **STEP 5: Test the Model**

Create a test script to verify it works:

```python
# ml/test_model.py
from ml.load_trained_model import TrainedResumeMatcher

# Initialize matcher (will auto-load trained model)
matcher = TrainedResumeMatcher()

# Test with sample data
resume = "Python developer with Django and React experience. 5 years in web development."
jd = "Looking for Python developer with Django and React. 3+ years experience required."

result = matcher.analyze_match(resume, jd)
print(f"Match Status: {result['match_status']}")
print(f"Similarity Score: {result['similarity_score']}%")
```

Run test:
```bash
cd ml
python test_model.py
```

---

### **STEP 6: Restart Backend**

The system will automatically use the trained model:

```bash
# Stop your backend (Ctrl+C)
# Then restart
cd backend
python run.py
```

The trained model will be loaded automatically!

---

## 🔄 Retraining (When You Have More Data)

As you collect more data:

1. **Collect new data:**
   ```bash
   cd ml
   python collect_training_data.py
   ```

2. **Retrain:**
   ```bash
   python train.py
   ```

3. **Restart backend** to use new model

---

## 📊 Improving Model Performance

### Tips for Better Results:

1. **More Data = Better Model**
   - Aim for 100+ examples
   - More is always better

2. **Balanced Labels**
   - Try to have similar counts of each label
   - If imbalanced, collect more of minority class

3. **Quality Labels**
   - Ensure labels are accurate
   - Review borderline cases manually

4. **Feature Engineering** (Advanced)
   - Edit `train_model.py` to add more features
   - Experiment with different models

---

## 🐛 Troubleshooting

### Error: "training_data.json not found"
**Solution:** Run `python collect_training_data.py` first, or create the file manually.

### Error: "Less than 3 examples of each label"
**Solution:** You need at least 3 examples of each label type. Collect more data.

### Error: "Model training failed"
**Solution:** 
- Check that all labels are exactly: "Good Match", "Partial Match", or "Poor Match"
- Ensure no empty text fields
- Verify JSON format is correct

### Low Accuracy (< 60%)
**Solution:**
- Collect more training data
- Ensure labels are accurate
- Check for data quality issues

### Model Not Loading
**Solution:**
- Check `ml/models/` directory exists
- Verify `.pkl` files are present
- Check file permissions

---

## 📝 Quick Reference

### Complete Training Workflow:

```bash
# 1. Collect data
cd ml
python collect_training_data.py

# 2. Train model
python train.py

# 3. Restart backend
cd ../backend
python run.py
```

### File Structure After Training:

```
ml/
├── training_data.json          # Your training data
├── models/
│   ├── matching_model.pkl      # Trained model
│   └── vectorizer.pkl          # TF-IDF vectorizer
├── collect_training_data.py    # Data collection script
├── train.py                    # Training script
└── load_trained_model.py       # Model loader
```

---

## ✅ Success Checklist

- [ ] Training data collected (20+ examples)
- [ ] `training_data.json` created
- [ ] Training script ran successfully
- [ ] Model files saved to `ml/models/`
- [ ] Accuracy > 70% (ideally)
- [ ] Backend restarted
- [ ] Model loading in application

---

## 🎯 Next Steps

After training:

1. **Monitor Performance** - Check if predictions improve
2. **Collect Feedback** - Let users rate match quality
3. **Retrain Regularly** - Update model with new data
4. **Fine-tune** - Adjust thresholds and features

---

**That's it! Your model is now trained and ready to use! 🎉**
