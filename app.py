from flask import Flask, request, jsonify, render_template
import joblib
import os
from utils.features import extract_features

app = Flask(__name__)

# Load model dari folder 'model'
model = joblib.load("model/manual_password_model300.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    password = request.form.get('password') or (request.json and request.json.get('password'))
    if not password:
        return jsonify({'error': 'Password required'}), 400

    features = extract_features(password)
    strength = model.predict(features)[0]

    if request.form:
        return render_template("index.html", result=strength, password=password)

    return jsonify({'strength': strength})


