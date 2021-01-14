#Clases de objetos resumen
class DatoResumido:
    def __init__(self, id, fecha, pais, ciudad, calidadAVG, ubicaciones):
        self.id = id
        self.fecha = fecha
        self.pais = pais
        self.ciudad = ciudad
        self.calidadAVG = calidadAVG
        self.ubicaciones = ubicaciones
class ElementoResumido:
    def __init__(self, distrito, datos):
        self.distrito = distrito
        self.datos = datos
class CaracteristicasElemento:
    def __init__(self, latitud, longitud, calidad, hora, humedad, temperatura, calor, concentracion, sensorHumo, sensorMetano):
        self.latitud = latitud
        self.longitud = longitud
        self.calidad = calidad
        self.hora = hora
        self.humedad = humedad
        self.temperatura = temperatura
        self.calor = calor
        self.concentracion = concentracion
        self.sensorHumo = sensorHumo
        self.sensorMetano = sensorMetano

#Clase para funcionalidad con Arduino
class DatoCalidad:
    def __init__(id, humedad, temperatura, calor, concentracion, latitud, longitud, sensorHumo, sensorMetano, fecha, calidad):
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