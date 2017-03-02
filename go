# $1 is the commit number of the docker instance

sudo docker run --net=host -t -i --privileged -v /dev/bus/usb:/dev/bus/usb -v /run/dbus:/run/dbus -v /var/run/dbus:/var/run/dbus --cap-add=ALL $1 /bin/bash
