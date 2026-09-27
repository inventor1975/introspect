import bleach
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from .models import Article

ALLOWED_TAGS = {"p", "b", "i", "em", "strong", "ul", "ol", "li", "blockquote"}


@require_POST
def save_article(request):
    body = bleach.clean(request.POST["body"], tags=ALLOWED_TAGS, attributes={}, strip=True)
    article = Article.objects.create(title=request.POST["title"], body=body)
    return redirect("show_article", pk=article.pk)


def show_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return HttpResponse(
        format_html("<h1>{}</h1><div class='body'>{}</div>", article.title, mark_safe(article.body))
    )
