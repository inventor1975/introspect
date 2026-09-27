from flask import Flask, render_template_string, request

app = Flask(__name__)

RESULTS = """
<h2>Results for <em>{{ q }}</em></h2>
{% for hit in hits %}<li>{{ hit }}</li>{% else %}<p>Nothing found.</p>{% endfor %}
"""


@app.route("/find")
def find():
    q = request.args.get("q", "")
    hits = [w for w in request.args.getlist("filter") if w]
    return render_template_string(RESULTS, q=q, hits=hits)
