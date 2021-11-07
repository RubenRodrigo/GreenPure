from django.conf.urls import url
from django.urls import path
from .views import CustomAccountCreate, DetailCurrent, DetailUser

app_name = 'users'

urlpatterns = [
    url(r'^$', DetailCurrent.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', DetailUser.as_view()),
    path('create/', CustomAccountCreate.as_view(), name="create_user"),
]
