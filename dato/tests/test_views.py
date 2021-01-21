from django.test import TestCase
from dato.models import *
from rest_framework.test import APIClient
from rest_framework import status
import json

# Create your tests here.
class APITests(TestCase):
	@classmethod
	def setUpTestData(cls):
		Datos.objects.create(
			Humedad= 50.00,
			Temperatura= 80.00,
			Calor= 112.12,
			Concentracion= 124.42,
			Latitud= -16.3745730,
			Longitud= -71.5121000,
			SensorHumo= True,
			SensorMetano= False,
			fecha= '2021-01-08T19:33:10Z'
			)
		pass

	def test_get_dato(self):
		client = APIClient()

		response = client.get('/dato/')

		result = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		for dato in result:
			self.assertIn('Humedad', dato)
			self.assertIn('Temperatura', dato)
			self.assertIn('Calor', dato)
			self.assertIn('Concentracion', dato)
			self.assertIn('Latitud', dato)
			self.assertIn('Longitud', dato)
			self.assertIn('SensorHumo', dato)
			self.assertIn('SensorMetano', dato)
			self.assertIn('fecha', dato)
			break

	def test_get_resumen(self):
		client = APIClient()

		response = client.get('/resumen/')

		result = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		for dato in result:
			self.assertIn('pais', dato)
			self.assertIn('ciudad', dato)
			self.assertIn('calidadAVG', dato)
			self.assertIn('ubicaciones', dato)
			for ubicacion in dato['ubicaciones']:
				self.assertIn('id', ubicacion)
				self.assertIn('distrito', ubicacion)
				self.assertIn('datos', ubicacion)
				for elemento in ubicacion['datos']:
					self.assertIn('latitud', elemento)
					self.assertIn('longitud', elemento)
					self.assertIn('calidad', elemento)
					self.assertIn('fecha', elemento)
					self.assertIn('hora', elemento)
					self.assertIn('sensorHumo', elemento)
					self.assertIn('sensorMetano', elemento)
					self.assertIn('humedad', elemento)
					self.assertIn('temperatura', elemento)
					self.assertIn('calor', elemento)
					self.assertIn('concentracion', elemento)
			break

	def test_get_ciudad(self):
		client = APIClient()

		response = client.get('/ciudad/1/')

		result = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.assertIn('idCiudad', result)
		self.assertIn('nombre', result)
		self.assertIn('distritos', result)
		for distrito in result['distritos']:
			self.assertIn('idDistrito', distrito)
			self.assertIn('nombre', distrito)
			self.assertIn('ciudadNombre', distrito)
			self.assertIn('calidad', distrito)
			break

	def test_get_ciudades(self):
		client = APIClient()

		response = client.get('/ciudades/')

		result = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		for dato in result:
			self.assertIn('idCiudad', dato)
			self.assertIn('nombre', dato)
			break

	def test_get_distritoDatos(self):
		client = APIClient()

		response = client.get('/distritoDatos/1/')

		result = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.assertIn('idDistrito', result)
		self.assertIn('nombre', result)
		self.assertIn('ciudadNombre', result)
		self.assertIn('calidadAVG', result)
		self.assertIn('datos', result)
		for elemento in result['datos']:
			self.assertIn('latitud', elemento)
			self.assertIn('longitud', elemento)
			self.assertIn('calidad', elemento)
			self.assertIn('fecha', elemento)
			self.assertIn('hora', elemento)
			self.assertIn('humedad', elemento)
			self.assertIn('temperatura', elemento)
			self.assertIn('calor', elemento)
			self.assertIn('concentracion', elemento)
			self.assertIn('sensorHumo', elemento)
			self.assertIn('sensorMetano', elemento)
			break

	def test_get_distritos(self):
		client = APIClient()

		response = client.get('/distritos/')

		result = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.assertIn('idDistrito', result)
		self.assertIn('nombre', result)
		self.assertIn('ciudadNombre', result)
		self.assertIn('calidadAVG', result)
		self.assertIn('datos', result)
		for elemento in result['datos']:
			self.assertIn('latitud', elemento)
			self.assertIn('longitud', elemento)
			self.assertIn('calidad', elemento)
			self.assertIn('fecha', elemento)
			self.assertIn('hora', elemento)
			self.assertIn('humedad', elemento)
			self.assertIn('temperatura', elemento)
			self.assertIn('calor', elemento)
			self.assertIn('concentracion', elemento)
			self.assertIn('sensorHumo', elemento)
			self.assertIn('sensorMetano', elemento)
			break

	def test_get_distritos(self):
		client = APIClient()

		response = client.get('/distritos/')

		result = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		for dato in result:
			self.assertIn('idDistrito', dato)
			self.assertIn('ciudad', dato)
			self.assertIn('distrito', dato)
			self.assertIn('humedad', dato)
			self.assertIn('temperatura', dato)
			self.assertIn('fecha', dato)
			self.assertIn('hora', dato)
			self.assertIn('calidadAVG', dato)
			break

	def test_get_distritosMapa(self):
		client = APIClient()

		response = client.get('/mapa/')

		result = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		for dato in result:
			self.assertIn('idDistrito', dato)
			self.assertIn('ciudad', dato)
			self.assertIn('distrito', dato)
			self.assertIn('latitud', dato)
			self.assertIn('longitud', dato)
			self.assertIn('humedad', dato)
			self.assertIn('temperatura', dato)
			self.assertIn('fecha', dato)
			self.assertIn('hora', dato)
			self.assertIn('calidadAVG', dato)
			break