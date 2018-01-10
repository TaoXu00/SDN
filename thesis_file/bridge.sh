 #!/bin/bash
sudo ifconfig br0 down
sudo brctl delbr br0

 brctl addbr br0
 brctl addif br0 s1
 brctl addif br0 eth0
 ifconfig eth0 0.0.0.0
 ifconfig br0 10.0.0.8 netmask 255.255.0.0 up
