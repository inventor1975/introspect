from django.http import HttpResponse


def banner(request):
    title = request.GET.get("title", "Announcements")
    subtitle = request.GET.get("sub", "")
    markup = "<header><h2>%s</h2><small>%s</small></header>" % (title, subtitle)
    return HttpResponse(markup)
