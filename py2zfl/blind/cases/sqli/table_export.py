import csv
import io
import sqlite3

from flask import Flask, Response, request

from lib.identifiers import quote_identifier

app = Flask(__name__)


@app.route("/export")
def export_table():
    table = request.args.get("table", "contacts")
    conn = sqlite3.connect("crm.db")
    cur = conn.execute(f"SELECT * FROM {quote_identifier(table)}")
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([d[0] for d in cur.description])
    writer.writerows(cur.fetchall())
    conn.close()
    return Response(buf.getvalue(), mimetype="text/csv")
