from django.conf.urls import url
from accounts import views, auth_views
from django.contrib.auth.views import password_change, password_change_done

urlpatterns = [
    url(r'^accounts/register/$', views.UserRegisterView.as_view(), name='user_register'),
    url(r'^accounts/login/$', views.UserLoginView.as_view(), name='user_login'),
    url(r'^accounts/logout/$', views.user_logout, name='user_logout'),
    url(r'^accounts/(?P<pk>\d+)/change/$', views.user_account, name='user_account'),

    url(r'^accounts/password/reset/$', views.user_password_reset, name='user_password_reset'),
    url(r'^accounts/password/reset/done/$', views.user_password_reset_done, name='user_password_reset_done'),
    url(r'^accounts/password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.user_password_reset_confirm,
        name='user_password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$', views.user_password_reset_complete, name='user_password_reset_complete'),

    url(r'^accounts/password/change/$', views.user_password_change, name='user_password_change'),
    url(r'^accounts/password/change/done/$', views.user_password_change_done, name='user_password_change_done'),

    url(r'^accounts/auth/google/login/$', auth_views.google_login, name='google_login'),
    url(r'^accounts/auth/github/login/$', auth_views.github_login, name='github_login'),

    url(r'^auth/google/callback/$', auth_views.google_callback, name='google_callback'),
    url(r'^auth/github/callback/$', auth_views.github_callback, name='github_callback'),
]
