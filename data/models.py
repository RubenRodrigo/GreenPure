from django.db import models
from geopy.geocoders import Nominatim

from device.models import Device
from .funciones import *

# Create your models here.


class Country(models.Model):
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.country


class City(models.Model):
    city = models.CharField(max_length=100)
    country_id = models.ForeignKey(
        Country, related_name="city", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.city


class District(models.Model):
    city_id = models.ForeignKey(
        City, related_name="district", on_delete=models.SET_NULL, null=True, blank=True)
    district = models.CharField(max_length=100)

    def __str__(self):
        return self.district


class Data(models.Model):
    district_id = models.ForeignKey(
        District, related_name='data', on_delete=models.CASCADE, null=True, blank=True)
    device_id = models.ForeignKey(
        Device, related_name='data', on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    quality = models.IntegerField()
    date = models.DateField('Date')
    time = models.TimeField('Time')
    humidity = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperature = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    warm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    concentration = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    smoke_sensor = models.BooleanField(default=False)
    methane_sensor = models.BooleanField(default=False)

    def __str__(self):
        return str(self.quality)


# class Datos(models.Model):
#     Humedad = models.DecimalField(max_digits=6, decimal_places=2, default=0)
#     Temperatura = models.DecimalField(
#         max_digits=6, decimal_places=2, default=0)
#     Calor = models.DecimalField(max_digits=6, decimal_places=2, default=0)
#     Concentracion = models.DecimalField(
#         max_digits=6, decimal_places=2, default=0)
#     Latitud = models.DecimalField(max_digits=10, decimal_places=7, default=0)
#     Longitud = models.DecimalField(max_digits=10, decimal_places=7, default=0)
#     SensorHumo = models.BooleanField(default=False)
#     SensorMetano = models.BooleanField(default=False)
#     fecha = models.DateTimeField('Fecha y hora')

#     def save(self, *args, **kwargs):
#         geolocator = Nominatim(user_agent="GreenPure")
#         location = geolocator.reverse(
#             str(self.Latitud) + "," + str(self.Longitud))
#         pais = obtenerPais(location, self.id)
#         ciudad = obtenerCiudad(location, self.id)
#         distrito = obtenerDistrito(location, self.id)
#         super().save(*args, **kwargs)

#         try:
#             Pais.objects.filter(pais=pais).get(ciudad=ciudad)
#         except:
#             Nivel1 = Pais(pais=pais, ciudad=ciudad, calidadAVG=0)
#             Nivel1.save()
#         try:
#             Distrito.objects.get(distrito=distrito)
#         except:
#             Nivel2 = Distrito(pais=Pais.objects.get(
#                 ciudad=ciudad), distrito=distrito)
#             Nivel2.save()
#         Nivel3 = Dato(distrito=Distrito.objects.get(distrito=distrito), latitud=self.Latitud, longitud=self.Longitud, calidad=obtenerCalidad(self), fecha=str(self.fecha)[:10], hora=str(
#             self.fecha)[11:19], humedad=self.Humedad, temperatura=self.Temperatura, calor=self.Calor, concentracion=self.Concentracion, sensorHumo=self.SensorHumo, sensorMetano=self.SensorMetano)
#         Nivel3.save()

#         calidades = []
#         Enfocado = Pais.objects.filter(pais=pais).get(ciudad=ciudad)
#         distritos = Distrito.objects.filter(pais=Enfocado.id)
#         for item in distritos:
#             elementos = Dato.objects.filter(distrito=item.id)
#             for item2 in elementos:
#                 calidades.append(item2.calidad)
#         Enfocado.calidadAVG = sum(calidades)/len(calidades)
#         Enfocado.save()
