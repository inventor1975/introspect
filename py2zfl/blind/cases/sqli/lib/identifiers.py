"""Identifier and LIKE-pattern helpers for SQLite."""


def quote_identifier(name):
    """Quote an SQLite identifier (table or column name) the standard way."""
    return '"' + str(name).replace('"', '""') + '"'


def escape_like(term, escape_char="\\"):
    """Escape LIKE wildcards so the term matches literally (use with ESCAPE)."""
    return (
        term.replace(escape_char, escape_char * 2)
        .replace("%", escape_char + "%")
        .replace("_", escape_char + "_")
    )
