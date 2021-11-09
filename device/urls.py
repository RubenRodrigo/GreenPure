from django.conf.urls import url
from django.urls import path

from device.views import DeviceDetail, DeviceList, DeviceResumeDetail, deviceActivate

urlpatterns = [
    url(r'^$', DeviceList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', DeviceDetail.as_view()),
    path('resume/', DeviceResumeDetail.as_view()),
    path('activate/<str:device>/', deviceActivate),
]
