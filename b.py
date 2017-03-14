from bluepy.btle import Peripheral, DefaultDelegate, Scanner, ADDR_TYPE_RANDOM, AssignedNumbers, ADDR_TYPE_PUBLIC

import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

t0=time.time()

# callback to print out values.

def print_hr(cHandle, data):
#    bpm = ord(data[1]) # python2
    bpm = data
    print ("len data", len(data), data.__class__)
#    bpm = ord(data[0])
#    bpm1 = data[0]
    print (bpm,"%.2f"%(time.time()-t0))

class HRM(Peripheral):
    def __init__(self, addr):
        print ("making an HRM at {}".format (addr))
#        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_RANDOM) # random for hrm on ipad, public for seat pad
        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_PUBLIC)

if __name__=="__main__":
    cccid = AssignedNumbers.client_characteristic_configuration
    hrmid = AssignedNumbers.heart_rate

#    hrmmid = AssignedNumbers.heart_rate_measurement

    hrm = None
    scanner = Scanner ().withDelegate(ScanDelegate())

    devs = scanner.scan (5.0)

    mac = ''

    for dev in devs:
        print ("Devices {}, ({}) RSSI {}".format (dev.addr, dev.addrType, dev.rssi))
        print (dev.__class__)
        mac = dev.addr


    try:
        hrm = HRM(mac)

# I think that getServices() is required to cache the values
        hrm.getServices()
# set callback for notifications
        hrm.delegate.handleNotification = print_hr

        for s in hrm.services:
            service = hrm.getServiceByUUID (s)
            print ("service: {}".format (str (service)))
            for ch in service.getCharacteristics ():
#                print (dir (ch))
                print ("    {}, hnd ={}, support {}".format (ch, ch.handle, ch.propertiesToString ()))
                if ch.supportsRead ():
                    print ("        val: {}".format (repr (ch.read ())))
                if "NOTIFY" in ch.propertiesToString ():
                    print ("trying to set up notify for characteristic @hndl {}".format (ch.handle))
#                    hrm.writeCharacteristic (ch.handle, b'\x0100') # this is definitely wrong
#                    hrm.writeCharacteristic (ch.handle+1, '\1\0') # python2
#                    hrm.writeCharacteristic (35, '\1\0') # python2 - works with literal
#                    hrm.writeCharacteristic (35, b'\1\0') # python3 - works with literal
                    hrm.writeCharacteristic (ch.handle+2, b'\1\0') # python3 -
#                    hrm.writeCharacteristic (ch.handle, '\1\0') # python2
#                    hrm.writeCharacteristic (ch.handle, b'\1\0') # python3?
                    print ("completed")



        for x in range(10):
            print (x)
            hrm.waitForNotifications(3.)

    finally:
        if hrm:
            hrm.disconnect()
