import csv
import io

from flask import Flask, Response, request

from lib.db import get_db

app = Flask(__name__)
ALLOWED = {"id", "email", "created_at", "plan"}


@app.route("/admin/export")
def export():
    cols = request.args.get("cols", "id,email").split(",")
    for c in cols:
        if c not in ALLOWED:
            app.logger.warning("unexpected export column %r", c)
    sql = "SELECT %s FROM subscribers ORDER BY id" % ", ".join(cols)
    rows = get_db().execute(sql).fetchall()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(cols)
    writer.writerows(rows)
    return Response(buf.getvalue(), mimetype="text/csv")
