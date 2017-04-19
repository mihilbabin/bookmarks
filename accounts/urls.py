from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # url(r'^login/$', views.user_login, name="user_login")
    url(r'^login/$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^password-change/$', auth_views.password_change, {'post_change_redirect': 'password_change_done'}, name='password_change'),
    url(r'^password-change-done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password-reset/$', auth_views.password_reset, {'post_reset_redirect': 'password_reset_done'}, name='password_reset'),
    url(r'^password-reset-done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit_profile, name='edit'),
    url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),
    url(r'^follow/$', views.user_follow, name='user_follow')
]
