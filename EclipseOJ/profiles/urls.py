from django.conf.urls import url
from . import views as profiles_views

urlpatterns = [
    url(r'^$', profiles_views.index, name='index'),
    url(r'^update/$', profiles_views.ProfileUpdateView.as_view(), name='profiles_update'),
    url(r'^change_password/$', profiles_views.change_password, name='change_password'),
    url(r'^(?P<nickname>[a-zA-Z0-9_@.+-]+)/$', profiles_views.detail, name='detail'),
]
