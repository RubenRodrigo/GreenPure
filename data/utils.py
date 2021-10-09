from .clases import *

# Métodos de localización
# def obtenerPais(location, id):
#     try:
#         pais = location.raw['address']['country']
#     except:
#         pais = str(id) + "-No disponible"
#     return pais

# def obtenerCiudad(location, id):
#     try:
#         ciudad = location.raw['address']['state']
#     except:
#         try:
#             ciudad = location.raw['address']['city']
#         except:
#             try:
#                 ciudad = location.raw['address']['country']
#             except:
#                 ciudad = str(id) + "-No disponible"
#     return ciudad

# def obtenerDistrito(location, id):
#     try:
#         distrito = location.raw['address']['town']
#     except:
#         try:
#             distrito = location.raw['address']['road']
#         except:
#             try:
#                 distrito = location.raw['address']['county']
#             except:
#                 try:
#                     distrito = location.raw['address']['region']
#                 except:
#                     distrito = str(id) + "-No disponible"
#     return distrito

# Métodos de resumen


def getQuality(data):
    quality = 1
    if data.temperature <= 26 and data.temperature >= 15:
        quality += 0
    elif data.temperature < 15 and data.temperature >= 5:
        quality += 10
    else:
        quality += 20

    if data.humidity <= 65 and data.humidity >= 55:
        quality += 0
    elif data.humidity < 55 and data.humidity >= 40:
        quality += 10
    else:
        quality += 20

    if data.methane_sensor:
        quality += 30
    else:
        quality += 0

    if data.smoke_sensor:
        quality += 20
    else:
        quality += 0

    return quality

# def obtenerCalidadAVG(dato):
#     calidades = []
#     distritos = Distrito.objects.filter(pais=dato.id, many=True)
#     for item in distritos:
#         elementos = Dato.objects.filter(distrito=item.id, many=True)
#         for item2 in elementos:
#             calidades.append(item2.calidad)
#     return sum(calidades)/len(calidades)
