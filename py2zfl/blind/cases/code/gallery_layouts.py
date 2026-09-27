from flask import Flask, abort, request, render_template_string

app = Flask(__name__)

LAYOUTS = {
    "grid": "<div class='grid'>{% for p in photos %}<img src='{{ p }}'>{% endfor %}</div>",
    "list": "<ul>{% for p in photos %}<li><a href='{{ p }}'>{{ p }}</a></li>{% endfor %}</ul>",
    "carousel": "<div class='carousel' data-count='{{ photos|length }}'></div>",
}


@app.route("/gallery")
def gallery():
    try:
        source = LAYOUTS[request.args.get("layout", "grid")]
    except KeyError:
        abort(400)
    photos = request.args.getlist("photo")
    return render_template_string(source, photos=photos)
