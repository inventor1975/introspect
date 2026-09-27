from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from .models import Comment, Post


@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Comment.objects.create(post=post, author=request.user, body=request.POST["body"])
    return redirect("post_detail", pk=pk)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = [
        {"author": c.author.username, "html": mark_safe(c.body)}
        for c in post.comments.order_by("created")
    ]
    return render(request, "blog/post_detail.html", {"post": post, "comments": comments})
