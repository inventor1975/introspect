from flask import Flask, abort, jsonify, request

app = Flask(__name__)

BLOCKED = ("import", "os.", "sys.", "subprocess", "exec", "eval")


def is_suspicious(expression):
    lowered = expression.lower()
    return any(word in lowered for word in BLOCKED)


@app.route("/calculator", methods=["POST"])
def calculator():
    expression = request.form.get("q", "")
    if is_suspicious(expression):
        abort(403)
    return jsonify(result=eval(expression))
