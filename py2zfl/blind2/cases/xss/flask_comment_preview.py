from flask import Flask, render_template_string, request

app = Flask(__name__)

PREVIEW = """
<section class="preview">
  <h4>{{ author }}</h4>
  <div class="comment-body">{{ body|safe }}</div>
</section>
"""


@app.route("/comments/preview", methods=["POST"])
def comment_preview():
    author = request.form.get("author", "guest")
    body = request.form.get("body", "").replace("\n", "<br>")
    return render_template_string(PREVIEW, author=author, body=body)
