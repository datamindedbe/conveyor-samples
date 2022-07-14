#!/bin/sh
set -e

wget https://app.conveyordata.com/api/info/cli/location/linux/amd64 -O conveyor_linux_amd64.tar.gz
tar -zxvf conveyor_linux_amd64.tar.gz --one-top-level
chmod +x conveyor_linux_amd64/bin/linux/amd64/conveyor 
sudo cp conveyor_linux_amd64/bin/linux/amd64/conveyor /usr/local/bin/conveyor
rm conveyor_linux_amd64.tar.gz
rm -rf conveyor_linux_amd64/