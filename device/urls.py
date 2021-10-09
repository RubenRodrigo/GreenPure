from django.conf.urls import url

from device.views import DeviceDetail, DeviceList

urlpatterns = [
    url(r'^$', DeviceList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', DeviceDetail.as_view()),
]
