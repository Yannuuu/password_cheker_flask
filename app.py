from flask import Flask, request, jsonify  # Hapus render_template
import joblib
import os
from utils.features import extract_features

app = Flask(__name__)

# Load model
model = joblib.load("model/manual_password_model300.pkl")

@app.route('/')
def home():
    return "Flask works!"

@app.route('/predict', methods=['POST'])
def predict():
    password = request.form.get('password') or (request.json and request.json.get('password'))
    
    if not password:
        return jsonify({'error': 'Password required'}), 400

    try:
        features = extract_features(password)
        strength = model.predict(features)[0]
        return jsonify({'strength': strength})
    
    except Exception as e:
        # Ini sangat penting buat tahu apa error-nya
        return jsonify({'error': str(e)}), 500
