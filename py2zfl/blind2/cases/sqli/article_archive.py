from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Article


@require_GET
def archive(request):
    year = request.GET.get("year", "2024")
    articles = Article.objects.raw(
        "SELECT id, title, published FROM blog_article "
        "WHERE EXTRACT(YEAR FROM published) = " + year + " ORDER BY published DESC"
    )
    return JsonResponse(
        {"year": year, "articles": [{"id": a.id, "title": a.title} for a in articles]}
    )
