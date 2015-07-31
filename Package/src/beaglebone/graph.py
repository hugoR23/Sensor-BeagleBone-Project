'''
@Authors: Quoc-Nam Dessoulles, Claire Loffler, Hugo Robellaz
'''
from pylab import *
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime, timedelta

from globals import TEMP,HUMI,LUMI,PRES,SENSORTYPE
import time,data

class Graph(object):
	def __init__(self,data):
		self.data= data

	'''
	Create the big plot to display with the data from the sensor betwenn fromTime and toTime. It saves the file under plot/filename and return filename
	Arguments :
		sensorType: temp,humi,pres,lumi <string>
		fromTime, toTime : <datetime Objects>
	'''
	def produceMain(self,sensorType, (fromTime, toTime)):
		unit=SENSORTYPE[sensorType]['unit'] if SENSORTYPE[sensorType]['unit']!='%' else '%%'
		color=SENSORTYPE[sensorType]['plotColor']
		fileName="./plots/mainPlot_"+sensorType+"_f"+str(int(time.mktime(fromTime.timetuple())))+"_t"+str(int(time.mktime(toTime.timetuple())))+".png"

		fig=figure(num=None, figsize=(8, 6), dpi=80)

		(X,Y)=self.data.getData(sensorType, (fromTime, toTime))
		if len(X)!=0:
			scatter(X, Y,  c=color, alpha=1,  edgecolors='none', s=20)
			#The following part is only for style purposes
			ax=gca()
			xlim(fromTime,toTime)
			subplots_adjust(bottom=0.1, left=.13, right=.96, top=.90, hspace=.2)
			ax.yaxis.set_major_formatter(FormatStrFormatter('%.01f'+unit))
			ax.spines['right'].set_color('none')
			ax.spines['top'].set_color('none')
			ax.xaxis.set_ticks_position('bottom')
			ax.yaxis.set_ticks_position('left')
			ax.spines['bottom'].set_color('#707070')
			ax.spines['left'].set_color('#707070')
			ax.spines['bottom'].set_linewidth(3)
			ax.spines['left'].set_linewidth(3)
			ax.xaxis.label.set_color('#707070')
			ax.tick_params(axis='x', colors='#707070')
			ax.yaxis.label.set_color('#707070')
			ax.tick_params(axis='y', colors='#707070')
			fig.autofmt_xdate()
		else:
			text(0.5, 0.5, "No Data to Plot", ha='center', va='center', color=color, fontsize=20, clip_on=True)
			xticks([]), yticks([])
			ax=gca()
			ax.spines['right'].set_color('none')
			ax.spines['top'].set_color('none')
			ax.spines['left'].set_color('none')
			ax.spines['bottom'].set_color('none')
		
		#Save the file
		fig.savefig(fileName)
		return fileName

	'''
	Create the small plot to display at the index page with the data from the sensor betwenn fromTime and toTime. It saves the file under plot/filename and return filename
	Arguments :
		sensorType: temp,humi,pres,lumi <string>
	'''
	def produceSmall(self,sensorType):
		unit=SENSORTYPE[sensorType]['unit'] if SENSORTYPE[sensorType]['unit']!='%' else '%%'
		color=SENSORTYPE[sensorType]['plotColor']
		fileName="./plots/smallPlot_"+sensorType+".png"
		today=datetime.today()
		fromTime=(today-timedelta(days=2))
		toTime=today
		
		fig=figure(num=None, figsize=(4.5, 3), dpi=80)
		
		(X,Y)=self.data.getData(sensorType, (today-timedelta(days=2), today))
		if len(X)!=0:
			scatter(X, Y,  c=color, alpha=1,  edgecolors='none', s=30)
			
			xlim(fromTime,toTime)
			xticks([fromTime,toTime-timedelta(days=1),toTime],[fromTime.strftime('%d/%m'),"Yesterday","Today"],fontsize=12)
			
			#The following part is only for style purposes
			subplots_adjust(bottom=0.1, left=.22, right=.90, top=.90, hspace=.2)
			ax= gca()
			ax.yaxis.set_major_formatter(FormatStrFormatter('%.01f'+unit))
			ax.spines['right'].set_color('none')
			ax.spines['top'].set_color('none')
			ax.xaxis.set_ticks_position('bottom')
			ax.yaxis.set_ticks_position('left')
			ax.spines['bottom'].set_color('#707070')
			ax.spines['left'].set_color('#707070')
			ax.spines['bottom'].set_linewidth(3)
			ax.spines['left'].set_linewidth(3)
			ax.xaxis.label.set_color('#707070')
			ax.tick_params(axis='x', colors='#707070')
			ax.yaxis.label.set_color('#707070')
			ax.tick_params(axis='y', colors='#707070')
		else:
			text(0.5, 0.5, "No Data to Plot", ha='center', va='center', color=color, fontsize=20, clip_on=True)
			xticks([]), yticks([])
			ax=gca()
			ax.spines['right'].set_color('none')
			ax.spines['top'].set_color('none')
			ax.spines['left'].set_color('none')
			ax.spines['bottom'].set_color('none')

		#Save the file
		fig.savefig(fileName)
		return fileName
