#!/bin/bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
rm -r /home/xu/mininet/H1Dir
rm -r /home/xu/mininet/H2Dir
mkdir /home/xu/mininet/H1Dir
mkdir /home/xu/mininet/H2Dir
pkill iperf




