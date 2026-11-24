import os
from flask import Flask, request
app = Flask(__name__)
ALLOWED = ("a.txt", "b.txt")

@app.route("/cat")
def cat():
    f = request.args.get("f")                          # read once into a local
    if f in ALLOWED:
        os.system("cat " + f)                          # EXPECT EARNED: the checked copy is the used copy
    return "ok"
