from flask import Flask, abort, jsonify, request

app = Flask(__name__)

ALLOWED_OPS = {"+", "-", "*", "/", "%", "//"}


@app.route("/arith")
def arith():
    op = request.args.get("op", "+")
    try:
        a = int(request.args["a"])
        b = int(request.args["b"])
    except (KeyError, ValueError):
        abort(400)
    if op in ALLOWED_OPS:
        result = eval(f"{a} {op} {b}")
        return jsonify(result=result)
    abort(400)
