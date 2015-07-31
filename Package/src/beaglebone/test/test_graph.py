'''
@Author: Hugo Robellaz
'''
import unittest

class GraphUnitTests(unittest.TestCase):

	def setUp(self):
		from graph import Graph
		from data import Data
		data= Data()
		self.inst = Graph(data)

	def test_produceMain(self):
		from datetime import datetime, timedelta
		import os
		path=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
		self.setUp()
		fromTime=datetime.today()-timedelta(days=100)
		toTime=datetime.today()
		fileName=self.inst.produceMain('temp', (fromTime,toTime))
		self.assertTrue(fileName.find('mainPlot')!=-1)
		self.assertTrue(os.path.exists(path+fileName[1:len(fileName)]))

	def test_produceSmall(self):
		from datetime import datetime, timedelta
		import os
		path=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
		self.setUp()
		fromTime=datetime.today()-timedelta(days=100)
		toTime=datetime.today()
		fileName=self.inst.produceSmall('temp')
		self.assertTrue(fileName.find('smallPlot')!=-1)
		self.assertTrue(os.path.exists(path+fileName[1:len(fileName)]))


