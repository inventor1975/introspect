import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

SORT_COLUMNS = {
    "region": "region",
    "product": "product",
    "total": "SUM(amount)",
    "orders": "COUNT(*)",
}


@app.route("/reports/revenue")
def revenue_report():
    sort_key = request.args.get("sort", "total")
    order_by = SORT_COLUMNS.get(sort_key, "SUM(amount)")
    descending = request.args.get("dir", "desc").lower() == "desc"
    query = (
        "SELECT region, product, SUM(amount), COUNT(*) FROM sales GROUP BY region, product "
        "ORDER BY {} {}".format(order_by, "DESC" if descending else "ASC")
    )
    conn = psycopg2.connect("dbname=reports user=reports")
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    conn.close()
    return render_template("reports/revenue.html", rows=rows, sort=sort_key)
