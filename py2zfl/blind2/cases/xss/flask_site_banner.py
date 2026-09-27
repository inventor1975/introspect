from flask import Flask, current_app, request
from markupsafe import Markup, escape

app = Flask(__name__)
app.config.from_envvar("STOREFRONT_SETTINGS", silent=True)


@app.route("/")
def home():
    banner = Markup(current_app.config.get("BANNER_HTML", ""))
    visitor = escape(request.args.get("ref", ""))
    return Markup("<header>{}</header><main><p>Welcome{}</p></main>").format(
        banner, Markup(", visitor from {}").format(visitor) if visitor else ""
    )
