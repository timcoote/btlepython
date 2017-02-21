# based on the test code at the bottom of bluepy/btle.py
from bluepy.btle import Peripheral, DefaultDelegate, Scanner, ADDR_TYPE_RANDOM, AssignedNumbers, BTLEException

import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

class HRM(Peripheral):
    def __init__(self, addr):
        print ("making an HRM at {}".format (addr))
        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_RANDOM)

if __name__=="__main__":

    hrm = None
    scanner = Scanner ().withDelegate(ScanDelegate())

    devs = scanner.scan (5.0)

    mac = ''

    for dev in devs:
        print ("Devices {}, ({}) RSSI {}".format (dev.addr, dev.addrType, dev.rssi))
        mac = dev.addr
        print (dev.__class__, mac)

    try:
        conn = Peripheral (mac, ADDR_TYPE_RANDOM)
    except BTLEException:
        pass

    print ("peripheral {}, services {} [{}]".format (conn, dir (conn), conn.getServices ()))

    try:
        for svc in conn.services:
            print (str (svc), svc.__class__, ":")
            for ch in svc.getCharacteristics ():
                print ("    {}, hnd={}, supports {}".format (ch, hex (ch.handle), ch.propertiesToString ()))
                chName = AssignedNumbers.getCommonName (ch.uuid)
    finally:
        conn.disconnect ()
