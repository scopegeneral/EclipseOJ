from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as accounts_views


urlpatterns = [
    url(r'^login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=False), name='login'),
    url(r'^login/?next=(?P<next>[0-9a-zA-Z_/]+)', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_field_name=next), name='login_direct'),
    url(r'^logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    url(r'^signup/', accounts_views.signup, name='signup'),
]
