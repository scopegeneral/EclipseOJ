from django.conf.urls import url
from . import views
urlpatterns =[
    url(r'^$', views.index, name="index"),
    url(r'^search/(?P<userID>\w*)/(?P<countryID>\w*)/(?P<cityID>\w*)/(?P<instiID>\w*)', views.search, name="search"),
#    url(r'^contest/(?P<contestID>[0-9]+)', views.contest_ranks, name="contest_ranks"),
]
