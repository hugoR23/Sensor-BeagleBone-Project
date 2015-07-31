'''
@Author: Quoc-Nam DESSOULES, Claire LOFFLER
To save the received data and display them
'''

try:
    from pylab import *
except ImportError:
    noGraph = True
else:
    noGraph = False

import time, pickle
from threading import Timer, Lock


 
class Verarbeitung:
    
    units = {"TEMPERATURE": "in C", "PRESSURE": "in hP", "HUMIDITY": "in %", "LUMINOSITY": "in lux"}
    MIN_TEMP = -275

    def __init__(self):
        self.data = {}
        self.lock = Lock() #To avoid that self.data is modified at the same time by differents function calls
        
#---To add the new dictionary received from the server to the dictionary self.data---# 
    def addData(self, data): #Where data is a dictionary of tuples who are in an increasing order accordingly to dates
        self.lock.acquire()

        for key, newList in data.items():
            try:
                oldList = self.data[key]
            except KeyError:
                oldList = []

            j = 0
            i = 0
            finalList = []
            while i < len(oldList) and j < len(newList): #We want the final resulting dictionary to respect the increasing date order
                d1, v1 = oldList[i]
                d2, v2 = newList[j]
                if d1 < d2:
                    finalList.append((d1,v1))
                    i += 1
                else:
                    finalList.append((d2,v2))
                    j += 1
                    
            if i < len(oldList):
                finalList.extend(oldList[i:])
            elif j < len(newList):
                finalList.extend(newList[j:])
                    
            self.data[key] = finalList

        self.lock.release()

#---To clear the self.data once that it has been saved by the server---#
    def clearData(self):
        self.lock.acquire()
        self.data = {}
        self.lock.release()

#---To get the self.data attribute---#
    def getData(self):
        self.lock.acquire()
        cpData = dict(self.data)
        self.lock.release()
        return cpData

#---To build a new dictionary, with the data boundaries corresponding to what the user asks for---#   
    def reduceList(self, dataList, startDate=0, endDate=int(time.time())):
        for i in range(len(dataList)):
            date, _ = dataList[i]
            if date >= startDate:
                break
        dataList = dataList[i:]
        
        for i in range(len(dataList)):
            date, _ = dataList[i]
            if date >= endDate:
                break
        dataList = dataList[:i]
        
        return dataList
        
#---To plot a figure: value of a given type of data (e.g, pressure) as a function of time---#        
    def createGraph(self, key, filename, startDate=0, endDate=int(time.time())):
        global noGraph
        if noGraph:
            return False

        self.lock.acquire()
        
        try:
            dataList = self.data[key]
        except KeyError:
            self.lock.release()
            return False
            
        dataList = self.reduceList(dataList, startDate, endDate)
        if dataList == []:
            self.lock.release()
            return False
        
        dateList, valueList = zip(*dataList)  # dateList and valueList are tuples. We need to convert them into a list, to give them then in argument for the plot
        dateList = list(dateList)
        minDate = dateList[0] 
        maxDate = dateList[-1] 
        valueList = list(valueList)
        
        fig = plt.figure(1)
        fig.clf()
        ax = fig.add_subplot(1,1,1)
        
        ax.plot(dateList, valueList)
        tick_params(labelsize=8)
        
        labels, _ = xticks()
        newLabels = []
        for label in labels:
            newLabels.append(time.strftime("%d/%m/%y\n%H:%M:%S", time.gmtime(int(label))))
        xticks(labels, newLabels)
        title(key + " in function of time\nbetween " + time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(minDate)) + " and "+ time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(maxDate)))
        
        savefig(filename)
        self.lock.release()
        return True

#---To make a pie chart that displays the proportion of cold, middle and hot temperatures between a time interval (that can be specified by the user)---#
    def createTempPie(self, filename, startDate=0, endDate=int(time.time())):
        global noGraph
        if noGraph:
            return False

        self.lock.acquire()
        
        try:
            dataList = self.data["TEMPERATURE"]
        except KeyError:
            self.lock.release()
            return False
            
        dataList = self.reduceList(dataList, startDate, endDate)
        if dataList == []:
            self.lock.release()
            return False
                   
        dateList, valueList = zip(*dataList)  # dateList and valueList are tuples. We need to convert them into a list, to give them then in argument for the plot
        dateList = list(dateList)
        minDate = max(dateList[0], startDate)
        maxDate = min(dateList[len(dateList)-1], endDate)
        valueList = list(valueList)
        n1=0
        n2=0
        n3=0
        for temp in valueList:
            if -20 < temp and temp < 0:
                n1 += 1
            elif 0 < temp and temp < 20:
                n2 += 1
            else:
                n3 +=1
        
        fig = plt.figure(1)
        fig.clf()
        ax = fig.add_subplot(1,1,1)
        
        ax.pie([n1,n2,n3], labels=["Negative T", "Middle T", "Hot T"])
        title("What's the TEMPERATURE?\nBetween " + time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(minDate)) + " and "+ time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(maxDate)))
        savefig(filename)
        self.lock.release()
        return True
    
