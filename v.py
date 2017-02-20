from __future__ import print_function
import pygatt
import binascii
import logging
import sys

#logging.basicConfig()
#logging.getLogger('pygatt').setLevel(logging.DEBUG)

adapter = pygatt.GATTToolBackend(gatttool_logfile=sys.stdout)
#adapter = pygatt.GATTToolBackend()

try:
    adapter.start ()
    devs = adapter.scan ()
    print (devs)
    for d in devs:
        name = d['name']
        print ("name {}".format (name))
        if name == u'Heart Rate':
            address = d ['address']
            print (name, address)
            dev = adapter.connect (address, 10, pygatt.backends.BLEAddressType.random)
            break

    characs = dev.discover_characteristics ()

#    print ("characteristics and type {}, {}".format (characs, characs.__class__))
    for k, v in characs.iteritems ():
#        print ("characterisic name {} and type: {},  value {} and type: {}, char handle: {} ** {}".format (k,k.__class__, v, v.__class__, dir (v), v.descriptors))
#        print("Read UUID %s: %s" % (k, binascii.hexlify(dev.char_read(k))))

        try:
            for r in range (0x23, 0x2d):
                val = dev.char_read_handle ("0x00{:02x}".format (r))
                print ("bytarray from {} : {}".format (r, binascii.hexlify (val)))

        except Exception as (e):
            print ("could not read characteristic {}".format (k))

#"""        try:
#            print ("read UUID {}: {}".format (k, binascii.hexlify (dev.char_read(c, timeout=10))))
#            print ("hanndread UUID {}: {}".format (c, binascii.hexlify (dev.get_handle(c, timeout=10))))
#        except Exception as e:
#            print (e)
##    print (characs, dir(characs))
#
#    print (dir(dev))
#"""

finally:
    adapter.stop ()
