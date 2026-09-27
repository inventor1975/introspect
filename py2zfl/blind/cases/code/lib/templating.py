"""Small wrappers around Flask template rendering."""
from flask import render_template_string


def render_snippet(source, **context):
    context.setdefault("site_name", "Acme")
    return render_template_string(source, **context)
