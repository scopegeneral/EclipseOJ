from django.conf.urls import url
from . import views as discuss_views

urlpatterns = [
    url(r'^$', discuss_views.discuss_index, name='discuss_index'),
    url(r'(?P<postID>[0-9]+)/$', discuss_views.post_detail, name='discuss_post'),
]
