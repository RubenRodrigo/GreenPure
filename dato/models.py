from django.db import models
from geopy.geocoders import Nominatim
from .funciones import *

# Create your models here.
class Pais(models.Model):
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    calidadAVG = models.IntegerField()

    def __str__(self):
        return self.pais + "-" + self.ciudad

class Distrito(models.Model):
    pais = models.ForeignKey(Pais, related_name='ubicaciones', on_delete=models.CASCADE, default=1)
    distrito = models.CharField(max_length=100)

    def __str__(self):
        return self.distrito

class Dato(models.Model):
    distrito = models.ForeignKey(Distrito, related_name='datos', on_delete=models.CASCADE, default=1)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    calidad = models.IntegerField()
    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')
    humedad = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperatura = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    calor = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    concentracion = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sensorHumo = models.BooleanField(default=False)
    sensorMetano = models.BooleanField(default=False)

class Datos(models.Model):
    Humedad = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Temperatura = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Calor = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Concentracion = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Latitud = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    Longitud = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    SensorHumo = models.BooleanField(default=False)
    SensorMetano = models.BooleanField(default=False)
    fecha = models.DateTimeField('Fecha y hora')

    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="GreenPure")
        location = geolocator.reverse(str(self.Latitud) + "," + str(self.Longitud))
        pais = obtenerPais(location, self.id)
        ciudad = obtenerCiudad(location, self.id)
        distrito = obtenerDistrito(location, self.id)
        super().save(*args, **kwargs)

        try:
            Pais.objects.filter(pais=pais).get(ciudad=ciudad)
        except:
            Nivel1 = Pais(pais=pais, ciudad=ciudad, calidadAVG=0)
            Nivel1.save()
        try:
            Distrito.objects.get(distrito=distrito)
        except:
            Nivel2 = Distrito(pais=Pais.objects.get(ciudad=ciudad), distrito=distrito)
            Nivel2.save()
        Nivel3 = Dato(distrito=Distrito.objects.get(distrito=distrito), latitud=self.Latitud, longitud=self.Longitud, calidad=obtenerCalidad(self), fecha=str(self.fecha)[:10], hora=str(self.fecha)[11:19], humedad=self.Humedad, temperatura=self.Temperatura, calor=self.Calor, concentracion=self.Concentracion, sensorHumo=self.SensorHumo, sensorMetano=self.SensorMetano)
        Nivel3.save()

        calidades = []
        Enfocado = Pais.objects.filter(pais=pais).get(ciudad=ciudad)
        distritos = Distrito.objects.filter(pais=Enfocado.id)
        for item in distritos:
            elementos = Dato.objects.filter(distrito=item.id)
            for item2 in elementos:
                calidades.append(item2.calidad)
        Enfocado.calidadAVG = sum(calidades)/len(calidades)
        Enfocado.save()