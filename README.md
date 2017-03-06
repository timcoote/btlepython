# btlepython
Experimental code interacting with separate btle devices.
=======================================================
These python programs were run on f25 laptop with low-cost bt 4.0 dongle. Python modules loaded with sudo pip install <modulename>

The initial remote btle device was a PunchThrough Heart Rate Monitor

code must be run as sudo python <prog.py>

Notes on the different python snippets, which were looking at different bluez api wrappers
```
a.py - example pygatt program. does not work as the mac address of the simulator is not static
b.py - Working example of using bluepy. Shows the messiness of using API constants: must be correct ones, used
     - in the correct order to get any value. Original from http://bit.ly/2krYTul, but uses lessons from () to find the btle device.
     - part way through working out how to interact with individual characteristics (commented out in this commit).
     - includes the rather arbitrary code to get notifications of changes.
c.py - based on the btle.py test code, this iterates over the services and characteristics of the last found btle device.
     - example output when interacting with a PT BLE Glucose monitor is provided in c.out (from earlier version). Updated
     - to cope with devices that are either RANDOM or PUBLIC mac addresses
v.py - example pygatt program. shows actual interaction with cli, and the opacity of some of the returned items if
     - just viewed. Unclear on what this program iterates over in detail. Also in action it illustrates the asynchronous
     - nature of the bluez ble api.
w.py - failing api example: appears to not connect.
x.py - first cut program to interact with bluetooth. Failed!
y.py - pre-cursor to w.py, showing that a device with a mac address can be found
z.py - early bluepy version that didn't include getting the device to notify updates.

ww.py - original code that b.py was derived from
```
Environment
===========
this code was built on Fedora 25 and is likely to have dependencies on that repo. Below, I try to identify specific dependencies that
became visible during a port to python3
- needed the rpm python3-pip to install python dependencies
- added bluepy (sudo pip3 install bluepy)

We were finding that the package management wasn't working as cleanly as I'd like so I built a docker container to isolate the configurations.
I used [this page](http://bit.ly/2lUTZH8) to work out how to run bluez in a container

I've not yet checked the hosting of this container on anything other than i686 box running fedora 25. To create the container:
```
sudo docker build . # sudo is not necessary for 64bit docker host, I believe
```
this will throw some errors for missing keys and no controlling terminal. I don't know how to remove these at the moment.

then find the image hash with:
```
sudo docker images
```
and use the hash to run:
```
./go <image hash>
```
cd to /home/olly, and then run python c.py, which will identify BT devices and try to interrogate them

Errors
======
just to note that the programs run with sudo, or you get this error:
```
[olly@linux ~]$ python3 c.py 
Traceback (most recent call last):
  File "c.py", line 21, in <module>
    devs = scanner.scan (5.0)
  File "/usr/lib/python3.5/site-packages/bluepy/btle.py", line 631, in scan
    self.start()
  File "/usr/lib/python3.5/site-packages/bluepy/btle.py", line 569, in start
    self._mgmtCmd("le on")
  File "/usr/lib/python3.5/site-packages/bluepy/btle.py", line 240, in _mgmtCmd
    "Failed to execute mgmt cmd '%s'" % (cmd))
bluepy.btle.BTLEException: Failed to execute mgmt cmd 'le on'
```
