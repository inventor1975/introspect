from flask import Flask, make_response, request
from markupsafe import escape

app = Flask(__name__)


class HtmlLayout:
    def __init__(self, title):
        self.title = title
        self.parts = []

    def add_paragraph(self, text):
        self.parts.append("<p>%s</p>" % escape(text))
        return self

    def render(self):
        return "<html><head><title>%s</title></head><body>%s</body></html>" % (
            escape(self.title),
            "".join(self.parts),
        )


@app.route("/memo")
def memo():
    layout = HtmlLayout(request.args.get("title", "Memo"))
    for line in request.args.get("body", "").splitlines():
        layout.add_paragraph(line)
    return make_response(layout.render())
