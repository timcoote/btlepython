from bluepy.btle import Peripheral, DefaultDelegate, Scanner, ADDR_TYPE_RANDOM, AssignedNumbers

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
    cccid = AssignedNumbers.client_characteristic_configuration
    hrmid = AssignedNumbers.heart_rate

#    hrmmid = AssignedNumbers.heart_rate_measurement

    hrm = None
    scanner = Scanner ().withDelegate(ScanDelegate())

    devs = scanner.scan (10.0)

    mac = ''

    for dev in devs:
        print ("Devices {}, ({}) RSSI {}".format (dev.addr, dev.addrType, dev.rssi))
        print (dev.__class__)
        mac = dev.addr


    try:
#        hrm = HRM('cb:d7:a0:40:c4:01')
        hrm = HRM(mac)

        service, = [s for s in hrm.getServices() if s.uuid==hrmid]
#        ccc, = service.getCharacteristics(forUUID=str(hrmmid))

        if 0: # This doesn't work
            ccc.write('\1\0')

        else:
            desc = hrm.getDescriptors(service.hndStart,
                                      service.hndEnd)
            d, = [d for d in desc if d.uuid==cccid]
            print [x.uuid.getCommonName () for x in desc], dir (d), desc, dir (desc [0].uuid), desc [0].uuid
#            for d in desc:
#                print d, dir (d)
#            d, = [d for d in desc if d.uuid==AssignedNumbers.body_sensor_location]

            hrm.writeCharacteristic(d.handle, '\1\0')

        t0=time.time()
        def print_hr(cHandle, data):
            bpm = ord(data[1])
            print "len data", len(data), data.__class__
#            bpm = ord(data[0])
            print bpm,"%.2f"%(time.time()-t0)
        hrm.delegate.handleNotification = print_hr

        for x in range(100):
            hrm.waitForNotifications(3.)

    finally:
        if hrm:
            hrm.disconnect()
