from flask import Flask, jsonify, request

app = Flask(__name__)


def _pair(args):
    return args.get("left", "0"), args.get("right", "0")


@app.route("/compare")
def compare():
    left, right = _pair(request.args)
    op = "=="
    verdict = eval(f"({left}) {op} ({right})")
    return jsonify(left=left, right=right, equal=bool(verdict))
