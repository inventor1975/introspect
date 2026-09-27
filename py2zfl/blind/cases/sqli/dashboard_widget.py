from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///metrics.db"
db = SQLAlchemy(app)


@app.route("/widgets/series")
def widget_series():
    ctx = {"bucket": "day", "limit": 30}
    ctx["metric"] = request.args["metric"]
    if request.args.get("bucket") == "week":
        ctx["bucket"] = "week"
    sql = (
        f"SELECT {ctx['bucket']} AS period, SUM({ctx['metric']}) AS value "
        f"FROM daily_metrics GROUP BY period ORDER BY period DESC LIMIT {ctx['limit']}"
    )
    rows = db.session.execute(text(sql)).all()
    return jsonify([{"period": p, "value": v} for p, v in rows])
