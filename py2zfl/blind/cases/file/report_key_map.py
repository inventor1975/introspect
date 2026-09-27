from django.http import FileResponse, Http404

REPORT_FILES = {
    "monthly": "/srv/reports/monthly_summary.xlsx",
    "quarterly": "/srv/reports/quarterly_summary.xlsx",
    "annual": "/srv/reports/annual_summary.xlsx",
}


def download_report(request, period):
    try:
        path = REPORT_FILES[period]
    except KeyError:
        raise Http404("unknown report period")
    return FileResponse(open(path, "rb"), as_attachment=True, filename=f"{period}.xlsx")
