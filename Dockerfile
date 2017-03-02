FROM docker.io/32bit/debian
ADD * /home/olly/
WORKDIR /home/olly
RUN apt-get -y update
RUN apt-get -y install libglib2.0-dev python python-pip libglib2.0-dev bluez usbutils
RUN pip install bluepy
