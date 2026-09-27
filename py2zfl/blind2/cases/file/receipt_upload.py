import os

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

RECEIPTS = "/srv/expenses/receipts"


@app.post("/expenses/<int:expense_id>/receipt")
def upload_receipt(expense_id):
    receipt = request.files.get("receipt")
    if receipt is None:
        return jsonify(error="receipt missing"), 400
    filename = secure_filename(receipt.filename or "")
    if not filename:
        return jsonify(error="invalid filename"), 400
    folder = os.path.join(RECEIPTS, str(expense_id))
    os.makedirs(folder, exist_ok=True)
    receipt.save(os.path.join(folder, filename))
    return jsonify(stored=filename), 201
