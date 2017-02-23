from django.conf.urls import url
from django.contrib import admin

from .views import (
    PostRetriveApiView,
    PostListApiView,
    PostUpdateApiView,
    PostDeleteApiView,
    PostCreateApiView,
	)

urlpatterns = [
	url(r'^$', PostListApiView.as_view(), name='list'),
    url(r'^create/$', PostCreateApiView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', PostRetriveApiView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateApiView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteApiView.as_view(), name='delete'),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
