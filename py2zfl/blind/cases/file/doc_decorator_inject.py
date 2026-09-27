import functools
import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)
DOC_ROOT = "/srv/app/handbook"


def with_document(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        doc = request.args.get("doc")
        if doc is None:
            abort(400)
        kwargs["doc"] = doc
        return view(*args, **kwargs)

    return wrapper


@app.route("/handbook")
@with_document
def handbook(doc):
    return send_file(os.path.join(DOC_ROOT, doc))
