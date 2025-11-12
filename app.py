# app.py
from flask import Flask, render_template, request
import os
from model import predict_emotion

app = Flask(__name__)

# Use /tmp on Render, static/uploads locally
if os.environ.get("RENDER"):  # Render automatically sets this
    UPLOAD_FOLDER = "/tmp"
else:
    UPLOAD_FOLDER = os.path.join("static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("image") or request.files.get("file")
    if not file or file.filename == "":
        return "No file uploaded"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    try:
        result = predict_emotion(filepath)
        return render_template("result.html", result=result, image_path=filepath)
    except Exception as e:
        return f"Error predicting emotion: {e}"


if __name__ == "__main__":
    app.run(debug=True)
