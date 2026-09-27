import os

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["RESUME_FOLDER"] = "/srv/app/resumes"


@app.post("/careers/apply")
def apply():
    resume = request.files.get("resume")
    if resume is None or not resume.filename:
        return jsonify({"error": "resume required"}), 400
    filename = secure_filename(resume.filename)
    if not filename.lower().endswith((".pdf", ".docx")):
        return jsonify({"error": "unsupported format"}), 400
    resume.save(os.path.join(app.config["RESUME_FOLDER"], filename))
    return jsonify({"stored": filename}), 201
