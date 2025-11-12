# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
from model import predict_emotion

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            return "No selected file"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            result = predict_emotion(filepath)
            return render_template('result.html', result=result, image_path=filepath)
        except Exception as e:
            return f"Error predicting emotion: {e}"

    elif 'file' in request.files:  # Webcam capture
        file = request.files['file']
        if file.filename == '':
            return "No file received"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            result = predict_emotion(filepath)
            return render_template('result.html', result=result, image_path=filepath)
        except Exception as e:
            return f"Error predicting emotion: {e}"

    else:
        return "No image provided"

if __name__ == '__main__':
    app.run(debug=True)
