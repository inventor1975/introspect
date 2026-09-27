def clamp_limit(raw, default=20, maximum=100):
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    return max(1, min(value, maximum))


def page_offset(raw_page, limit):
    try:
        page = int(raw_page)
    except (TypeError, ValueError):
        page = 1
    return max(page - 1, 0) * limit
