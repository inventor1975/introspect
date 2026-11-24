import os
from flask import Flask, request, abort
app = Flask(__name__)
ALLOWED = ("a.txt", "b.txt")

@app.route("/cat")
def cat():
    if request.args.get("f") not in ALLOWED:
        abort(400)
    os.system("cat " + request.args.get("f"))         # EXPECT EARNED IF STABLE: re-read after a rejecting check
    return "ok"
