from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def comment_form(request):
    context = {"submitted": False}
    if request.method == "POST":
        comment = request.POST.get("comment", "").strip()
        context["submitted"] = True
        context["comment_html"] = mark_safe(comment.replace("\n", "<br>"))
    return render(request, "comments/form.html", context)
