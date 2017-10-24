from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.template.context_processors import csrf
from django.utils import timezone

def discuss_index(request):
    all_posts = Post.objects.all()
    if all_posts:
        return render(request, "discuss/index.html", {'all_posts' : all_posts})
    else:
        args = {}
        args['warning'] = "No posts at the moment"
        args['message'] = "Please check again later."
        return render(request, "warning.html", )

def post_detail(request, postID):
    try:
        post = Post.objects.get(pk = postID)
    except Post.DoesNotExist:
        args = {}
        args['warning'] = "No such post found"
        args['message'] = "Please verify your details and try again."
        return render(request, "warning.html", args)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.parent = post
            comment.time = timezone.now()
            comment.save()
            return redirect('post_detail', postID=post.pk)
    comment_form = CommentForm()
    args = {}
    args.update(csrf(request))
    args['post'] = post
    args['all_comments'] = post.comment_set.order_by('-time')
    args['comment_form'] = comment_form
    return render(request, "discuss/post_detail.html", args)

def add_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.time = timezone.now()
            post.save()
            return redirect('post_detail', postID=post.pk)
    else:
        post_form = PostForm()
        args = {}
        args.update(csrf(request))
        args['post_form'] = post_form
        return render(request, "discuss/add_post.html", args)
