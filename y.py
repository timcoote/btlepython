from gattlib import DiscoverService

service = DiscoverService ("hci0")
devices = service.discover (2)

print ("here {} {}".format (service, devices))

