#!/usr/bin/env python

#import rospy
from scapy.all import *

import os, argparse, sys, signal

import imp
db_man = imp.load_source('DB_Manager', '/home/eliana/git/Cinnamon/db.py')
cinnamon_man = imp.load_source('Sniffer', '/home/eliana/git/Cinnamon/Sniffer.py')

from listener import Listen

class CinnamonController:

    def __init__(self):
        rospy.init_node('cinnamon_controller', anonymous=False)
		rospy.loginfo("Started ")
        print("Started")
        self.stopSniff = False
        
        self.interface = "wlp3s0_mon"
        self.sniffer = cinnamon_man.Sniffer()

    def startSniff(self):
        print("Start to sniff from "+self.interface)
        sniff(iface=self.interface, prn=self.sniffer.sniffAP, stop_filter=self.checkStop, store=0)
        
    def setStopSniff(self, stop_sniff):
        self.stopSniff = stop_sniff

    def checkStop(self,p):
        if self.stopSniff:
            return True
        return False


if __name__ == '__main__':

    cinnamon = CinnamonController()

    listener = Listen(1, "Thread1", 2, cinnamon)
    listener.start()

    cinnamon.startSniff()
