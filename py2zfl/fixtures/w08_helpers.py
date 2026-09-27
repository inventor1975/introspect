import re
from flask import Flask, request, abort
app = Flask(__name__)
ALLOWED = frozenset({"terms", "privacy"})
WORD = re.compile(r"[a-z]+")

class Repo:
    def search(self, q):
        cur.execute("SELECT * FROM s WHERE q='" + q + "'")

def repository():
    return Repo()

def guarded_open(name):
    if name not in ALLOWED:          # a module-level set, used INSIDE a summarised helper
        raise ValueError(name)
    return open("/srv/" + name)

def build(region):
    return "SELECT * FROM sales WHERE region = %s", [region]

@app.route("/h")
def h():
    repository().search(request.args["q"])            # EXPECT: REFUTED (a method on a call's result)
    guarded_open(request.args["n"])                    # clean: the helper's guard holds
    sql, params = build(request.args["r"])
    cur.execute(sql, params)                           # clean: only the params carry the value
    for v in (request.args["a"], request.args["b"]):
        pass
    a, b = request.args["a"], request.args["b"]
    for v in (a, b):
        if not WORD.fullmatch(v):
            abort(400)
    open("/srv/" + a + b)                              # clean: each passed the check in the loop
    return "ok"