#---To make an histogramm to display the evolution of a given type of data as a function tof time---#
    def createBar(self, key, filename, startDate=0, endDate=int(time.time())):
        global noGraph
        if noGraph:
            return False

        self.lock.acquire()
        
        try:
            dataList = self.data[key]
        except KeyError:
            self.lock.release()
            return False
        
        dataList = self.reduceList(dataList, startDate, endDate)
        if dataList == []:
            self.lock.release()
            return False
        
        dateList, valueList = zip(*dataList)  # dateList and valueList are tuples. We need to convert them into a list, to give them then in argument for the plot
        minDate = max(dateList[0], startDate)
        maxDate = min(dateList[len(dateList)-1], endDate)
        valueList = list(valueList)
        lowValue = min(valueList)
        highValue = max(valueList)
        
        step = (highValue - lowValue)/10.0
        xList = arange(lowValue,highValue,step)
        yList = [0]*len(xList) #xList is equal to 10 (see step)
        for i in range(len(valueList)):
            j = min(int(floor((valueList[i]-lowValue) / step)), 9)
            yList[j]+=1
            
        fig = plt.figure(1)
        fig.clf()
        ax = fig.add_subplot(1,1,1)
        ax.bar(xList,yList, width=step)
        ylabel('Number of measured '+ key)
        xlabel(Verarbeitung.units[key])
        title('Histogram of the '+ key + "\nbetween " + time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(minDate)) + " and "+ time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(maxDate)))
        savefig(filename)
        
        self.lock.release()
        return True

#---To store the content of self.data into a .csv file. Hugo will then go through this file to access the data easily and plot the graphs on the website---#
    def saveDataCSV(self):
        self.lock.acquire()
        
        try:
            f = open("dataSaved.csv", "wb")
        except IOError:
            self.lock.release()
            return False

        #Before saving the data in the file we put them all in an increasing order according to date, regardless of the type of data.
        #And we reject duplications
        Tdict = {}
        Hdict = {}
        Pdict = {}
        Ldict = {}
        timevaluesList = []
        for key, lis in self.data.items():
            for elmt in lis:
                timevalue, value = elmt
                timevalue = round(timevalue)
                if timevalue not in timevaluesList: #We do not want to have 2 lines in our .csv file with the same date
                    timevaluesList.append(timevalue)
                
                if key == "TEMPERATURE":
                    Tdict[timevalue] = value
                elif key == "PRESSURE":
                    Pdict[timevalue] = value
                elif key == "HUMIDITY":
                    Hdict[timevalue] = value
                elif key == "LUMINOSITY":
                    Ldict[timevalue] = value

        timevaluesList.sort()
        t = Verarbeitung.MIN_TEMP
        p = -1
        h = -1
        l = -1
        for timevalue in timevaluesList:
            try:
                t = Tdict[timevalue]
            except:
                pass

            try:
                p = Pdict[timevalue]
            except:
                pass

            try:
                h = Hdict[timevalue]
            except:
                pass

            try:
                l = Ldict[timevalue]
            except:
                pass
            #While respecting the increasing order of dates, we save in the file .csv the data with the good format we have fixed
            if t>Verarbeitung.MIN_TEMP and h>=0 and l>=0 and p>=0:
                timeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timevalue))
                f.write(",".join([timeStr, str(t), str(h), str(l), str(p*1000)]) + "\n")

        f.close()
        self.lock.release()
        return True

#---Before closing the program, we save all the retrieved data self.data in a file .data---#
    def saveData(self):
        try:
            f = open("dataSaved.data", "w")
        except IOError:
            return False

        self.lock.acquire()
        
        try:
            pickle.dump(self.data, f)
        except:
            f.close()
            self.lock.release()
            return False
        else:
            f.close()
            self.lock.release()
            return True

#---At every start of our program, we load the data that have been saved in dataSaved.data, so that we do not loose all the measurements from the previous times---#
    def loadData(self):
        try:
            f = open("dataSaved.data", "r")
        except IOError:
            return False

        try:
            self.addData(pickle.load(f))
        except:
            f.close()
            return False
        else:
            f.close()
            return True
            
        
