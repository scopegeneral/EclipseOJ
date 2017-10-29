from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    A Post provides base to the discussion view. Users can discuss problems/solutions on the :view:`discuss.discuss_index` & the :view:`discuss.post_detail` pages. Post object are basic units used on those pges. Each time a a new discussion thread starts a new post object is created
    """
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        help_text="It is linked via ForeignKey to a user, which means that a post is uniquly linked to an User"
    )
    title = models.CharField(
        max_length=250,
        help_text="This is the title of the post/discussion thread",
    )
    body = models.TextField(
        help_text="This is the core body of the discussion thread using a TextField",
    )
    time = models.DateTimeField(
        help_text="This is a DateTimeField and is used to store the time at which the post has been created",
    )

    def __str__(self):
        return 'Post {}'.format(self.pk)

class Comment(models.Model):
    """
    If you want to reply to some :model:`discuss.Post` created by some user you can use the comment feature.
    """
    parent = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        help_text="A comment can only occur if a post has been created so a comment is linked via a foreign key to Post. on_delete = CASCADE has been set to true i.e. if a post is deleted then all it's related comments will also be deleted"
    )
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        help_text="It is linked via ForeignKey to a user, which means that a comment is uniquly linked to an User"
    )
    body = models.TextField(
        help_text="This is the core body of the discussion thread using a TextField",
    )
    time = models.DateTimeField(
        help_text="This is a DateTimeField and is used to store the time at which the comment has been created",    
    )
