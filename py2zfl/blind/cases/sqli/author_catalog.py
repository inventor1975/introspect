from django.shortcuts import render
from django.views.decorators.http import require_GET

from library.models import Author
from lib.reporting import author_totals_query


@require_GET
def author_catalog(request):
    author = request.GET.get("author", "")
    authors = []
    if author:
        sql, params = author_totals_query(author)
        authors = Author.objects.raw(sql, params)
    return render(request, "library/author_catalog.html", {"authors": authors})
