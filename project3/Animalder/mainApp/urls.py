from django.urls import path
from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'home.html'} ,name='logout'),
    url(r'^profile/(?P<username>.+)$', views.profile, name='profile'),
    url('profile', views.selfProfile, name='profile'),
    path('rate/', views.rate, name='rate'),
    url(r'^rate/(?P<ratedUserID>.+)/$', views.rate, name='rate'),
    path('matches/', views.matches, name='matches'),
    path('mailbox/', views.mailbox, name='mailbox'),
    url(r'^message/(?P<username>.+)/$', views.message, name='message'),
    path('menu/', views.menu, name='menu'),
    path('', views.home, name='home'),
]