import datetime

from flask import Flask
from markupsafe import Markup

app = Flask(__name__)
app.config.from_envvar("SITE_SETTINGS", silent=True)


@app.route("/footer")
def footer():
    footer_html = Markup(app.config.get("FOOTER_HTML", ""))
    year = datetime.date.today().year
    return Markup("<footer>{}<small>&copy; {}</small></footer>").format(footer_html, year)
