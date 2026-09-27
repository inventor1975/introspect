import json

from flask import Flask, jsonify, request

app = Flask(__name__)


def parse_value(raw):
    try:
        return json.loads(raw)
    except ValueError:
        return eval(raw)


@app.route("/settings/<key>", methods=["PUT"])
def update_setting(key):
    raw = request.get_data(as_text=True)
    value = parse_value(raw)
    return jsonify({key: value})
