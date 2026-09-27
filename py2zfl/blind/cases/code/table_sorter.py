from flask import Flask, abort, jsonify, request

app = Flask(__name__)

SORTABLE = ("name", "created", "size", "owner")


class Record:
    def __init__(self, name, created, size, owner):
        self.name, self.created, self.size, self.owner = name, created, size, owner


RECORDS = [Record("a.txt", 3, 120, "kim"), Record("b.txt", 1, 40, "lee")]


@app.route("/files")
def files():
    field = request.args.get("sort", "name")
    if field not in SORTABLE:
        abort(400)
    key = eval(f"lambda r: r.{field}")
    return jsonify([r.__dict__ for r in sorted(RECORDS, key=key)])
