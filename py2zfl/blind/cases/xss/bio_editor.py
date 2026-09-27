from flask import Flask, render_template_string, request

app = Flask(__name__)

BIO_TEMPLATE = """
<section class="bio">
  <h2>{{ username }}</h2>
  <div class="about">{{ about|safe }}</div>
</section>
"""


@app.route("/bio/preview", methods=["POST"])
def bio_preview():
    return render_template_string(
        BIO_TEMPLATE,
        username=request.form.get("username", ""),
        about=request.form.get("about", ""),
    )
