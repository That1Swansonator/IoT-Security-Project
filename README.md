My primary goal is to create a secure and bespoke IoT network based on the three-layer approach using three security methods.

A bash file will; be made as a sort of installer.
rm /usr/lib/python3.11/EXTERNALLY-MANAGED for removing the PIP installation roadblock

The following bash commands is to install the necessary packages to control the gpio pins on the Raspberry Pi.
wget https://github.com/joan2937/lg/archive/master.zip
unzip master.zip
cd lg-master
make
sudo make install


