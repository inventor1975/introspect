from flask import Flask, render_template_string, request

app = Flask(__name__)

NOTICE_TEMPLATE = (
    "<div class='notice notice-{{ level }}'>"
    "{% autoescape false %}{{ message }}{% endautoescape %}"
    "</div>"
)


@app.route("/notice")
def notice():
    level = request.args.get("level", "info")
    if level not in ("info", "warn", "error"):
        level = "info"
    message = request.args.get("msg", "")
    return render_template_string(NOTICE_TEMPLATE, level=level, message=message)
