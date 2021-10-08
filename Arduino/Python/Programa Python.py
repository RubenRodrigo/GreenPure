import httplib2
import requests
import serial
import urllib3
import json
import time

def extraer_field(texto, str_field):
    txt = texto.data.decode()
    txt1 = json.loads(txt)
    txt2 = txt1[len(txt1)-1].get(str_field)
    return txt2

def extraer_calidad(texto, str_field):
    txt = texto.data.decode()
    txt1 = json.loads(txt).get(str_field)
    return txt1

http = urllib3.PoolManager()
ser = serial.Serial('COM2', 9600)
ser.readline()
conn = httplib2.Http()
while True:
    datoString = ser.readline()
    datos = str(datoString).split(",")
    
    humedad = (datos[0][2:-3])
    temperatura =(datos[1][:-3])
    calor = (datos[2])
    if (datos[3]=='0'):
        mq4 = "false"
    else:
        mq4 = "true"
    if (datos[4]=='0'):
        mq2 = "false"
    else:
        mq2 = "true"
    latitud = (datos[5])
    longitud = (datos[6])
    tiempo = (datos[7])
    concentracion = (datos[8][:-5])
     
    print ("H: "+humedad+" T: "+temperatura+" C: "+calor+" MQ4: "+mq4+" MQ2: "+mq2+" LAT: "+latitud+" LNG: "+longitud+" Time: "+tiempo+" C: "+concentracion+"\n")
    
    parametros = {'Humedad': humedad,'Temperatura': temperatura,'Calor': calor,'Concentracion': concentracion,'SensorMetano': mq4,'SensorHumo': mq2,'Latitud': latitud,'Longitud': longitud,'fecha': tiempo}
    resp = requests.post('http://127.0.0.1:8000/dato/', json=parametros)
    
    r = http.request('GET', 'http://127.0.0.1:8000/inscribir/')
    b = extraer_calidad(r,'calidad')
    if int(b) <= 45:
        ser.write(("1").encode())
    else:
        ser.write(("2").encode())
    print ("Calidad: ", b)
    time.sleep(5)
    ser.write(("0").encode())
