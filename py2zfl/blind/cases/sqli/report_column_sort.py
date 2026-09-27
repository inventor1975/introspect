import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)


def pg():
    return psycopg2.connect("dbname=reports user=reports")


@app.route("/reports/sales")
def sales_report():
    sort = request.args.get("sort", "region")
    direction = request.args.get("dir", "asc")
    query = (
        "SELECT region, product, SUM(amount) AS total FROM sales "
        "GROUP BY region, product ORDER BY {} {}".format(sort, direction)
    )
    with pg() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    return render_template("reports/sales.html", rows=rows, sort=sort, direction=direction)
