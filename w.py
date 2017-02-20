from __future__ import print_function
from bluetooth.ble import DiscoveryService, GATTRequester
import sys
import time

service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
    r = GATTRequester (address)
    print("Connecting...", end=' ')
    sys.stdout.flush()
    print (dir (r), r.is_connected ())
    time.sleep (2)
    r.connect (True)


