from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    #url(r'^noone$', views.blog_id, name='blog_id'),
]
