#!/bin/sh
wget https://app.conveyordata.com/api/info/cli/location/linux/amd64 -O conveyor_linux_amd64.tar.gz
tar -zxvf conveyor_linux_amd64.tar.gz
chmod +x bin/linux/amd64/conveyor 
sudo cp bin/linux/amd64/conveyor /usr/local/bin/conveyor
rm conveyor_linux_amd64.tar.gz