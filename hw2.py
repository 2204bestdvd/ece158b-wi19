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

POXDIR = os.environ[ 'HOME' ] + '/pox'


class POXHub( Controller ):
    "Custom Controller class to invoke POX forwarding.hub"
    def __init__( self, name, cdir=POXDIR,
                  command='python pox.py',
                  cargs=( 'openflow.of_01 --port=%s '
                          'forwarding.hub' ),
                  **kwargs ):
        Controller.__init__( self, name, cdir=cdir,
                             command=command,
                             cargs=cargs, **kwargs )


class POXSwitch( Controller ):
    "Custom Controller class to invoke POX forwarding.hub"
    def __init__( self, name, cdir=POXDIR,
                  command='python pox.py',
                  cargs=( 'openflow.of_01 --port=%s '
                          'forwarding.l2_learning' ),
                  **kwargs ):
        Controller.__init__( self, name, cdir=cdir,
                             command=command,
                             cargs=cargs, **kwargs )


controllers = { 'hub': POXHub, 'switch': POXSwitch }

if __name__ == '__main__':
    setLogLevel( 'info' )
    net = Mininet( topo=SingleSwitchTopo( 4 ), controller=POXHub )
    net.start()
    CLI( net )
    net.stop()

