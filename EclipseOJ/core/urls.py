from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/', signup, name='signup'),
    url(r'^update/$', ProfileUpdateView.as_view(), name='update_profile'),
    url(r'^change_password/$', auth_views.PasswordChangeView.as_view(template_name='core/change_password.html', success_url='profile'), name='change_password'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_@.+-]+)/$', other_profile, name='other_profile'),
    url(r'^profile/', profile, name='profile'),
]
