from flask import Flask, request
from jinja2.utils import htmlsafe_json_dumps

app = Flask(__name__)


@app.route("/map")
def map_embed():
    options = {
        "place": request.args.get("place", "Lisbon"),
        "zoom": 12,
    }
    return (
        "<div id='map'></div>"
        "<script>initMap(" + str(htmlsafe_json_dumps(options)) + ");</script>"
    )
