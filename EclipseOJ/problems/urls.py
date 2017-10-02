from django.conf.urls import url, include
from . import views as problems_views

urlpatterns = [
    url(r'^$', problems_views.index, name='index'),
    url(r'^(?P<problemID>[0-9]+[A-E])/$', problems_views.problem, name='problem'),
]
