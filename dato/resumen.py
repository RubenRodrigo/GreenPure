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
                distrito = str(id) + "-No disponible"
    return distrito

#Métodos de resumen
def crearArregloResumen(latitud, longitud, calidadAVG, hora, humedad, temperatura, calor, concentracion, sensorHumo, sensorMetano, distrito, idDato, fecha, pais, ciudad, calidad):    
    #Listas para receptar los objetos resumidos
    elementosDato = []
    caracteristicas = []
    #Tercer nivel
    caracteristicasElemento = CaracteristicasElemento(latitud, longitud, calidadAVG, hora, humedad, temperatura, calor, concentracion, sensorHumo, sensorMetano)
    caracteristicas.append(caracteristicasElemento)
    #Segundo nivel
    elementoResumido = ElementoResumido(distrito, caracteristicas)
    elementosDato.append(elementoResumido)
    #Primer nivel
    datoResumido = DatoResumido(idDato, fecha, pais, ciudad, calidad, elementosDato)
    return datoResumido

def correccionOrientacionResumen(datosResumidos, paisesCiudades, distritos, datosDistrito):
    resumenNivel3 = []
    resumenNivel2 = []
    resumenFinal = []
    for item in datosResumidos:
        contador = 0
        for item2 in item.ubicaciones:
            if item2.distrito == distritos[contador] and str(item.pais+item.ciudad) == paisesCiudades[contador]:
                contador2 = 0
                for item3 in item2.datos:
                    if item2.distrito == datosDistrito[contador2]:
                        resumenNivel3.append(item3)    
                    contador2 = contador2 +1
                resumenNivel2.append(ElementoResumido(item2.id, item2.distrito, resumenNivel3))
                resumenNivel3 = []
            contador = contador + 1
        resumenFinal.append(DatoResumido(item.id, item.fecha, item.pais, item.ciudad, item.calidadAVG, resumenNivel2))
        resumenNivel2 = []
    return resumenFinal