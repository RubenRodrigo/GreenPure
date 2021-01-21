from rest_framework import serializers
from .models import *


class DatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datos
        fields = ('__all__')

    def create(self, validated_data):
        return Datos.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Humedad = validated_data.get('Humedad',instance.Humedad)
        instance.Temperatura = validated_data.get('Temperatura', instance.Temperatura)
        instance.Calor = validated_data.get('Calor', instance.Calor)
        instance.Concentracion = validated_data.get('Concentracion', instance.Concentracion)
        instance.Latitud = validated_data.get('Latitud', instance.Latitud)
        instance.Longitud = validated_data.get('Longitud', instance.Longitud)
        instance.SensorHumo = validated_data.get('SensorHumo', instance.SensorHumo)
        instance.SensorMetano = validated_data.get('SensorMetano', instance.SensorMetano)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.save()
        return instance

#Serializadores para funciones de respuesta específica
class CaracteristicasSerializer(serializers.Serializer):
    latitud = serializers.DecimalField(max_digits=12, decimal_places=7, default=0)
    longitud = serializers.DecimalField(max_digits=12, decimal_places=7, default=0)
    calidad = serializers.IntegerField()
    fecha = serializers.DateField()
    hora = serializers.TimeField()
    humedad = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperatura = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    calor = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    concentracion = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    sensorHumo = serializers.BooleanField()
    sensorMetano = serializers.BooleanField()
    
class CiudadesSerializer(serializers.Serializer):
    idCiudad = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)

class DistritoAuxiliarSerializer(serializers.Serializer):
    idDistrito = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    ciudadNombre = serializers.CharField(max_length=100)
    calidad = serializers.IntegerField()

class CiudadesDistritosSerializer(serializers.Serializer):
    idCiudad = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    distritos = serializers.ListField(
        child = DistritoAuxiliarSerializer()
    )

class DatosDistritoSerializer(serializers.Serializer):
    idDistrito = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    ciudadNombre = serializers.CharField(max_length=100)
    calidadAVG = serializers.IntegerField()
    datos = serializers.ListField(
        child = CaracteristicasSerializer()
    )
    
class DistritosDatosSerializer(serializers.Serializer):
    idDistrito = serializers.IntegerField()
    ciudad = serializers.CharField(max_length=100)
    distrito = serializers.CharField(max_length=100)
    humedad = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperatura = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    fecha = serializers.DateField()
    hora = serializers.TimeField()
    calidadAVG = serializers.IntegerField()

class DistritosMapaSerializer(serializers.Serializer):
    idDistrito = serializers.IntegerField()
    ciudad = serializers.CharField(max_length=100)
    distrito = serializers.CharField(max_length=100)
    latitud = serializers.DecimalField(max_digits=12, decimal_places=7, default=0)
    longitud = serializers.DecimalField(max_digits=12, decimal_places=7, default=0)
    humedad = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperatura = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    fecha = serializers.DateField()
    hora = serializers.TimeField()
    calidadAVG = serializers.IntegerField()

#Serializadores para actuador Arduino
class DatoCalidadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    humedad = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperatura = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    calor = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    concentracion = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    latitud = serializers.DecimalField(max_digits=12, decimal_places=7, default=0)
    longitud = serializers.DecimalField(max_digits=12, decimal_places=7, default=0)
    calidad = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    sensorHumo = serializers.BooleanField()
    sensorMetano = serializers.BooleanField()
    fecha = serializers.CharField(max_length=100)
    calidad = serializers.IntegerField()

#Serializadores para resumen de datos
class DatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dato
        fields = ('latitud', 'longitud', 'calidad', 'fecha', 'hora', 'humedad', 'temperatura', 'calor', 'concentracion', 'sensorHumo', 'sensorMetano')

class DistritoSerializer(serializers.ModelSerializer):
    datos = DatoSerializer(many=True, read_only=True)
    class Meta:
        model = Distrito
        fields = ('id' ,'distrito', 'datos')

class PaisSerializer(serializers.ModelSerializer):
    ubicaciones = DistritoSerializer(many=True, read_only=True)
    class Meta:
        model = Pais
        fields = ('id', 'pais', 'ciudad', 'calidadAVG', 'ubicaciones')