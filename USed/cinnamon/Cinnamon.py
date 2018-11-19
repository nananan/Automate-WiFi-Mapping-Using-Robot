#!/usr/bin/python

from scapy.all import *

import os, argparse, sys, signal
from multiprocessing import Process

from Sniffer import Sniffer

interface = ''
bssid = None
stopper = False

monitor_enable  = 'ifconfig wlp2s0 down; iw dev wlp2s0 interface add wlp2s0_mon type monitor; ifconfig wlp2s0_mon up'
monitor_disable = 'iw dev wlp2s0_mon del; ifconfig wlp2s0 up'

def channel_hopper(channel):
	# if (channel != None):
	# 	try:
	# 		os.system("iw dev %s set channel %d" % (interface, channel))
	# 		time.sleep(1)
	# 	except KeyboardInterrupt:
	# 		print("Exception")
	# else:
	while True:
		try:
			channel = random.randrange(1,15)
			os.system("iw dev %s set channel %d" % (interface, channel))
			time.sleep(1)
		except KeyboardInterrupt:
			break

def filterFunc(p):
	if p.addr1 == bssid or p.addr2 == bssid or p.addr3 == bssid:
		return True
	return False

def signal_handler(signal, frame):
	# p.terminate()
	# p.join()
	stopper = True

	os.system(monitor_disable)
	print("\n-=-=-=-=-=  END =-=-=-=-=-=-")
	os._exit(0)

def stopperCheck(p):
	if stopper:
		return True
	return False



if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Cinnamon.py')
	parser.add_argument('-i', '--interface', dest='interface', type=str, required=False, help='Interface to use for sniffing')
	parser.add_argument('-b', '--bssid', dest='bssid', type=str, required=False, help='Bssid to set')
	parser.add_argument('-c', '--channel', dest='channel', type=str, required=False, help='Channel to set')
	args = parser.parse_args()
	
	user = os.getenv("SUDO_USER")
	
	if user is None:
		print("This program needs 'sudo'")
	else:
		print('Press CTRL+c to stop sniffing...')

		os.system(monitor_enable)

		filterStr = ""
   		if args.channel != None:
   			#os.system("systemctl stop networking")
   			os.system("ifconfig %s down" % (args.interface))
			os.system("iw dev %s set channel %d" % (args.interface, int(args.channel)))
   			os.system("ifconfig %s up" % (args.interface))
		
		if args.bssid != None:
			bssid = args.bssid

		if args.interface != None:
			interface = args.interface

			sniffer = Sniffer()


			# channel_set = False
			# if args.channel != None:
			# 	p = Process(target = channel_hopper(args.channel))
			# 	channel_set = True
			print("-=-=-=-=-=-= cinnamon.py =-=-=-=-=-=-")
			print("CH ENC BSSID			 SSID")
			#if channel_set == False:
			# p = Process(target = channel_hopper(None))
			# p.start()
			signal.signal(signal.SIGINT, signal_handler)

			if bssid != None:
				sniff(lfilter=filterFunc, iface=args.interface, prn=sniffer.sniffAP, stop_filter=stopperCheck, store=0)
			else:
				sniff(iface=args.interface, prn=sniffer.sniffAP, stop_filter=stopperCheck, store=0)


			# sniff(iface=interface,prn=sniffAP)

