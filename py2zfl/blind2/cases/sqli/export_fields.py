import csv
import io

from flask import Flask, Response, abort, request

from lib.db import get_db

app = Flask(__name__)
ALLOWED = {"id", "email", "created_at", "plan"}


@app.route("/admin/export/fields")
def export_fields():
    requested = request.args.get("cols", "id,email").split(",")
    cols = []
    for c in requested:
        c = c.strip()
        if c not in ALLOWED:
            abort(400, description=f"unknown column {c}")
        cols.append(c)
    sql = "SELECT %s FROM subscribers ORDER BY id" % ", ".join(cols)
    rows = get_db().execute(sql).fetchall()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(cols)
    writer.writerows(rows)
    return Response(buf.getvalue(), mimetype="text/csv")
