import html

from flask import Flask, request

app = Flask(__name__)


@app.route("/dashboard/chart")
def chart():
    limit = request.args.get("limit", "50")
    series = html.escape(request.args.get("series", "cpu"))
    return f"""
<div id="chart" data-series="{series}"></div>
<script>
  var chartLimit = {html.escape(limit)};
  renderChart(document.getElementById("chart"), chartLimit);
</script>
"""
