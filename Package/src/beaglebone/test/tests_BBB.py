'''
@Author: Quoc-Nam DESSOULES, Claire LOFFLER
'''

import unittest
import BBB
import os


class MainTest(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
#---Our tests: we skip them if we are not in the BB---#      
    @unittest.skipIf(not os.path.exists("/var/lib/opkg/lists/beaglebone"), "This test should be runned on the Beagle Bone only.")
    def test_lux(self):
        self.assertGreaterEqual(BBB.read_lux(), 0)
        
    @unittest.skipIf(not os.path.exists("/var/lib/opkg/lists/beaglebone"), "This test should be runned on the Beagle Bone only.")
    def test_temp0(self):
        self.assertGreater(BBB.read_temp0(), BBB.MIN_TEMP)
        
    @unittest.skipIf(not os.path.exists("/var/lib/opkg/lists/beaglebone"), "This test should be runned on the Beagle Bone only.")
    def test_temp1(self):
        self.assertGreater(BBB.read_temp1(), BBB.MIN_TEMP)
        
    @unittest.skipIf(not os.path.exists("/var/lib/opkg/lists/beaglebone"), "This test should be runned on the Beagle Bone only.")
    def test_humidity(self):
        self.assertGreaterEqual(BBB.read_humidity(), 0)
        
    @unittest.skipIf(not os.path.exists("/var/lib/opkg/lists/beaglebone"), "This test should be runned on the Beagle Bone only.")
    def test_pressure(self):
        self.assertGreaterEqual(BBB.read_pressure(), 0)
        
    @unittest.skipIf(not os.path.exists("/var/lib/opkg/lists/beaglebone"), "This test should be runned on the Beagle Bone only.")
    def test_reading(self):
        self.assertRaises(IOError, BBB.read_general, "kjdbcsjk/ncezkfcn/suzidb.xd")
    
    @unittest.skipIf(not os.path.exists("/var/lib/opkg/lists/beaglebone"), "This test should be runned on the Beagle Bone only.")
    def test_getData(self):
        self.assertTrue(BBB.getData())
        
    @unittest.skip("No reactor running...")
    def test_sendData(self):
        self.assertTrue(BBB.sendData())
        self.assertFalse(BBB.sendData())

    
if __name__ == "__main__":
    unittest.main()
    
    
