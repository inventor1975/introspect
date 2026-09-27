import psycopg2
from psycopg2.extensions import quote_ident
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/admin/column-stats")
def column_stats():
    column = request.args.get("column", "country")
    with psycopg2.connect(dbname="crm") as conn:
        with conn.cursor() as cur:
            ident = quote_ident(column, cur)
            cur.execute(
                "SELECT " + ident + ", COUNT(*) FROM contacts GROUP BY " + ident + " ORDER BY 2 DESC LIMIT 20"
            )
            rows = cur.fetchall()
    return jsonify([[r[0], r[1]] for r in rows])
