from django.conf.urls import url
from . import views


urlpatterns	= [
    url(r'^(?P<get_id>[0-9]*)/posts', views.posts, name='posts'),
    #url(r'post', views.post, name='post'),
    url(r'^(?P<get_id>[0-9]*)/post', views.post, name='post'),
    url(r'^(?P<get_id>[0-9]*)/comments', views.comments, name='comments'),
    url(r'^(?P<get_id>[0-9]*)/comment', views.comment, name='comment'),


]