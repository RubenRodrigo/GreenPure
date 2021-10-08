from django.conf.urls import url
from .views import DetailUser

app_name = 'users'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', DetailUser.as_view()),
]
