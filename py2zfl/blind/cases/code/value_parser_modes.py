import ast

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

PARSERS = {
    "literal": ast.literal_eval,
    "number": float,
    "expr": eval,
}


@app.route("/convert")
def convert():
    mode = request.args.get("mode", "literal")
    parser = PARSERS.get(mode)
    if parser is None:
        abort(400)
    return jsonify(value=parser(request.args["value"]))
