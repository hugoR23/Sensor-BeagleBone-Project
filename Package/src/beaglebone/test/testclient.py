'''
@Author: Louis-Adrien DUFRENE, Hang YUAN
'''

import unittest
from client import Client, MyClientFactory
from twisted.internet import reactor


class MainTest(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
                
    @unittest.skip("No reactor running...")
    def test_sendData1(self):
        tuple1 = (150000000, -36)
        tuple2 = (150000156, 57)
        tuple3 = (1155684658465, 159)
        dict = {}
        client = Client()
        dict["TEMPERATURE"] = [tuple1, tuple2, tuple3]
        print "Data ready"
        self.assertTrue(client.sendData(dict))
        print "Data sent"
        
    @unittest.skip("No reactor running...")
    def test_sendData2(self):
        tuple1 = (150000000, -36)
        tuple2 = (150000156, 57)
        tuple3 = (1155684658465, 159)
        tuple4 = (15183513,123456789)
        tuple5 = (123456789, -1965)
        tuple6 = (15698745312, 15.45)
        dict = {}
        client = Client()
        dict["TEMPERATURE"] = [tuple1, tuple2, tuple3]
        dict["HUMIDITY"] = [tuple4]
        dict["PLOP"] = [tuple5, tuple6]
        print "Data ready"
        self.assertTrue(client.sendData(dict))
        print "Data sent"
            
if __name__ == "__main__":
    unittest.main()
	
    
    
