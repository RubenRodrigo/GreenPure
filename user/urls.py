from django.conf.urls import url
from django.urls import path
from .views import BlacklistTokenUpdateView, CustomAccountCreate, DetailUser

app_name = 'users'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailUser.as_view()),
    path('create/', CustomAccountCreate.as_view(), name="create_user"),
    path('signout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
