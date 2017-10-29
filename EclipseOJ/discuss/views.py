from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.template.context_processors import csrf
from django.utils import timezone

def discuss_index(request):
    """
    Display all the discussion threads present in the server. The are put sequentially based on time of creation of post.

    **Template:**

    :template:`discuss/index.html`
    """
    all_posts = Post.objects.all()
    return render(request, "discuss/index.html", {'all_posts' : all_posts})

def post_detail(request, postID):
    """
    Display the detailed view for a post. In general a post may be truncated to shorter length in the index view. So this view shows the complete post.
    It also displays the comments made by people on the post, Users can comment on a post by generating a post-request rendered through a django form.

    **Template:**

    :template:`discuss/post_detail.html`
    """
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
    """
    This view is basically a form through which user can create a post/discussion thread. Appropirate text fields have been provided to a django form
     
    **Template:**

    :template:`discuss/add_post.html`
    """
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
