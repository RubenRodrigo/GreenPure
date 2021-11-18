from django.conf.urls import url
from .views import CityDetail, CountryDetail, DataDetail, DataList, DataListAll, DistrictDetail

urlpatterns = [
    url(r'^$', DataList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', DataDetail.as_view()),
    url(r'^country/(?P<pk>[0-9]+)/$', CountryDetail.as_view()),
    url(r'^city/(?P<pk>[0-9]+)/$', CityDetail.as_view()),
    url(r'^district/(?P<pk>[0-9]+)/$', DistrictDetail.as_view()),

    url(r'^all/$', DataListAll.as_view()),
    # url(r'^dato/(?P<pk>[0-9]+)/$', views.Dato_detail),
    # url('respuesta', views.respuesta, name='respuesta'),
    # url('resumen', views.resumen, name='resumen'),
    # url(r'^ciudad/(?P<pk>[0-9]+)/$', views.ciudad),
    # url('ciudades',views.ciudades, name='ciudades'),
    # url(r'^distritoDatos/(?P<pk>[0-9]+)/$', views.distritoDatos),
    # url('distritos', views.distritos, name='distritos'),
    # url('mapa', views.distritosMapa, name='distritosMapa'),
    # url('inscribir', views.inscribir, name='inscribir'),
]
