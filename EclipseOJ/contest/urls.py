from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<contestID>[0-9]+)/$', views.contest, name='contest'),
]
