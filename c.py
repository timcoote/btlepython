# based on the test code at the bottom of bluepy/btle.py
from bluepy.btle import Peripheral, DefaultDelegate, Scanner, ADDR_TYPE_PUBLIC, ADDR_TYPE_RANDOM, AssignedNumbers, BTLEException

import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)


if __name__=="__main__":

    scanner = Scanner ().withDelegate(ScanDelegate())

    devs = scanner.scan (5.0)

    mac = ''

    for dev in devs:
#        print ("Devices {}, ({}) RSSI {}".format (dev.addr, dev.addrType, dev.rssi))
        mac = dev.addr
#        print (dev.__class__, mac)

    try:
        conn = Peripheral (mac, ADDR_TYPE_PUBLIC)
        conn.getServices ()  # needed to get the services property populated?
    except BTLEException:
        try:
            conn = Peripheral (mac, ADDR_TYPE_RANDOM)
            conn.getServices ()
        except BTLEException as b:
            print ("btle exception".format (b))


#    print ("peripheral {}, services {}".format (conn, conn.services))

    try:
        for svcuuid in conn.services:
            svc = conn.getServiceByUUID (svcuuid)
            print (str (svc), ":")
            for ch in svc.getCharacteristics ():
                print ("    {}, hnd={}, supports {}".format (ch, hex (ch.handle), ch.propertiesToString ()))
#                chName = AssignedNumbers.getCommonName (ch.uuid)
#                print ("characteristic name {}".format (chName))

                if (ch.supportsRead()):
                    try:
                        print("    ->", repr(ch.read()))
                    except BTLEException as e:
                        print("Error: ->", e)

    finally:
        conn.disconnect ()
