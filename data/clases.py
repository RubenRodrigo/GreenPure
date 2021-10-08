#Clases de objetos resumen
class DatoResumido:
    def __init__(self, id, pais, ciudad, calidadAVG, ubicaciones):
        self.id = id
        self.pais = pais
        self.ciudad = ciudad
        self.calidadAVG = calidadAVG
        self.ubicaciones = ubicaciones
class ElementoResumido:
    def __init__(self, id, distrito, datos):
        self.id = id
        self.distrito = distrito
        self.datos = datos
class CaracteristicasElemento:
    def __init__(self, latitud, longitud, calidad, fecha, hora, humedad, temperatura, calor, concentracion, sensorHumo, sensorMetano):
        self.latitud = latitud
        self.longitud = longitud
        self.calidad = calidad
        self.fecha = fecha
        self.hora = hora
        self.humedad = humedad
        self.temperatura = temperatura
        self.calor = calor
        self.concentracion = concentracion
        self.sensorHumo = sensorHumo
        self.sensorMetano = sensorMetano
    
#Clases para funcionalidad de datos enfocados
class Ciudad:
    def __init__(self, idCiudad, nombre):
        self.idCiudad = idCiudad
        self.nombre = nombre
class CiudadDistritos:
    def __init__(self, idCiudad, nombre, distritos):
        self.idCiudad = idCiudad
        self.nombre = nombre
        self.distritos = distritos
class DistritoAuxiliar:
    def __init__(self, idDistrito, nombre, ciudadNombre, calidad):
        self.idDistrito = idDistrito
        self.nombre = nombre
        self.ciudadNombre = ciudadNombre
        self.calidad = calidad
class DistritoEnfocado:
    def __init__(self, idDistrito, ciudad, distrito, humedad, temperatura, concentracion, hora, fecha, calidadAVG):
        self.idDistrito = idDistrito
        self.ciudad = ciudad
        self.distrito = distrito
        self.humedad = humedad
        self.temperatura = temperatura
        self.concentracion = concentracion
        self.hora = hora
        self.fecha = fecha
        self.calidadAVG = calidadAVG
class DistritoMapa:
    def __init__(self, idDistrito, ciudad, distrito, latitud, longitud, humedad, temperatura, concentracion, hora, fecha, calidadAVG):
        self.idDistrito = idDistrito
        self.ciudad = ciudad
        self.distrito = distrito
        self.latitud = latitud
        self.longitud = longitud
        self.humedad = humedad
        self.temperatura = temperatura
        self.concentracion = concentracion
        self.hora = hora
        self.fecha = fecha
        self.calidadAVG = calidadAVG
class Distrito:
    def __init__(self, idDistrito, nombre, ciudadNombre, calidadAVG, datos):
        self.idDistrito = idDistrito
        self.nombre = nombre
        self.ciudadNombre = ciudadNombre
        self.calidadAVG = calidadAVG
        self.datos = datos

#Clase para funcionalidad con Arduino
class DatoCalidad:
    def __init__(self, id, humedad, temperatura, calor, concentracion, latitud, longitud, sensorHumo, sensorMetano, fecha, calidad):
        self.id = id
        self.humedad = humedad
        self.temperatura = temperatura
        self.calor = calor
        self.concentracion = concentracion
        self.latitud = latitud
        self.longitud = longitud
        self.sensorHumo = sensorHumo
        self.sensorMetano = sensorMetano
        self.fecha = fecha
        self.calidad = calidad
