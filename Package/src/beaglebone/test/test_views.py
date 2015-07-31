'''
@Author: Hugo Robellaz
'''
import unittest

from pyramid.testing import DummyRequest
from pyramid.testing import setUp
from pyramid.testing import tearDown
import imp

try:
    imp.find_module('webtest')
    webTestFound = True
except ImportError:
    webTestFound = False

class ProjectorViewsUnitTests(unittest.TestCase):
	def setUp(self):
		request = DummyRequest()
		self.config = setUp(request=request)

	def tearDown(self):
		tearDown()

	def _makeOne(self, request):
		from views import ProjectorViews

		inst = ProjectorViews(request)
		return inst

	def test_index_view(self):
		request = DummyRequest()
		inst = self._makeOne(request)
		result = inst.index_view()
		self.assertEqual(result['title'], 'Home')

	def test_temp_view(self):
		from globals import TEMP

		request = DummyRequest()
		inst = self._makeOne(request)
		result = inst.temp_view()
		for key,value in TEMP.items():
			self.assertEqual(result[key], value)

	def test_pressure_view(self):
		from globals import PRES

		request = DummyRequest()
		inst = self._makeOne(request)
		result = inst.pressure_view()
		for key,value in PRES.items():
			self.assertEqual(result[key], value)

	def test_luminance_view(self):
		from globals import LUMI

		request = DummyRequest()
		inst = self._makeOne(request)
		result = inst.luminance_view()
		for key,value in LUMI.items():
			self.assertEqual(result[key], value)

	def test_humidity_view(self):
		from globals import HUMI

		request = DummyRequest()
		inst = self._makeOne(request)
		result = inst.humidity_view()
		for key,value in HUMI.items():
			self.assertEqual(result[key], value)

@unittest.skipIf(not webTestFound, "Web test not found.")
class ProjectorFunctionalTests(unittest.TestCase):
	def setUp(self):
		from application import main
		app = main()
		from webtest import TestApp
		self.testapp = TestApp(app)

	def test_it(self):
		res = self.testapp.get('/', status=200)
		self.assertTrue(b'Home' in res.body)
		res = self.testapp.get('/temperature', status=200)
		self.assertTrue(b'Temperature' in res.body)
		res = self.testapp.get('/pressure', status=200)
		self.assertTrue(b'Pressure' in res.body)
		res = self.testapp.get('/humidity', status=200)
		self.assertTrue(b'Humidity' in res.body)
		res = self.testapp.get('/luminance', status=200)
		self.assertTrue(b'Luminance' in res.body)
		
		res = self.testapp.get('/mainPlot.png?sensorType=temp', status=200)
		self.assertTrue(b'image/png' in res.content_type)
		res = self.testapp.get('/smallPlot.png?sensorType=temp', status=200)
		self.assertTrue(b'image/png' in res.content_type)
