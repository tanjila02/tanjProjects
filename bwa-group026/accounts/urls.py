# accounts/urls.py
from django.urls import path, re_path
from django.contrib import admin
admin.autodiscover()

from . import views
from .views import UserProfileView


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', views.home, name = 'home'),
    re_path(r'^users/$', views.userlist, name = 'userlist'),
    re_path(r'^users/(?P<string>[\w.@+-]+)/request/$', views.request_friendship, name='friendrequest'),
    path('users/edit/', views.update_profile, name = 'edit_profile'),
    re_path(r'^users/(?P<string>[\w.@+-]+)/$', views.profile_page, name='user'),
    path('admin/', admin.site.urls),

################

    path('conversation/', views.chat_home, name='chat_home'),
    path('conversation/post/', views.post, name='post'),
    path('conversation/messages/', views.messages, name='messages'),

]
