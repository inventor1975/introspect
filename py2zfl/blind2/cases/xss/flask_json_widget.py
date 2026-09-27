from flask import Flask, request

app = Flask(__name__)


def render_list(title, items):
    out = [f"<h4>{title}</h4>", "<ul>"]
    for item in items:
        out.append("<li>%s</li>" % item.get("label", ""))
    out.append("</ul>")
    return "".join(out)


@app.post("/api/widgets/list")
def widget_list():
    payload = request.get_json(force=True) or {}
    html_fragment = render_list(payload.get("title", "List"), payload.get("items", []))
    return html_fragment, 200, {"Content-Type": "text/html; charset=utf-8"}
