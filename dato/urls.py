from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dato/$', views.Datos_list),
    url(r'^dato/(?P<pk>[0-9]+)/$', views.Dato_detail),
    url('respuesta', views.respuesta, name='respuesta'),
    url('resumen', views.resumen, name='resumen'),
    url(r'^ciudad/(?P<pk>[0-9]+)/$', views.ciudad),
    url('ciudades',views.ciudades, name='ciudades'),
    url(r'^distritoDatos/(?P<pk>[0-9]+)/$', views.distritoDatos),
    url('distritos', views.distritos, name='distritos'),
    url('mapa', views.distritosMapa, name='distritosMapa'),
    url('inscribir', views.inscribir, name='inscribir'),
]