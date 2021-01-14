from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from geopy.geocoders import Nominatim
import requests
from .models import Datos
from .serializers import *
from .resumen import *
from .clases import *
#Variable de la IP de la API a consumir
API = "http://54.157.137.57/" 

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def Datos_list(request):
    """
    List all code serie, or create a new serie.
    """
    if request.method == 'GET':
        datos = Datos.objects.all()
        serializer = DatosSerializer(datos, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DatosSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
@csrf_exempt
def Dato_detail(request, pk):
    """
    Retrieve, update or delete a serie.
    """
    try:
        datos = Datos.objects.get(pk=pk)
    except Datos.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DatosSerializer(datos)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DatosSerializer(Datos, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        Datos.delete()
        return HttpResponse(status=204)

def resumen(request):
    datos = Datos.objects.all()
    #Listas para receptar los objetos resumidos
    datosResumidos = []
    elementosDato = []
    caracteristicas = []
    resumenFinal = []
    #Listas para guardar variables de orientación de datos
    distritos = []
    paisesCiudades = []
    datosDistrito = []
    repetidos = []
    #Variable contador
    cont = 0
    for dato in datos:  
        cont = cont+1
        #Datos de ubicación
        geolocator = Nominatim(user_agent="GreenPure")
        location = geolocator.reverse(str(dato.Latitud) + "," + str(dato.Longitud))
        pais = obtenerPais(location, cont)
        ciudad = obtenerCiudad(location, cont)
        distrito = obtenerDistrito(location, cont)
        datosDistrito.append(distrito)
        #Arreglo con el resumen
        #Tercer nivel
        caracteristicasElemento = CaracteristicasElemento(dato.Latitud, dato.Longitud, 12, str(dato.fecha)[11:19], dato.Humedad, dato.Temperatura, dato.Calor, dato.Concentracion, dato.SensorHumo, dato.SensorMetano)
        caracteristicas.append(caracteristicasElemento)
        #Segundo nivel
        if distrito in repetidos:
            continue
        elementoResumido = ElementoResumido(cont, distrito, caracteristicas)
        elementosDato.append(elementoResumido)
        repetidos.append(distrito)
        distritos.append(distrito)
        paisesCiudades.append(pais+ciudad)
        #Primer nivel
        if pais+ciudad in repetidos:
            continue
        datoResumido = DatoResumido(cont, str(dato.fecha)[:10], pais, ciudad, 24, elementosDato)
        datosResumidos.append(datoResumido)
        repetidos.append(pais+ciudad)
    resumenFinal = correccionOrientacionResumen(datosResumidos, paisesCiudades, distritos, datosDistrito)
    #Serialización de datos
    serializer = DatosResumenSerializer(resumenFinal, many=True)
    return JSONResponse(serializer.data)

def ciudades(request):
    ciudadesLista = []
    response = requests.get(API+"resumen", params={})
    if response.status_code == 200:
        response = response.json()
    for item in response:
        ciudad = Ciudad(item['id'], item['ciudad'])
        ciudadesLista.append(ciudad)
    serializer = CiudadesSerializer(ciudadesLista, many=True)
    return JSONResponse(serializer.data)

def ciudad(request, pk):
    response = requests.get(API+"resumen", params={})
    if response.status_code == 200:
        response = response.json()
    for item in response:
        if str(item['id']) == str(pk):
            distritos = []
            for item2 in item['ubicaciones']:
                distritoAuxiliar = DistritoAuxiliar(item2['id'],item2['distrito'],item['ciudad'],item['calidadAVG'])
                distritos.append(distritoAuxiliar)
            ciudadDistritos = CiudadDistritos(item['id'], item['ciudad'],distritos)
    serializer = CiudadesDistritosSerializer(ciudadDistritos)
    return JSONResponse(serializer.data)

def distrito(request, pk):
    response = requests.get(API+"resumen", params={})
    if response.status_code == 200:
        response = response.json()
    for item in response:
        for item2 in item['ubicaciones']:
            if str(item2['id']) == str(pk):
                distrito = Distrito(item2['id'], item2['distrito'], item['ciudad'], item['calidadAVG'], item2['datos'])
    serializer = DatosDistritoSerializer(distrito)
    return JSONResponse(serializer.data)

def humedad(request):
    elementos = Datos.objects.all()
    context = {
        "elementos": elementos
    }
    return render(request, 'index.html', context)