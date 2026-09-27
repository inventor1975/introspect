from django.shortcuts import render

from blog.models import Article


def archive_by_year(request):
    year = request.GET.get("year", "2024")
    articles = Article.objects.raw(
        "SELECT * FROM blog_article WHERE strftime('%%Y', published_at) = '%s' "
        "ORDER BY published_at DESC" % year
    )
    return render(request, "blog/archive.html", {"articles": articles, "year": year})
