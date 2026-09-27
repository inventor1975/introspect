from flask import Flask, make_response, request

app = Flask(__name__)


def classify(filename):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return "accepted", filename
    return "rejected", filename


@app.post("/upload/check")
def upload_check():
    upload = request.files.get("file")
    original = upload.filename if upload else request.form.get("filename", "")
    status, detail = classify(original)
    resp = make_response(f"<p class='upload-{status}'>Upload {status}.</p>")
    resp.headers["X-Upload-Status"] = status
    return resp
