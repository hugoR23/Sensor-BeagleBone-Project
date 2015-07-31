'''
@Author: Louis-Adrien DUFRENE, Hang YUAN
'''

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Client (LineReceiver):
        
    def connectionMade(self):
        print "Connection made"
        self.sendData()
    
    def connectionLost(self):
        print "Connection lost"
         
    def sendData(self):
        tuple1 = (150000000,-36)
        tuple2 = (150000156,57)
        tuple3 = (1155684658465,159)
        tuple4 = (15183513,123456789)
        tuple5 = (123456789,-1965)
        tuple6 = (15698745312,15.45)
        
        dict = {}        
        dict["TEMPERATURE"] = [tuple1, tuple2, tuple3]
        dict["HUMIDITY"] = [tuple4]
        dict["PLOP"] = [tuple5, tuple6]
        
        print "dict: " + str(dict)
        
        list = []
        
        string = ""
        
        for key, newlist in dict.iteritems():
        
            for tuple in dict[key]:
                string += "|" + str(tuple)
                
            list.append(key + string + "/")
            string = ""
        
        print "list: " + str(list)
        
        try:
            self.sendLine("".join(list))
            print "data sent: " + "".join(list)
            return True
            
        except:
            return False
    
    
class ClientFactory (ReconnectingClientFactory):
    
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return Client()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

if __name__ == "__main__":
    reactor.connectTCP('localhost', 1234, ClientFactory())
    reactor.run()
