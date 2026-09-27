"""Report definitions: each report is a fixed expression over the query parameters."""

REPORTS = {
    "margin": "(revenue - cost) / revenue if revenue else 0",
    "growth": "(current - previous) / previous if previous else 0",
    "average_order": "revenue / orders if orders else 0",
}


class UnknownReport(LookupError):
    pass


def run_report(name, params):
    try:
        expression = REPORTS[name]
    except KeyError:
        raise UnknownReport(name)
    numeric = {key: float(value) for key, value in params.items()}
    return eval(expression, {"__builtins__": {}}, numeric)
