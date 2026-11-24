import os
from flask import Flask, request
app = Flask(__name__)
ALLOWED = ("a.txt", "b.txt")

@app.route("/cat")
def cat():
    if request.args.get("f") in ALLOWED:              # f is checked ...
        os.system("cat " + request.args.get("g"))     # EXPECT REFUTED: ... g is used
    return "ok"
