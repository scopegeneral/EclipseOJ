from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    This form is for creatimg Posts/Discussion threads on the system. It's a ModelForm i.e. it instantiates the Post object
    """
    class Meta:
        model = Post
        fields = ('title', 'body',)

class CommentForm(forms.ModelForm):
    """
    This form is for creating comments on a discussion thread. It's a ModelForm i.e. it instantiates the Comment object
    """
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'Add Comment',
        }
