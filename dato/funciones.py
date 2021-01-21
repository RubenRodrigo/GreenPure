from geopy.geocoders import Nominatim
from .clases import *

#Métodos de localización
def obtenerPais(location, id):
    try: 
        pais = location.raw['address']['country']
    except:
        pais = str(id) + "-No disponible"
    return pais

def obtenerCiudad(location, id):
    try:
        ciudad = location.raw['address']['state']
    except:
        try:
            ciudad = location.raw['address']['city']
        except:
            try:
                ciudad = location.raw['address']['country']
            except:
                ciudad = str(id) + "-No disponible"
    return ciudad

def obtenerDistrito(location, id):
    try:
        distrito = location.raw['address']['town']
    except:
        try:
            distrito = location.raw['address']['road']
        except:
            try:
                distrito = location.raw['address']['county']
            except:
                try:
                    distrito = location.raw['address']['region']
                except:
                    distrito = str(id) + "-No disponible"
    return distrito

#Métodos de resumen
def obtenerCalidad(dato):
    calidad = 1
    if dato.Temperatura <= 26 and dato.Temperatura >= 15:
        calidad += 0
    elif dato.Temperatura < 15 and dato.Temperatura >= 5:
        calidad += 10
    else:
        calidad += 20

    if dato.Humedad <= 65 and dato.Humedad >= 55:
        calidad += 0
    elif dato.Humedad < 55 and dato.Humedad >= 40:
        calidad += 10
    else:
        calidad += 20
    
    if dato.SensorMetano:
        calidad += 30
    else:
        calidad += 0
    
    if dato.SensorHumo:
        calidad += 20
    else:
        calidad += 0
    
    return calidad

def obtenerCalidadAVG(dato):
    calidades = []
    distritos = Distrito.objects.filter(pais=dato.id, many=True)
    for item in distritos:
        elementos = Dato.objects.filter(distrito=item.id, many=True)
        for item2 in elementos:
            calidades.append(item2.calidad)
    return sum(calidades)/len(calidades)