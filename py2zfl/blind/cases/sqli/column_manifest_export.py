import csv
import io
import json
import sqlite3
from pathlib import Path

from flask import Flask, Response, request

app = Flask(__name__)
MANIFEST = Path(__file__).with_name("export_columns.json")


def load_columns(kind):
    with MANIFEST.open(encoding="utf-8") as fh:
        return json.load(fh)[kind]


@app.route("/export/<kind>")
def export(kind):
    columns = load_columns("customers" if kind == "customers" else "orders")
    since = request.args.get("since", "1970-01-01")
    conn = sqlite3.connect("crm.db")
    cur = conn.execute(
        f"SELECT {', '.join(columns)} FROM {'customers' if kind == 'customers' else 'orders'} "
        "WHERE updated_at >= ?",
        (since,),
    )
    buf = io.StringIO()
    csv.writer(buf).writerows([columns, *cur.fetchall()])
    conn.close()
    return Response(buf.getvalue(), mimetype="text/csv")
