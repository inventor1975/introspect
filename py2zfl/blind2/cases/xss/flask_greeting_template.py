from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE = """
<!doctype html>
<title>Hi</title>
<div class="banner"><strong>Hello, {{ name }}!</strong></div>
<p>You have {{ unread }} unread messages.</p>
"""


@app.route("/hi")
def hi():
    name = request.args.get("name", "friend")
    unread = request.args.get("unread", "0")
    return render_template_string(PAGE, name=name, unread=unread)
