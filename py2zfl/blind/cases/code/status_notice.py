from string import Template

from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = "<div class='notice'>{{ notice }}</div><small>{{ when }}</small>"


@app.route("/status/notice", methods=["POST"])
def status_notice():
    message = Template(request.form.get("message", "Service $service is $state"))
    text = message.safe_substitute(
        service=request.form.get("service", "api"),
        state=request.form.get("state", "operational"),
    )
    return render_template_string(PAGE, notice=text, when="just now")
