'''
@Author: Gruppe 3
'''

from verarbeitung import Verarbeitung
import os, time, sys
from threading import Thread
import server
import application


def main():
    print "Launched."

    if not os.path.exists("dataSaved.csv"):
        try:
            f = open("dataSaved.csv", "w")
        except IOError:
            print "Unable to create CSV file. Exiting."
            return
        else:
            f.close()

    v = Verarbeitung()
    v.loadData()
    v.saveDataCSV()

    t = Thread(target=application.realmain)
    t.start()
    print "Web server launched!"

    try:
        print "About to launch local server..."
        server.main(v)
    except KeyboardInterrupt:
        pass
    finally:
        print "Exiting. Saving data."
        v.saveData()
        t._Thread__stop()
        


if __name__ == "__main__":
    main()
