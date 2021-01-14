from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dato/$', views.Datos_list),
    url(r'^dato/(?P<pk>[0-9]+)/$', views.Dato_detail),
    url('respuesta', views.humedad, name='respuesta'),
    url('resumen', views.resumen, name='resumen'),
    url('ciudades', views.ciudades, name='ciudades'),
    url(r'^ciudad/(?P<pk>[0-9]+)/$', views.ciudad),
    url(r'^distrito/(?P<pk>[0-9]+)/$', views.distrito),
]