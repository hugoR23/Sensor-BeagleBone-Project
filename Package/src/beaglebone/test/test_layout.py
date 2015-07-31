'''
@Author: Hugo Robellaz
'''
import unittest

from pyramid.testing import DummyRequest
from pyramid.testing import setUp
from pyramid.testing import tearDown

class LayoutUnitTests(unittest.TestCase):
	def setUp(self):
		request = DummyRequest()
		self.config = setUp(request=request)

	def tearDown(self):
		tearDown()

	def _makeOne(self):
		from layouts import Layouts

		inst = Layouts()
		return inst

	def test_global_template(self):
		from chameleon.zpt.template import Macro

		inst = self._makeOne()
		self.assertEqual(inst.global_template.__class__, Macro)

	def test_HTML_GET(self):
		inst = self._makeOne()
		inst.request = DummyRequest()
		
		inst.request.GET['test1']='ok'
		self.assertEqual(inst.HTML_GET('test1'),'ok' )
		self.assertEqual(inst.HTML_GET('test2'),0 )

	def test_getDateToPrint(self):
		from datetime import datetime, timedelta
		inst = self._makeOne()
		inst.request = DummyRequest()
		
		#Test1 : wrong inputName
		self.assertEqual(inst.getDateToPrint('coucou'), 0)
		
		#Test2 : input by default for 'toDate'
		today=datetime.today()
		self.assertEqual(inst.getDateToPrint('toDate'), today.strftime('%d/%m/%y'))
		
		#Test3 : input by default for 'fromDate'
		date=datetime.today()-timedelta(hours=24)
		self.assertEqual(inst.getDateToPrint('fromDate'), date.strftime('%d/%m/%y'))
		
		#Test4 : input by default for 'toHour'
		today=datetime.today()
		self.assertEqual(inst.getDateToPrint('toHour'), today.strftime('%H:%M'))
		
		#Test5 : input by default for 'fromHour'
		today=datetime.today()
		self.assertEqual(inst.getDateToPrint('fromHour'), today.strftime('%H:%M'))
		
		#Test6 : input already in GET variable
		inst.request.GET['fromDate']='23/11/11'
		self.assertEqual(inst.getDateToPrint('fromDate'), '23/11/11')

	def test_getDate(self):
		from datetime import datetime, timedelta
		inst = self._makeOne()
		inst.request = DummyRequest()
		
		#Test1 deltaTime&custom=0
		today=datetime.today()
		(fromTime,toTime)=inst.getDate()
		self.assertEqual(fromTime-timedelta(microseconds=fromTime.microsecond), today-timedelta(seconds=86400, microseconds=today.microsecond))
		self.assertEqual(toTime-timedelta(microseconds=toTime.microsecond), today-timedelta(microseconds=today.microsecond))
		
		#Test2 deltaTime=int<>0&custom=0
		inst.request.GET['deltaTime']=64600
		today=datetime.today()
		(fromTime,toTime)=inst.getDate()
		self.assertEqual(fromTime-timedelta(microseconds=fromTime.microsecond), today-timedelta(seconds=64600, microseconds=today.microsecond))
		self.assertEqual(toTime-timedelta(microseconds=toTime.microsecond), today-timedelta(microseconds=today.microsecond))
		
		#Test3 deltaTime=0&custom=1
		inst.request.GET['custom']=1
		inst.request.GET['fromDate']='23/11/11'
		inst.request.GET['fromHour']='10:00'
		inst.request.GET['toDate']='26/12/12'
		inst.request.GET['toHour']='11:10'
		(fromTime,toTime)=inst.getDate()
		fromTimeTest=datetime(2011, 11, 23, 10, 00)
		toTimeTest=datetime(2012, 12, 26, 11, 10)
		self.assertEqual(fromTime, fromTimeTest)
		self.assertEqual(toTime, toTimeTest)
