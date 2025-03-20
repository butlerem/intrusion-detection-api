from flask import Flask, request, jsonify
import joblib
import numpy as np

# Load trained LightGBM Model
model = joblib.load("Lightgbm_model.pkl")

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
  data = request.json
  features = np.array(data['features']).reshape(1, -1)

  # Get probability prediction
  probs = model.predict_proba(features)[:,1]

  # Apply threshold 0.3
  prediction = init(probs[0] > 0.3)

  return jsonify({'attack_detected': prediction})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)