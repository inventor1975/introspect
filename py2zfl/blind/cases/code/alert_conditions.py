from flask import Flask, jsonify, request

app = Flask(__name__)


def current_metrics():
    return {"cpu": 71.5, "mem": 43.0, "disk": 88.2}


@app.route("/alerts/evaluate")
def evaluate_alerts():
    conditions = {name: cond for name, cond in request.args.items() if name.startswith("alert_")}
    metrics = current_metrics()
    fired = []
    for name, cond in conditions.items():
        if eval(cond, {"__builtins__": None}, metrics):
            fired.append(name[len("alert_"):])
    return jsonify(fired=fired)
