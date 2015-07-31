'''
@Authors: Quoc-Nam Dessoulles, Claire Loffler, Hugo Robellaz
'''
import csv,time
from datetime import datetime, timedelta
import globals
from globals import TEMP,HUMI,LUMI,PRES,SENSORTYPE

class Data(object):
	DATALIST=[]
	def __init__(self,databaseFilename=globals.DATABASE_FILENAME):
		self.DATALIST=self.cacheData(databaseFilename)

	def cacheData(self,dbFilename):
		dataList=[]
		with open(dbFilename,'r') as f:
			fieldnames=['date', 'temp', 'humi', 'lumi','pres']
			data = csv.DictReader(f,fieldnames)
			for line in data:
				line['date']=datetime.strptime(line['date'],"%Y-%m-%d  %H:%M:%S")
				line['temp']=float(line['temp'])
				line['pres']=float(line['pres'])
				line['lumi']=float(line['lumi'])
				line['humi']=float(line['humi'])
				dataList.append(line)
		return dataList
	cacheData=classmethod(cacheData)
	'''
	Return the latest data on all sensors and the time they were updated
	'''
	def getLatestData(self):
		if len(self.DATALIST)==0:
			return {"updatedTime": "now",
					"lastTemp": "NC",
					"lastPres": "NC",
					"lastLumi": "NC",
					"lastHumi": "NC"}
		else:
			last=self.DATALIST[len(self.DATALIST)-1]
			return {"updatedTime": last['date'].strftime('on %d %b, %Y at %H:%M'),
					"lastTemp":last['temp'],
					"lastPres":last['pres'],
					"lastLumi":last['lumi'],
					"lastHumi":last['humi']}

	'''
	getMainData returns the important data from the sensor between fromTime and toTime
	Arguments :
		sensorType: temp,humi,pres,lumi <string>
		fromTime, toTime : <datetime Objects>
	'''
	def getMainData(self,sensorType, (fromTime, toTime)):
		(dates,values)=self.getData(sensorType, (fromTime, toTime))
		nb=len(values)
		if nb==0:
			return {"average": "NC",
					"highest": "NC",
					"lowest": "NC",
					"nbOfSample": nb,
					"avgDeltaTime": "NC",
					"updatedTime": "now"}
		else:
			avgDeltaTime=0
			previousDate=dates[0]
			for date in dates[1:nb]:
				avgDeltaTime+=(date-previousDate).total_seconds()
				previousDate=date
			avgDeltaTime=str(int((avgDeltaTime/(nb-1))//60))+'m '+str(int((avgDeltaTime/(nb-1))%60))+'s' if(nb>1) else "NC"
			return {"average": round(sum(values)/nb,2),
					"highest": max(values),
					"lowest": min(values),
					"nbOfSample": nb,
					"avgDeltaTime": avgDeltaTime,
					"updatedTime": dates[nb-1].strftime('on %d %b, %Y at %H:%M')}

	'''
	getData returns the data from the sensor between fromTime and toTime
	Arguments :
		sensorType: temp,humi,pres,lumi <string>
		fromTime, toTime : <datetime Objects>
	'''
	def getData(self,sensorType, (fromTime, toTime)):
		dates=[]
		values=[]
		for data in self.DATALIST:
			date=data['date']
			if date<=toTime and date>=fromTime:
				dates.append(date)
				values.append(float(data[sensorType]))
			if date>=toTime:
				break
		return (dates,values)

