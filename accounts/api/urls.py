from django.conf.urls import url
from django.contrib import admin

from .views import (
    CreateUserApiView,
    LoginUserApiView,
    )

urlpatterns = [
    url(r'^login/$', LoginUserApiView.as_view(), name='login'),
    url(r'^register/$', CreateUserApiView.as_view(), name='register'),
]