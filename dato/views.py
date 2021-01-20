from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from geopy.geocoders import Nominatim
import requests
from .models import *
from .models import Distrito as DistritoModel
from .serializers import *
from .funciones import *
from .clases import *

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
    if request.method == 'GET':
        resumen = Pais.objects.all()
        serializer = PaisSerializer(resumen, many=True)
        return JSONResponse(serializer.data)

def ciudad(request, pk):
    resumen = Pais.objects.get(pk=pk)
    ubicaciones = DistritoModel.objects.filter(pais=resumen.id)
    distritos = []
    for item2 in ubicaciones:
        distritoAuxiliar = DistritoAuxiliar(item2.id,item2.distrito,resumen.ciudad,resumen.calidadAVG)
        distritos.append(distritoAuxiliar)
    ciudadDistritos = CiudadDistritos(resumen.id, resumen.ciudad,distritos)
    serializer = CiudadesDistritosSerializer(ciudadDistritos)
    return JSONResponse(serializer.data)

def ciudades(request):
    resumen = Pais.objects.all()
    ciudadesLista = []
    for item in resumen:
        ciudad = Ciudad(item.id, item.ciudad)
        ciudadesLista.append(ciudad)
    serializer = CiudadesSerializer(ciudadesLista, many=True)
    return JSONResponse(serializer.data)

def distritoDatos(request, pk):
    resumen = Pais.objects.all()
    for item in resumen:
        ubicaciones = DistritoModel.objects.filter(pais=item.id)
        for item2 in ubicaciones:
            datos = Dato.objects.filter(distrito=item2.id)
            if str(item2.id) == str(pk):
                distrito = Distrito(item2.id, item2.distrito, item.ciudad, item.calidadAVG, datos)
    serializer = DatosDistritoSerializer(distrito)
    return JSONResponse(serializer.data)

def distritos(request):
    resumen = Pais.objects.all()
    if request.GET.get('id_distrito1', -1) == -1:
        distritosLista = []
        cont = 0
        for item in resumen:
            ubicaciones = DistritoModel.objects.filter(pais=item.id)
            for item2 in ubicaciones:
                if cont < 4:
                    #Colocando el último dato
                    item3 = Dato.objects.filter(distrito=item2.id).last()
                    distritoEnfocado = DistritoEnfocado(item2.id, item.ciudad, item2.distrito, item3.humedad, item3.temperatura, item3.concentracion, item3.hora, item3.fecha, item.calidadAVG)
                    distritosLista.append(distritoEnfocado)
                else:
                    break
                cont += 1
        serializer = DistritosDatosSerializer(distritosLista, many=True)
        return JSONResponse(serializer.data)
    else:
        distritosLista = []
        idsDistritos = []
        cont = 1
        while request.GET.get('id_distrito'+str(cont)) != None:
            id_distrito = request.GET.get('id_distrito'+str(cont))
            idsDistritos.append(id_distrito)
            cont += 1
        for item in resumen:
            ubicaciones = DistritoModel.objects.filter(pais=item.id)
            for item2 in ubicaciones:
                if str(item2.id) in idsDistritos:
                    item3 = Dato.objects.filter(distrito=item2.id).last()
                    distritoEnfocado = DistritoEnfocado(item2.id, item.ciudad, item2.distrito, item3.humedad, item3.temperatura, item3.concentracion, item3.hora, item3.fecha, item.calidadAVG)
                    distritosLista.append(distritoEnfocado)
        serializer = DistritosDatosSerializer(distritosLista, many=True)
        return JSONResponse(serializer.data)

def distritosMapa(request):
    resumen = Pais.objects.all()
    distritosLista = []
    for item in resumen:
        ubicaciones = DistritoModel.objects.filter(pais=item.id)
        for item2 in ubicaciones:
            item3 = Dato.objects.filter(distrito=item2.id).last()
            distritoMapa = DistritoMapa(item2.id, item.ciudad, item2.distrito, item3.latitud, item3.longitud,item3.humedad, item3.temperatura, item3.concentracion, item3.hora, item3.fecha, item.calidadAVG)
            distritosLista.append(distritoMapa)
    serializer = DistritosMapaSerializer(distritosLista, many=True)
    return JSONResponse(serializer.data)

def inscribir(request):
    dato = Datos.objects.last()
    datoCalidad = DatoCalidad(dato.id, dato.Humedad, dato.Temperatura, dato.Calor, dato.Concentracion, dato.Latitud, dato.Longitud, dato.SensorHumo, dato.SensorMetano, dato.fecha, obtenerCalidad(dato))
    serializer = DatoCalidadSerializer(datoCalidad)
    return JSONResponse(serializer.data)

def respuesta(request):
    elementos = Datos.objects.all()
    context = {
        "elementos": elementos
    }
    return render(request, 'index.html', context)