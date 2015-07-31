'''
@Author: Louis-Adrien DUFRENE, Hang YUAN
'''
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.error import ConnectionDone
import time

#The class Client, which inherits from the protocol LineReceiver.
#There will be one instance of this class for each client connected to the server.
class Client(LineReceiver):
        
    def __init__(self):
        self.timeBegin = time.time()
        self.timeRef = time.time()

    #This method is called when the client is connected to the server.    
    def connectionMade(self):
        print "Connection made."
    
    #This method is called when the connexion with the server is lost.
    def connectionLost(self, reason=ConnectionDone):
        print "Connection lost: " + reason.getErrorMessage()
        if reactor.running:
            reactor.stop()
    
    #This method sends the dictionnary 'dict' as a string to the server.
    def sendData(self, mydict):        
        mylist = []
        
        string = ""
        
        for key, newlist in mydict.iteritems():
        
            for mytuple in mydict[key]:
                string += "|" + str(mytuple)#Here we separate the key and each tuples from the same key with a "|" 
                
            mylist.append(key + string + "/")#Here we separate each group of key and tuples with a "/"
            string = ""
        
        try:
            self.sendLine("".join(mylist))#Sends the dictionnary as a string
            return True
            
        except:
            return False

    def lineReceived(self, line):
        self.timeBegin = float(line)
        self.timeRef = time.time()

    def getTime(self):
        t = time.time() - self.timeRef + self.timeBegin
        return t
    

#This class is the factory used to create the client instance. It inherits from ClientFactory.
#Each a new client tries to connect to the server, the ClientFactory will called the method buildProtocol.    
class MyClientFactory(ClientFactory):
    
    def __init__(self):
        self.protocol = None

    #This method is called each time the factory creates an instance of Client. It also creates the instance.
    def buildProtocol(self, addr):
        print 'Connected.'
        self.protocol = Client()
        return self.protocol
    
    #This method is called when the connection with the server is lost.
    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        if reactor.running:
            reactor.stop()
    
    #This method is called when the connection to the server failed.
    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        if reactor.running:
            reactor.stop()

    def getProtocol(self):
        return self.protocol


if __name__ == "__main__":
    reactor.connectTCP('localhost', 1234, MyClientFactory())
    reactor.run()


