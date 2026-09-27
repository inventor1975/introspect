from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/charts/series")
def chart_series():
    fn_src = request.args.get("fn", "x * x")
    xs = range(int(request.args.get("n", 10)))
    return jsonify(points=[_apply(fn_src, x) for x in xs])


def _apply(source, x):
    return eval(source, {"x": x})
