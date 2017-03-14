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
     - this commit does have working notifications for the seat pad, for both python2 and python3. Returned values look arbitrary.
     - had to faff with the returned handles to find the right one to write to to get the notification (base+2). Documentation on github
     - indicated that it ought to be base+1 (!) This is confused further as the reported handle by bluetoothctl is 34 (dec) with a control
     - handle of 35 (dec)!
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

Notes
=====
Something is confusing about setting up the notification code. According to various posts on the bluepy github site, the handle to write '\1\0'
to is the next value after the handle reporting the characteristic (e.g. http://bit.ly/2mVdeBr). However, the code that works has to write to
the value 2 more than the handle reportedly associated with the NOTIFY capability (see code in b.py). The actual handle for the seat up/down
event is x21 or 33 dec, and the write works to x23/35.

However, when interrogating the device using bluetoothctl (which uses the dbus interface, rather than the hcitool/gatttool interface used by
bluepy), the handle that can be read which gives the status of the seat is x22. I'm not clear what handle x21 does:
```
[00:07:80:B4:61:40][LE]> primary
attr handle: 0x0001, end grp handle: 0x0007 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x0008, end grp handle: 0x000b uuid: 00001809-0000-1000-8000-00805f9b34fb
attr handle: 0x000c, end grp handle: 0x001b uuid: 0000180a-0000-1000-8000-00805f9b34fb
attr handle: 0x001c, end grp handle: 0x001f uuid: 0000180f-0000-1000-8000-00805f9b34fb
attr handle: 0x0020, end grp handle: 0xffff uuid: 79f7744a-f8e6-4810-8f16-140b6974835d
[00:07:80:B4:61:40][LE]> char-read-uuid  79f7744a-f8e6-4810-8f16-140b6974835d
Error: Read characteristics by UUID failed: No attribute found within the given range
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0020
Characteristic value/descriptor: 5d 83 74 69 0b 14 16 8f 10 48 e6 f8 4a 74 f7 79 
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0021
Characteristic value/descriptor: 12 22 00 2f a4 0d e9 4a aa 5f 98 0a 43 26 23 25 5f 69 64 
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0022
Characteristic value/descriptor: 0f 53 
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0022
Characteristic value/descriptor: 0f 53 
[00:07:80:B4:61:40][LE]> char-write-req 0x0021 0x0100
Error: Characteristic Write Request failed: Attribute can't be written
[00:07:80:B4:61:40][LE]> char-write-req 0x0020 0x0100
Error: Characteristic Write Request failed: Attribute can't be written
[00:07:80:B4:61:40][LE]> char-write-req 0x0022 0x0100
Error: Characteristic Write Request failed: Attribute can't be written
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0020
Characteristic value/descriptor: 5d 83 74 69 0b 14 16 8f 10 48 e6 f8 4a 74 f7 79 
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0021
Characteristic value/descriptor: 12 22 00 2f a4 0d e9 4a aa 5f 98 0a 43 26 23 25 5f 69 64 
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0022
Characteristic value/descriptor: 0f 53 
[00:07:80:B4:61:40][LE]> char-write-req 0x0023 0x0100
Error: Characteristic Write Request failed: Attribute value length is invalid
[00:07:80:B4:61:40][LE]> char-write-req 0x0023 0x10
Characteristic value was written successfully
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0022
Characteristic value/descriptor: 0f 53 
[00:07:80:B4:61:40][LE]> char-read-hnd 0x0022
Characteristic value/descriptor: 2d 53 
[00:07:80:B4:61:40][LE]> char-write-req 0x0023 0100
Characteristic value was written successfully
Notification handle = 0x0022 value: 0f 53 
Notification handle = 0x0022 value: 2d 53 
Notification handle = 0x0022 value: 0f 53 
Notification handle = 0x0022 value: 2d 53 
```

Maybe I need to check more carefully what I'm looking at here and query bluepy as to what's happening.

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
