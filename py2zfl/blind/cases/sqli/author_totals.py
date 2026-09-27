from django.shortcuts import render
from django.views.decorators.http import require_GET

from library.models import Author
from lib.reporting import author_totals_sql


@require_GET
def author_totals(request):
    author = request.GET.get("author", "")
    authors = Author.objects.raw(author_totals_sql(author)) if author else []
    return render(request, "library/author_totals.html", {"authors": authors})
