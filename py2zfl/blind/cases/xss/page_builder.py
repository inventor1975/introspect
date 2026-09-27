from flask import Flask, make_response, request
from markupsafe import escape

app = Flask(__name__)


class HtmlPage:
    def __init__(self, title):
        self.title = title
        self.parts = []

    def add_paragraph(self, text):
        self.parts.append("<p>%s</p>" % text)
        return self

    def render(self):
        return "<html><head><title>%s</title></head><body>%s</body></html>" % (
            escape(self.title),
            "".join(self.parts),
        )


@app.route("/note")
def note():
    page = HtmlPage(request.args.get("title", "Note"))
    for line in request.args.get("body", "").splitlines():
        page.add_paragraph(line)
    return make_response(page.render())
