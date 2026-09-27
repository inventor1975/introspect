from django.shortcuts import render

from blog.models import Article


def search(request):
    q = request.GET.get("q", "").strip()
    articles = []
    if q:
        articles = Article.objects.raw(
            "SELECT * FROM blog_article WHERE title LIKE %s OR summary LIKE %s "
            "ORDER BY published_at DESC",
            [f"%{q}%", f"%{q}%"],
        )
    return render(request, "blog/search.html", {"articles": articles, "q": q})
