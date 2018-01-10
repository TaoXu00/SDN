 #!/bin/bash
sudo mn -c
#start floodlight
cd floodlight
java -jar target/floodlight.jar &
cd ..
#start xampp server
/opt/lampp/lampp start
#start mininet topology
sleep 3	
cd topologyGenerator
sudo python Netgenerator.py full.out linkSetting
#sudo python mytopology2.py			
