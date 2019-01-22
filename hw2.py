#!/usr/bin/python
###
# UCSD ECE 158B Assignment 2 example script
# Modified from Introduction to Mininet example script
# https://github.com/mininet/mininet/wiki/Introduction-to-Mininet
###

from mininet.net import Mininet
from mininet.node import Controller
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel

import os

class POXHub( Controller ):
    "Custom Controller class to invoke POX forwarding.hub"
    def start( self ):
        "Start POX hub"
        self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]
        self.cmd( self.pox, 'forwarding.hub &' )
    def stop( self ):
        "Stop POX"
        self.cmd( 'kill %' + self.pox )


class POXBridge( Controller ):
    "Custom Controller class to invoke POX forwarding.l2_learning"
    def start( self ):
        "Start POX learning switch"
        self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]
        self.cmd( self.pox, 'forwarding.l2_learning &' )
    def stop( self ):
        "Stop POX"
        self.cmd( 'kill %' + self.pox )

controllers = { 'hub': POXHub, 'bridge': POXBridge }

if __name__ == '__main__':
    setLogLevel( 'info' )
    net = Mininet( topo=SingleSwitchTopo( 4 ), controller=POXBridge )
    net.start()
    CLI( net )
    net.stop()

