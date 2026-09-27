from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = """<html>
<head><title>%(title)s | Docs</title></head>
<body>
  <h1>%(title)s</h1>
  {{ content|safe }}
</body>
</html>"""


def load_content(slug):
    return "<p>Documentation for %s</p>" % slug


@app.route("/docs/<slug>")
def docs_page(slug):
    title = request.args.get("title", slug.replace("-", " ").title())
    source = PAGE % {"title": title}
    return render_template_string(source, content=load_content(slug))
