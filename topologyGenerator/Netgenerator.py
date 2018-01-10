#!/usr/bin/python

"""
This imports config from a VirtualNetworkGraph.py .out file and creates
a network with the same node connectivity.
"""
import sys
import os
import time
import thread
import socket
import subprocess
import pickle
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
from mininet.node import Controller, RemoteController, OVSSwitch
from random import randint

s_linkList = {}
switchList = []
hostList = []
h_bw = {}
#paths = []
#path_costs = {}
#prev_ema = {}

#FOR FULL OR RANDOM
class FullTopo(Topo):
        def build(self, switches, hosts, s_links, h_bw,file):
                file.write("link bandwidth"+'\n')
                currHost = 0
                for switch in switches:
                        self.addSwitch(switch,protocols=["OpenFlow13"])
		for host in hosts:
                        self.addHost(host)
                #links between switches
                for key in s_links:
                        self.addLink(key[0],key[1],bw=s_links[key][0])
			file.write(key[0]+"<->"+key[1]+":"+str(s_links[key][0])+'\n')
                        #links between hosts and switches
                        if  key[0] in switches:
				#print key[0]+" "+hosts[currHost]
				self.addLink(key[0],hosts[currHost],bw=h_bw[key[0]])
				file.write(key[0]+"<->"+hosts[currHost]+":"+str(h_bw[key[0]])+'\n')
                                switches.remove(key[0])
                                currHost = currHost + 1
		self.addLink(switches[0],hosts[currHost],bw=h_bw[switches[0]])
		file.write(switches[0]+"<->"+hosts[currHost]+":"+str(h_bw[switches[0]])+'\n')
class StarTopo (Topo):
        def build(self, nodes, hosts, s_links, h_queue):
                currHost = 0
                for s in range(0,len(nodes)):
                        self.addSwitch(nodes[s],cls = OVSSwitch, protocols='OpenFlow13')
                        self.addHost('h'+str(s+1))
                for key in s_links:
                        self.addLink(key[0],key[1],bw=s_links[key][0], delay=s_links[key][1], loss=s_links[key][2], max_queue_size=s_links[key][3], use_htb=True)
                        self.addLink(hosts[currHost], nodes[currHost+1],max_queue_size=h_queue[currHost],use_htb=True)
                        currHost = currHost + 1
                self.addLink(hosts[currHost], nodes[0])

class LinearTopo (Topo):
        def build(self, nodes, hosts, s_links, h_queue):
                currHost = 0
                for s in range(0,len(nodes)):
                        self.addSwitch(nodes[s],cls = OVSSwitch, protocols='OpenFlow13')
                        self.addHost('h'+str(s+1))
                for key in s_links:
                        self.addLink(key[0],key[1],bw=s_links[key][0], delay=s_links[key][1], loss=s_links[key][2], max_queue_size=s_links[key][3], use_htb=True)
                        self.addLink(hosts[currHost],nodes[currHost],max_queue_size=h_queue[currHost],use_htb=True)
                        currHost = currHost + 1
                # Add last host to last node2 switch...
                self.addLink(hosts[currHost], nodes[currHost],max_queue_size=h_queue[currHost],use_htb=True)

class DiamondTopo (Topo):
        def build(self, nodes, hosts, s_links, h_queue):
                currHost = 0
                for s in range(0,len(nodes)):
                        self.addSwitch(nodes[s],cls = OVSSwitch, protocols='OpenFlow13')
                self.addHost('h1')
                self.addHost('h2')
                for key in s_links:
                        self.addLink(key[0],key[1],bw=s_links[key][0], delay=s_links[key][1], loss=s_links[key][2], max_queue_size=s_links[key][3], use_htb=True)
                self.addLink('h1','s1', max_queue_size=h_queue[0],use_htb=True)
                self.addLink('h2','s4', max_queue_size=h_queue[1],use_htb=True)

def writeConnectionsAndIPTofile(net,file): 
     file.write("connections"+'\n')
     for link in net.links:
       file.write(str(link)+'\n')
     file.write("IP"+'\n')
     for host in net.hosts:
        file.write(host.name+ ' '+host.IP()+'\n')
     file.close()

def createNet(filename, li):
    f = open(filename)
    links = open(li)

    for line in f:
        s_link = links.readline()
        #bw, delay, loss, queue = s_link.split(' ')
	bw=s_link.split(' ')[0]
        node1,node2 = line.split()
        s1 = "s"+str(int(node1)+1)
        s2 = "s"+str(int(node2)+1)
	#check duplicate links between switchs
        if (s1,s2) not in s_linkList and (s2,s1) not in s_linkList:
		s_linkList[(s1,s2)] = [int(bw.strip())]
		if s1 not in switchList:
		    switchList.append(s1)
		if s2 not in switchList:
		    switchList.append(s2)
		h1 = "h"+str(int(node1)+1)
		h2 = "h"+str(int(node2)+1)
		if h1 not in hostList:
		    hostList.append(h1)
		if h2 not in hostList:
		    hostList.append(h2)
   
    h = links.readline().split(' ')
   # print h
    i=1
    for q in h:
	key='s'+str(i)
        h_bw[key]=int(q.strip())
	i +=1
    f.close()
    links.close()
    file=open("hostsInfo.txt","w")
    if (filename == "linear.out"):
        topo = LinearTopo(switchList, hostList, s_linkList, h_bw,file)
    elif (filename == "star.out"):
        topo = StarTopo(switchList, hostList, s_linkList, h_bw)
    elif (filename == "diamond.out"):
        topo = DiamondTopo(switchList, hostList, s_linkList, h_bw)
    else:       #full or random
        topo = FullTopo(switchList, hostList, s_linkList, h_bw,file)

   # net = Mininet(topo=topo, link=TCLink, controller=RemoteController)
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController( name, ip='127.0.0.1',port=6633),
        switch=OVSSwitch,
        autoSetMacs=True,
        link=TCLink)
   
    writeConnectionsAndIPTofile(net,file)
    info( '*** Starting network\n')
    net.start()
    os.system("bash bridge.sh")
    for host in net.hosts:
	host.cmd("cd ..")
        host.cmd("cd migrationServer") 
        #result=host.cmd("pwd")
        result=host.cmd("java -jar migrationServer.jar &")
	#host.cmd('ps aux')
       # print(host.IP()+" running migration Server") 
    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()
    


if __name__ == '__main__':

    setLogLevel( 'info' )
createNet(sys.argv[1], sys.argv[2])
