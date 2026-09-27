import csv
import os

from flask import Flask, jsonify, request

app = Flask(__name__)
DATASET_DIR = "/srv/datasets"


@app.route("/datasets/preview")
def preview_dataset():
    name = request.args.get("dataset", "sample.csv").lstrip(".")
    path = os.path.join(DATASET_DIR, name)
    rows = []
    with open(path, newline="") as fh:
        for i, row in enumerate(csv.reader(fh)):
            if i >= 20:
                break
            rows.append(row)
    return jsonify({"dataset": name, "rows": rows})
