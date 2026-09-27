from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/calc")
def calc():
    expr = request.args.get("expr", "0")
    try:
        value = eval(expr)
    except Exception as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(expr=expr, value=value)
