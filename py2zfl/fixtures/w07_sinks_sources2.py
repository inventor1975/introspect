import tempfile
from flask import Flask, request
from urllib.parse import unquote
from markupsafe import escape
app = Flask(__name__)

@app.route("/a")
def a():
    j = request.get_json(force=True)
    conn.exec_driver_sql(f"SELECT * FROM t WHERE k='{j['k']}'")        # EXPECT: REFUTED (get_json; exec_driver_sql)
    tempfile.NamedTemporaryFile(prefix=request.headers["X-P"], dir="/tmp/up")   # EXPECT: REFUTED (prefix=../x)
    return unquote(str(escape(request.args["q"])))                     # EXPECT: REFUTED (decoding undoes the escape)
