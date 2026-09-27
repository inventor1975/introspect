import functools

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

KNOWN_METRICS = frozenset({"mean", "median", "stdev", "variance"})


def metric_param(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        metric = request.args.get("metric", "mean")
        if metric not in KNOWN_METRICS:
            abort(400, "unknown metric")
        return view(metric, *args, **kwargs)
    return wrapper


@app.route("/series/<int:series_id>/metric")
@metric_param
def series_metric(metric, series_id):
    import statistics

    data = [3.0, 4.5, 2.25, 8.0, 5.5]
    value = eval(f"statistics.{metric}(data)", {"statistics": statistics, "data": data})
    return jsonify(series=series_id, metric=metric, value=value)
