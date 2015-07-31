'''
@Author: Quoc-Nam DESSOULES, Claire LOFFLER
'''

import unittest
from verarbeitung import Verarbeitung
import time, random, os.path


class MainTest(unittest.TestCase):

    def setUp(self):
        self.ver = Verarbeitung()
        
    def tearDown(self):
        pass
        
    def generateRandomList(self, count=10): #Generate a random list of tuples (date, value) that we will use as values of a dictionary
        dateList = []
        valueList = []
        for x in range(count):
            dateList.append(int(time.time()) + random.randint(-100000,0))
            valueList.append(random.randint(0,40))
        dateList.sort()
        dataList = zip(dateList,valueList)
        
        return dataList
    
	#Test addData function
    def test_add(self):
		#A first randomly generated dictionary
        dataList = self.generateRandomList()
        self.ver.addData( {"TEMPERATURE":dataList} )
        
		#Check if it has correctly been added (the key "TEMPERATURE" must exists in self.ver.data and its value must correspond to dataList
        try:
            tupleList = self.ver.data["TEMPERATURE"]
        except KeyError:
            self.fail("Data not saved into dictionary.")
            
        for data in dataList:
            self.assertIn(data, tupleList)
            
		#Two other randomly generated dictionaries
        dataListT = self.generateRandomList()
        dataListP = self.generateRandomList()
        self.ver.addData( {"TEMPERATURE":dataListT, "PRESSURE":dataListP} )
        
		#Check if they have been added correctly
        try:
            tupleListT = self.ver.data["TEMPERATURE"]
            tupleListP = self.ver.data["PRESSURE"]
        except KeyError:
            self.fail("Data not saved into dictionary.")
            
        for data in dataListT:
            self.assertIn(data, tupleListT)
        for data in dataListP:
            self.assertIn(data, tupleListP)
           
	#Test that the 3 different graphs display correctly what is asked
    def test_graphs(self):
        self.ver.addData( {"TEMPERATURE":self.generateRandomList()} )
        self.ver.addData( {"PRESSURE":self.generateRandomList()} )
        
        self.assertFalse(self.ver.createGraph("ADGEGHD", "graph.png")) #The type of data the user wants to plot must be one of the key in self.ver.data
        self.ver.createGraph("PRESSURE", "graph.png")
        self.ver.createTempPie("graph2.png")
        self.ver.createBar("TEMPERATURE", "graph3.png")
        
		#We check that the graphs have been indeed saved in a .png file
        self.assertTrue(os.path.exists("graph.png"))
        self.assertTrue(os.path.exists("graph2.png"))
        self.assertTrue(os.path.exists("graph3.png"))
      
	#Test the reduceList function  
    def test_reduceList(self):
        dataList = self.generateRandomList() #randomly generaded data (tuples of (date,value))
        startDate = int(time.time())-1000 #Choose a startDate
        endDate=int(time.time())-100 #Choose a endDate
        dataList2 = self.ver.reduceList(dataList, startDate=startDate, endDate=endDate) #Try to reduce the list accordingly
        
        for data in dataList2:
            self.assertIn(data, dataList) #Check that we have not added data that were not in dataList
            date, _ = data
            self.assertGreaterEqual(date, startDate)#Check that all the values of the new reduced list are older than startDate
            self.assertLessEqual(date, endDate)#Check that all the values of the new reduced list are less than endDate old
  
	#Check that addData respects the increasing order of dates      
    def test_add_order(self):
        self.ver.addData( {"TEMPERATURE":self.generateRandomList()} )
        self.ver.addData( {"TEMPERATURE":self.generateRandomList()} )
        tupleList = self.ver.data["TEMPERATURE"]
        
        for i in range(len(tupleList)-1):
            date1, _ = tupleList[i]
            date2, _ = tupleList[i+1]
            self.assertGreaterEqual(date2, date1)
    #Test the getData function       
    def test_get(self):
        dataAdded = {"TEMPERATURE":self.generateRandomList()}
        self.ver.addData( dataAdded )
        dataStored = self.ver.getData()
        self.assertEqual(dataAdded, dataStored) #Check dataAdded and the dict returned by self.ver.getData are the same
        dataStored["PRESSURE"] = self.generateRandomList()
        self.assertNotEqual(self.ver.getData(), dataStored)#If we modify dataStored, it is different from the dataAdded
        
	#Test the clearData function
    def test_clear(self):
        self.ver.addData( {"TEMPERATURE":self.generateRandomList()} )
        self.ver.clearData()
        self.assertEqual(self.ver.getData(), {})

	#Test the saveDataCSV function by checking the existence of the fil "dataSaved.csv"
    def test_saveCSV(self):
        self.ver.addData( {"TEMPERATURE":self.generateRandomList()} )
        self.ver.addData( {"PRESSURE":self.generateRandomList()} )
        self.ver.addData( {"HUMIDITY":self.generateRandomList()} )
        self.ver.addData( {"LUMINOSITY":self.generateRandomList()} )
        self.ver.saveDataCSV()
        self.assertTrue(os.path.exists("dataSaved.csv"))

	#Test the saveData and loadData functions
    def test_saveload(self):
        self.ver.addData( {"TEMPERATURE":self.generateRandomList()} )
        self.ver.addData( {"PRESSURE":self.generateRandomList()} )
        data = self.ver.getData() #The initial data we have
        self.ver.saveData()
        self.assertTrue(os.path.exists("dataSaved.data")) #check the existence of the fil "dataSaved.csv"
        self.ver.clearData() #We erase self.ver.data and see if the loadData function works well
        self.ver.loadData()
        self.assertEqual(data, self.ver.getData()) #we check if the initial data and the loaded ones are the same
        
    
    
if __name__ == "__main__":
    unittest.main()
    
    
