#!/usr/bin/python

import threading, curses, sys

import time
from time import sleep

from pynput.keyboard import Key, Listener
user = 'eliana'
import imp
cinnamon_man = imp.load_source('Sniffer', '/home/'+user+'/git/Cinnamon/Sniffer.py')


class Listen (threading.Thread):
    
    def on_press(self, key):
        print('{0} pressed'.format(key))

    def on_release(self, key):
        print('{0} release'.format(key))
        if key == Key.esc:
            # Stop listener
            self.cinnamon.setStopSniff(True)
            return False

    def __init__(self, threadID, name, delay, cinnamon):
        threading.Thread.__init__(self)
        #self.setDaemon(True)
        
        self.cinnamon = cinnamon
        
    def run(self):
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()





