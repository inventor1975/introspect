import os
from flask import Flask, request
app = Flask(__name__)
ALLOWED = ("a.txt", "b.txt")

@app.route("/cat")
def cat():
    if request.args.get("f") in ALLOWED:              # the check reads the source once ...
        os.system("cat " + request.args.get("f"))     # EXPECT EARNED IF STABLE: ... the use reads it again
    return "ok"
