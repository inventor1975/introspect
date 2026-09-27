"""Small WHERE-clause builders used by the listing endpoints."""


def build_where_clause(filters):
    """Turn {'city': 'Oslo', 'tier': 'gold'} into ' WHERE city = 'Oslo' AND tier = 'gold''."""
    parts = []
    for column, value in filters.items():
        if value in (None, ""):
            continue
        parts.append("%s = '%s'" % (column, value))
    if not parts:
        return ""
    return " WHERE " + " AND ".join(parts)


def build_param_where(filters, allowed):
    """Build a placeholder WHERE clause for the allowed columns only.

    Returns (clause, params) for a qmark-style driver.
    """
    parts, params = [], []
    for column in allowed:
        value = filters.get(column)
        if value in (None, ""):
            continue
        parts.append(f"{column} = ?")
        params.append(value)
    clause = (" WHERE " + " AND ".join(parts)) if parts else ""
    return clause, params
