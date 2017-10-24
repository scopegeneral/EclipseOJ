from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    title = models.CharField(max_length=250)
    body = models.TextField()
    time = models.DateTimeField()

    def __str__(self):
        return 'Post {}'.format(self.pk)

class Comment(models.Model):
    parent = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    body = models.TextField()
    time = models.DateTimeField()
