'''
@Author: Quoc-Nam DESSOULES, Claire LOFFLER
To retrieve the data from the BB and send them to the server-side
'''
from verarbeitung import Verarbeitung
from client import Client, MyClientFactory
import argparse
from threading import Timer
from twisted.internet import reactor
import time


MIN_TEMP = Verarbeitung.MIN_TEMP 
v = Verarbeitung()
factory = None

prevTemp0 = MIN_TEMP
prevTemp1 = MIN_TEMP
prevLux = -1
prevHumidity = -1
prevPressure = -1


def main():
    global v, factory
    
    #We let the user the possibility to choose the frequency of retrieval of the data and of sending the data, as well as the server whith whom he's speaking
    parser = argparse.ArgumentParser(description='Python program to retrieve external data from Beagle Bone.')#The ArgumentParser object will hold all the information necessary to parse the command line into Python data types
    parser.add_argument('-m', '--time_measurement', default=1, type=float, help="Time interval between two measurements.")
    parser.add_argument('-s', '--time_sending', default=10, type=float, help="Time interval between two sendings.")
    parser.add_argument('-a', '--address', default="192.168.7.1", help="Remote server address.")
    parser.add_argument('-p', '--port', default=1234, type=int, help="Remote server port.")
    args = parser.parse_args()
    
    #We start with an empty data dictionary that we will fill during the measurements
    v.clearData()

    Timer(args.time_measurement, getData, (args.time_measurement,)).start()#getData retrieves at regular intervals the data
    reactor.callLater(args.time_sending, sendData, args.time_sending)#sendData sends at regular intervals the data to the server

    #Creation of an instance of ClientFactory and LineReceiver to communicate with the server
    factory = MyClientFactory()
    reactor.connectTCP(args.address, args.port, factory)
    reactor.run()

#--- Functions to read the data in the corresponding BB file ---#
def read_lux():
    try:
        return read_general("/sys/bus/i2c/devices/1-0039/lux1_input")
    except IOError:
        return -1

def read_temp0():
    try:
        return read_general("/sys/bus/i2c/devices/1-0077/temp0_input")/10.0
    except IOError:
        return MIN_TEMP

def read_temp1():
    try:
        return read_general("/sys/bus/i2c/devices/1-0040/temp1_input")/1000.0
    except IOError:
        return MIN_TEMP

def read_humidity():
    try:
        return read_general("/sys/bus/i2c/devices/1-0040/humidity1_input")/1000.0
    except IOError:
        return -1

def read_pressure():
    try:
        return read_general("/sys/bus/i2c/devices/1-0077/pressure0_input")/100000.0
    except IOError:
        return -1

def read_general(fileAddr):
    try:
        f = open(fileAddr, "r")
    except IOError:
        raise
    else:
        value = int(f.readline())
        f.close()
        return value

#---To retrieve the data that have changed and puts them in v.data---#
def getData(nextTime=0):
    global v, prevTemp0, prevTemp1, prevLux, prevHumidity, prevPressure
    
    temp0 = read_temp0()
    temp1 = read_temp1()
    lux = read_lux()
    humidity = read_humidity()
    pressure = read_pressure()

    protocol = None
    if factory:
        protocol = factory.getProtocol()

    if protocol: 
        timeFn = protocol.getTime #To set a correct date and hour in the dictionary, because the BB always starts at the year 2000 at 1h:0:0
        #And we want the data to be displayed with the real value for the real date!
    else:
        timeFn = time.time

    newDict = {}
    if temp1 != prevTemp1 and temp1 > MIN_TEMP:
        newDict["TEMPERATURE"] = [(timeFn(), temp1)]
        prevTemp1 = temp1
    if lux != prevLux and lux >= 0:
        newDict["LUMINOSITY"] = [(timeFn(), lux)]
        prevLux = lux
    if humidity != prevHumidity and humidity >= 0:
        newDict["HUMIDITY"] = [(timeFn(), humidity)]
        prevHumidity = humidity
    if pressure != prevPressure and pressure >= 0:
        newDict["PRESSURE"] = [(timeFn(), pressure)]
        prevPressure = pressure

    if newDict == {}:
        print "No data to add."
        result = False
    else:
        v.addData(newDict)
        print "Data added."
        result = True

    if nextTime > 0:
        Timer(nextTime, getData, (nextTime,)).start()
    return result

#---To send the data that have been stored in v.data---#
def sendData(nextTime=0):
    global v, factory

    data = v.getData()
    
    if data == {}:
        print "No data to send."
        r = False
    else:
        result = False
        protocol = None
        if factory:
            protocol = factory.getProtocol()
        if protocol:
            result = protocol.sendData(data)
        
        if not result:
            print "Failed to send data."
            r = False
        else:   
            print "Data sent."
            v.clearData()
            print "Data deleted."
            r = True
    
    if nextTime > 0:
        reactor.callLater(nextTime, sendData, nextTime)
    return r

    

if __name__ == "__main__":
    main()



