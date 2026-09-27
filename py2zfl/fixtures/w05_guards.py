import re
from flask import Flask, request, abort
app = Flask(__name__)
SORTABLE = ("name", "date")
IDENT = re.compile(r"[a-z_]+")

@app.route("/g")
def g():
    a = request.args["a"]
    if not a.isdigit():
        abort(400)
    eval(a)                                  # clean
    b = request.args["b"]
    if b not in SORTABLE:
        return "bad"
    eval(b)                                  # clean
    c = request.args["c"]
    if IDENT.fullmatch(c) is None:
        abort(400)
    eval(c)                                  # clean
    d = request.args["d"]
    try:
        int(d)
    except ValueError:
        d = "0"
    eval(d)                                  # clean
    e = request.args["e"]
    eval(e)                                  # EXPECT: REFUTED
    return "ok"
