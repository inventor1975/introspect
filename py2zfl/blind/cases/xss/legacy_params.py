import functools
import html

from flask import Flask, Response, request

app = Flask(__name__)


def with_query_params(*names):
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            for n in names:
                kwargs[n] = request.args.get(n, "")
            return view(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/legacy/label")
@with_query_params("label", "color")
def legacy_label(label, color):
    body = '<span style="color:%s">%s</span>' % (html.escape(color), label)
    return Response(body, mimetype="text/html")
