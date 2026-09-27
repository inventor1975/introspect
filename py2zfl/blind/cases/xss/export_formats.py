from flask import Flask, abort, make_response, request
from markupsafe import escape

app = Flask(__name__)


class Exporter:
    def as_table(self, rows):
        cells = "".join("<tr><td>%s</td></tr>" % escape(r) for r in rows)
        return "<table>" + cells + "</table>"

    def as_list(self, rows):
        return "<ul>" + "".join("<li>%s</li>" % r for r in rows) + "</ul>"

    def as_lines(self, rows):
        return "<br>".join(escape(r) for r in rows)


@app.route("/export")
def export():
    fmt = request.args.get("format", "table")
    rows = request.args.getlist("row")
    handler = getattr(Exporter(), "as_" + fmt, None)
    if handler is None:
        abort(404)
    return make_response(handler(rows))
