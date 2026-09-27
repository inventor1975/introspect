from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Article


@require_GET
def archive_by_year(request):
    year = request.GET.get("year", "2024")
    articles = Article.objects.raw(
        "SELECT id, title, published FROM blog_article "
        "WHERE EXTRACT(YEAR FROM published) = %s ORDER BY published DESC",
        [year],
    )
    return JsonResponse(
        {"year": year, "articles": [{"id": a.id, "title": a.title} for a in articles]}
    )
