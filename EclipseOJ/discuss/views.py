from django.shortcuts import render
from .models import Post, Comment

def discuss_index(request):
    all_posts = Post.objects.all()
    return render(request, "discuss/index.html", {'all_posts' : all_posts})

def post_detail(request, postID):
    try:
        post = Post.objects.get(post_ID = postID)
    except Post.DoesNotExist:
        raise Http404("There is no post with this ID. Please verify")
    args = {}
    args['post'] = post
    args['all_comments'] = post.comment_set.order_by('-time')
    return render(request, "discuss/post_detail.html", args)
