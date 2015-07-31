'''
@Author: Louis-Adrien DUFRENE, Hang YUAN
'''

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from verarbeitung import Verarbeitung
import argparse, time
from twisted.internet.error import ConnectionDone


v = None

#The class Server inherits from the protocol LineReceiver.
#There will be one instance of this class for each client connected to the server.
class Server (LineReceiver):
    
    #This method is called whe the server receives datas from the client.
    def lineReceived(self, line):
        global v
        print "Data received."

        mylist = line.split("/")#Here it separates each group key|tuples.
        mylist.pop()
        mydict = {}
        
        for word in mylist:
        
            list_temp = word.split("|")#Here it separates the key and each tuple.
            list_tuple = []
            key = list_temp[0]#Here is the key.
            
            for i in range(1,len(list_temp)):
                list_tuple.append(eval(list_temp[i]))
                
            mydict[key] = list_tuple#Here we create the new dictionnary.
            
        v.addData(mydict)
        print "Data added."
        
        if not v.saveDataCSV():
            print "Unable to save data."
        else:
            print "Data saved."
    
    #This method is called when the connexion with the client is made. 
    def connectionMade(self):
        self.sendLine(str(time.time() + 7200))
        print "Connection made."
    
    #This method is called when the connexion with the client is lost.
    def connectionLost(self, reason=ConnectionDone):
        print "Connection lost: " + reason.getErrorMessage()

#This class is the factory used to create the server instance. It inherits from Factory.
#Each time a new client tries to connect to the server, the ServerFactory will called the method buildProtocol.        
class ServerFactory (Factory):

    def buildProtocol(self, addr):
        return Server()

def main(verInstance=None):
    global v

    parser = argparse.ArgumentParser(description='Python server to listen to BeagleBone client.')#The ArgumentParser object will hold all the information necessary to parse the command line into Python data types
    parser.add_argument('-p', '--port', default=1234, type=int, help="Remote server port.")
    args = parser.parse_args()
    
    if verInstance != None:
        v = verInstance
    else:
        v = Verarbeitung()

    reactor.listenTCP(args.port, ServerFactory())
    reactor.run()

if __name__ == "__main__":
    main()



    
