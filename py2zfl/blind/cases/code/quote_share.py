from flask import Flask, request, render_template_string

app = Flask(__name__)


def as_literal(text):
    return "{% raw %}" + text + "{% endraw %}"


@app.route("/share")
def share_preview():
    quote = request.args.get("quote", "")
    author = request.args.get("author", "anonymous")
    source = "<blockquote>" + as_literal(quote) + "</blockquote><cite>{{ author }}</cite>"
    return render_template_string(source, author=author)
