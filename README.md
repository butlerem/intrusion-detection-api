## LightGBM Intrusion Detection

A Python project for detecting network intrusions using a LightGBM classifier and serving predictions via a Flask API.

## Overview
- Load and preprocess network session data
- Train and evaluate LightGBM model with balanced classes
- Adjust decision threshold to boost recall
- Expose /predict endpoint for real-time inference

## Requirements
Python 3.8+
Packages listed in requirements.txt:
```python
  numpy
  pandas
  seaborn
  matplotlib
  xgboost
  lightgbm
  scikit-learn
  Flask
  joblib
```

## Data
- Input CSV: cybersecurity_intrusion_data.csv
- Key steps:
  - Drop unused columns
  - Fill missing encryption_used with None
  - One-hot encode protocol_type and encryption_used
  - Split into train/test (80/20)
  
## Training
Run python train.py (or notebook):
- Imports and settings
- Preprocessing as above
- Model instantiation:
```python
from lightgbm import LGBMClassifier
model = LGBMClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)
```
- Predictions and evaluation (precision, recall, F1)
- Lower threshold to 0.3 to increase recall:
```python
probs = model.predict_proba(X_test)[:,1]
y_pred = (probs > 0.3).astype(int)
```
- View results summary table in notebook
- Save model:
```python
import joblib
joblib.dump(model, 'Lightgbm_model.pkl')
```
## API
- File: app.py (or flask_app.py)
- Load model:
```python
model = joblib.load('Lightgbm_model.pkl')
```
Endpoint:
```python
POST /predict
Request JSON: {"features": [v1, v2, ..., v10]}
Response JSON: {"attack_detected": true|false}
```
Runs on port 5000 by default:
```bash
flask run --host 0.0.0.0 --port 5000
```
## Usage
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Train model:
```bash
python train.py
```
3. Start API:
```bash
python app.py
```
3. Test prediction:
```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"features":[599,4,492.98,0.6068,1,0,1,0,1,0]}'
```
4. Results

Final comparison of models (precision, recall, F1):
```python
Random Forest            98.6 / 71.9 / 83.2
XGBoost (Default)        94.1 / 73.7 / 82.6
XGBoost (Tuned)          90.3 / 74.3 / 81.5
LightGBM (Default)       97.8 / 72.7 / 83.4
LightGBM (Threshold 0.3) 82.7 / 78.2 / 80.4
```
## License
MIT

