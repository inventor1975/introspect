from datetime import datetime

from flask import Flask, request, render_template_string

app = Flask(__name__)


class Notice:
    def __init__(self, text, author):
        self.text = text
        self.author = author
        self.posted = datetime.utcnow()

    def html(self):
        return render_template_string(
            "<article>" + self.text + "<footer>{{ a }} &middot; {{ t }}</footer></article>",
            a=self.author,
            t=self.posted.strftime("%Y-%m-%d"),
        )


@app.route("/notices/preview", methods=["POST"])
def preview_notice():
    notice = Notice(request.form["text"], request.form.get("author", "staff"))
    return notice.html()
