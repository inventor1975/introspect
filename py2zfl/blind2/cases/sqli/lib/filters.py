"""Small helpers for turning query-string filters into SQL fragments."""


def build_where(field_map):
    parts = []
    for column, value in field_map.items():
        parts.append("%s = '%s'" % (column, value))
    if not parts:
        return "1=1"
    return " AND ".join(parts)


def like_pattern(term):
    term = term.strip()
    return "%" + term + "%"
