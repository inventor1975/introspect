from flask import Flask, jsonify, request

app = Flask(__name__)

SAFE_GLOBALS = {"__builtins__": {}}


@app.route("/grades/score")
def score():
    weights = request.args.get("weights", "0.5*exam + 0.3*hw + 0.2*quiz")
    marks = {"exam": 71.0, "hw": 88.0, "quiz": 93.0}
    total = eval(weights, SAFE_GLOBALS, marks)
    return jsonify(total=total)
