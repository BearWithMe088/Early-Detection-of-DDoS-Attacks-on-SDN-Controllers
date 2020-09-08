# dicrete time analysis in form of number of packets is done 
# i.e. after every 50 packets, entropy is calucted
# if in a particular interval the entropy is below the threshold then lower the count where DDoS detection number is preserved
# our aim here is to detect the DDoS attack within 250 packets
# therefore the count to DDoS attack detection should be 5
# as the number of packets is 50, in 5 times if the attack has happened the value of entropy will drop and we will know the attack has happened

import math
from pox.core import core
log = core.getLogger()

class Entropy(object):
	count = 0
	entDic = {}  # entropy dictionary
	ipList = []  
	dstEnt = [] 
	value = 1    # initially it should be 1

	def statcolect(self, element):
		l = 0
		self.count +=1
		self.ipList.append(element)
		if self.count == 50:
			for i in self.ipList:
				l +=1
				if i not in self.entDic:
					self.entDic[i] =0
				self.entDic[i] +=1
			self.entropy(self.entDic)
			log.info(self.entDic)
			self.entDic = {}
			self.ipList = []
			l = 0
			self.count = 0

	def entropy (self, lists):
		l = 50
		elist = []
		for k,p in lists.items():
			'''
			log.info("p is")
			log.info(p)
			log.info("P is obtained from")
			log.info(k)
			log.info("l is")
			log.info(l)
			'''
			c = p/float(l)
			c = abs(c)
			elist.append(-c * math.log(c, 10))
			log.info('Entropy = ')
			log.info(sum(elist))
			self.dstEnt.append(sum(elist))
		if(len(self.dstEnt)) == 80:
			print self.dstEnt
			self.dstEnt = []
                self.value = sum(elist)

	def __init__(self):
		pass
# our aim here is to detect the DDoS attack within 250 packets
# therefore the count to DDoS attack detection should be 5
# as the number of packets is 50, in 5 times if the attack has happened the value of entropy will drop and we will know the attack has happened
