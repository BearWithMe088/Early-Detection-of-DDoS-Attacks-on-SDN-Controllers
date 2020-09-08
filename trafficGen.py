# this code will generate random source IP address  
# will send the packet to random desitanation between the host
# the start and end value will be provided as command line arguments
# the value will be corresponding to a particular node, say hi 
# where i is between 1 to 64 as per the mininet network topology
# to run this code go to /mininet/custom
# then give command: python trafficGen.py -s 2 -e 60
# do this only after you are in the xterm window of that particular node
# this will generate the traffic/packets from a particular node/host. 

import sys
import time
from random import randrange
import getopt  # for parsing the command line arguments
from os import popen  # will fetch the shell commands into python
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


def genDestIP(start, end):

    firstOctate = 10
    secondOctate =0
    thirdOctate =0
    IPaddr = ".".join([str(firstOctate),str(secondOctate),str(thirdOctate),str(randrange(start,end))])
    return IPaddr

def main(argv):
    print (argv)
#exception handling
    try:
        opts, args = getopt.getopt(sys.argv[1:],'s:e:',['start=','end='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt =='-s':
            start = int(arg)
        elif opt =='-e':
            end = int(arg)

    if start == '':
        sys.exit()
    if end == '':
        sys.exit()

	# open the ethernet interface to send packet
	# ifconfig will read the IP addr
	# awk will read the contents, it is a text parser
    interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()

    for i in xrange(1000):
	# do not directly use the IP, use with Ether()/IP then only it works
        packets = Ether()/IP(dst=genDestIP(start, end),src=genSourceIP())/UDP(dport=80,sport=2)
	#UDP source port= 2 and destination port =80
        
	print(repr(packets))

        sendp(packets,iface=interface.rstrip(),inter=0.1)

if __name__ == '__main__':   # will avoid the main when other programs are running
    main(sys.argv)
