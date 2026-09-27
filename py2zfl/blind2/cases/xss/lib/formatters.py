"""Output formatters selectable per widget."""
from markupsafe import escape


def plain(value):
    return str(escape(value))


def emphasis(value):
    return f"<em>{escape(value)}</em>"


def rich(value):
    return value.replace("\n", "<br>")
