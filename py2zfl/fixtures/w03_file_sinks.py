import os, shutil
from pathlib import Path
from flask import Flask, request, send_file
app = Flask(__name__)
BASE = Path("/srv/files")

@app.route("/f")
def f():
    name = request.args["name"]
    send_file(os.path.join("/srv", name))    # EXPECT: REFUTED
    (BASE / name).read_text()                # EXPECT: REFUTED
    os.remove(name)                          # EXPECT: REFUTED
    return "ok"
