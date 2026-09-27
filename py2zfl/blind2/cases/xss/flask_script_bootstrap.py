from flask import Flask, render_template_string, request

app = Flask(__name__)

BOOT = """
<div id="app"></div>
<script>
  window.__INITIAL_QUERY__ = {{ q|tojson }};
  window.__SORT__ = {{ sort|tojson }};
</script>
<script src="/static/app.js"></script>
"""


@app.route("/app")
def spa_shell():
    return render_template_string(
        BOOT, q=request.args.get("q", ""), sort=request.args.get("sort", "recent")
    )
