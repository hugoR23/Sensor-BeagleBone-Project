'''
@Author: Hugo Robellaz
'''
import unittest
from datetime import datetime, timedelta

class DataUnitTests(unittest.TestCase):

	def setUp(self):
		from data import Data
		import globals
		import os
		path=os.path.dirname(os.path.realpath(__file__))+'/'
		self.DBFileName=path+'TestDB.csv'
		self.nbOfSample=self.createTestFileData()
		self.inst= Data(self.DBFileName)
	
	def storeCSV(self, data, file):
		import csv
		with open(file,'ab+') as f:
			fieldnames=('date', 'temp', 'humi', 'lumi','pres')
			w = csv.DictWriter(f,fieldnames)
			w.writerow(data)

	def createTestFileData(self):
		open(self.DBFileName, 'w').close()
		today=datetime(2011, 11, 23, 10, 00, 01)
		date=today-timedelta(days=7)
		nbOfSample=0
		while(date<=today):
			X=date.day*date.hour+date.minute/15
			dict={'date':date,
				  'temp':float(20+X/(7*18)),
				  'humi':float(50+X/(7*18)),
				  'lumi':float(100+X/(7*18)),
				  'pres':float(1000+X/(7*18))}
			date=date+timedelta(minutes=30)
			self.storeCSV(dict,self.DBFileName)
			nbOfSample+=1
		return nbOfSample

	def test_cacheData(self):
		self.setUp()
		res=self.inst.DATALIST
		for dict in res:
			date=dict['date']
			X=date.day*date.hour+date.minute/15
			testDict={'date':date,
				  'temp':float(20+X/(7*18)),
				  'humi':float(50+X/(7*18)),
				  'lumi':float(100+X/(7*18)),
				  'pres':float(1000+X/(7*18))}
			self.assertEqual(dict,testDict)
		self.assertEqual(len(res),self.nbOfSample)

	def test_getData(self):
		self.setUp()
		fromTime=datetime(2011, 11, 20, 10, 01, 01)
		toTime=datetime(2011, 11, 22, 11, 31, 01)
		nbOfData=int((toTime-fromTime).total_seconds()/3600.0*2)
		(dates,values)=self.inst.getData('temp',(fromTime,toTime))
		self.assertEqual(dates[0],datetime(2011, 11, 20, 10, 30, 01))
		self.assertEqual(dates[len(dates)-1],datetime(2011, 11, 22, 11, 30, 01))
		self.assertEqual(len(values),nbOfData)

	def test_getLatestData(self):
		self.setUp()
		res=self.inst.getLatestData()
		date=datetime(2011, 11, 23, 10, 00, 01)
		X=date.day*date.hour+date.minute/15
		testDict={"updatedTime": date.strftime('on %d %b, %Y at %H:%M'),
				  'lastTemp':20+X/(7*18),
				  'lastHumi':50+X/(7*18),
				  'lastLumi':100+X/(7*18),
				  'lastPres':1000+X/(7*18)}
		for key,value in res.items():
			self.assertEqual(value,testDict[key])

	def test_getMainData(self):
		self.setUp()
		fromTime=datetime(2011, 11, 20, 10, 01, 01)
		#Test1: nbOfData=0
		toTime=datetime(2011, 11, 20, 10, 15, 01)
		nbOfData=int((toTime-fromTime).total_seconds()/3600.0*2)
		res=self.inst.getMainData('temp',(fromTime,toTime))
		self.assertEqual(res["nbOfSample"],nbOfData)
		self.assertEqual(res["avgDeltaTime"],"NC")
		self.assertEqual(res["highest"],"NC")
		
		#Test2: nbOfData=1
		toTime=datetime(2011, 11, 20, 10, 31, 01)
		nbOfData=int((toTime-fromTime).total_seconds()/3600.0*2)
		res=self.inst.getMainData('temp',(fromTime,toTime))
		self.assertEqual(res["nbOfSample"],nbOfData)
		self.assertEqual(res["avgDeltaTime"],"NC")

		#Test3: nbOfData>1
		toTime=datetime(2011, 11, 22, 11, 31, 01)
		nbOfData=int((toTime-fromTime).total_seconds()/3600.0*2)
		res=self.inst.getMainData('temp',(fromTime,toTime))
		self.assertEqual(res["nbOfSample"],nbOfData)
		self.assertEqual(res["avgDeltaTime"],"30m 0s")
