from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name="judge_index"),
    url(r'^(?P<username>[a-zA-Z0-9_@.+-]+)/$', views.userspecific, name='mysubmissions'),
]
