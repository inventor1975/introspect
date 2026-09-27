"""Small HTML fragment builders shared by the widget views."""
from markupsafe import escape


def render_card(title, body):
    return (
        '<div class="card"><h3>' + title + "</h3>"
        '<div class="card-body">' + body + "</div></div>"
    )


def render_tile(label, value):
    return '<div class="tile"><span>%s</span><b>%s</b></div>' % (
        escape(label),
        escape(value),
    )
