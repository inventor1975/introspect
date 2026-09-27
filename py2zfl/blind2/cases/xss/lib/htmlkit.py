"""Small HTML building blocks shared by the storefront views."""
from html import escape


def card(title, body, css="card"):
    return (
        f'<div class="{css}">'
        f"<h3>{title}</h3>"
        f'<div class="card-body">{body}</div>'
        "</div>"
    )


def card_escaped(title, body, css="card"):
    return card(escape(title), escape(body), css)


def table_row(cells):
    return "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"


def page(title, content):
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{escape(title)}</title></head><body>{content}</body></html>"
    )
