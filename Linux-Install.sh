#!/bin/bash
echo "This script will install the required dependencies for Ubuntu Server 23.10"
echo "This is a script to install Python 3.11 on Ubuntu 20.04"
echo "This script will install Python 3.11 from source"

sudo apt update
sudo apt upgrade

rm /usr/lib/python3.11/EXTERNALLY-MANAGED

echo "This will install pip3"
sudo apt install python3-pip

echo "This will install the required python3 libraries with pip3"
pip3 install -r requirements.txt

sudo apt install arduino

echo "Complete!"
