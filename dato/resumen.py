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
    calidad = 0
    if dato.Temperatura <= 26 and dato.Temperatura >= 15:
        calidad += 10
    elif dato.Temperatura < 15 and dato.Temperatura >= 5:
        calidad += 0
    else:
        calidad -= 20

    if dato.Humedad <= 65 and dato.Humedad >= 55:
        calidad += 10
    elif dato.Humedad < 55 and dato.Humedad >= 40:
        calidad += 0
    else:
        calidad -= 20
    
    if dato.SensorMetano:
        calidad += 30
    else:
        calidad -= 30
    
    if dato.SensorHumo:
        calidad += 20
    else:
        calidad -= 20
    
    return calidad

def correccionOrientacionResumen(datosResumidos, paisesCiudades, distritos, datosDistrito):
    resumenNivel3 = []
    resumenNivel2 = []
    resumenFinal = []
    calidades = []
    for item in datosResumidos:
        contador = 0
        for item2 in item.ubicaciones:
            if item2.distrito == distritos[contador] and str(item.pais+item.ciudad) == paisesCiudades[contador]:
                contador2 = 0
                for item3 in item2.datos:
                    if item2.distrito == datosDistrito[contador2]:
                        resumenNivel3.append(item3)  
                        calidades.append(item3.calidad)  
                    contador2 = contador2 +1
                resumenNivel2.append(ElementoResumido(item2.id, item2.distrito, resumenNivel3))
                resumenNivel3 = []
            contador = contador + 1
        resumenFinal.append(DatoResumido(item.id, item.pais, item.ciudad, sum(calidades)/len(calidades), resumenNivel2))
        resumenNivel2 = []
        calidades = []
    return resumenFinal