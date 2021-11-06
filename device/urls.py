from django.conf.urls import url
from django.urls import path

from device.views import DeviceDetail, DeviceList, deviceActivate

urlpatterns = [
    url(r'^$', DeviceList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', DeviceDetail.as_view()),
    path('activate/<str:device>/', deviceActivate),
]
