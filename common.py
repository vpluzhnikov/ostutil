# -*- coding: utf-8 -*-
__author__ = 'vsevolodpluzhnikov'

from novaclient import client as client_nova
from ceilometerclient import client as client_ceilometer
from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client as client_keystone
from ConfigParser import ConfigParser

import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='ost.log',
    filemode='w')

logger = logging.getLogger(__name__)

def load_config(configfile):
    consettings = ConfigParser()
    consettings.read(configfile)
    try:
        logger.debug('Read config file ' + configfile)
        return dict(consettings.items('Connection'))
    except:
        logger.error('Error while reading configuration from ' + configfile)
        return None

def build_query(resource_id, metric):
    return [dict(field='resource_id', op='eq', value=resource_id), dict(field='meter',op='eq',value=metric)]

def print_table(lines, separate_head=True):
    """Prints a formatted table given a 2 dimensional array"""
    #Count the column width
    widths = []
    for line in lines:
        for i,size in enumerate([len(x) for x in line]):
            while i >= len(widths):
                widths.append(0)
            if size > widths[i]:
                widths[i] = size

    #Generate the format string to pad the columns
    print_string = ""
    for i,width in enumerate(widths):
        print_string += "{" + str(i) + ":" + str(width) + "} | "
    if (len(print_string) == 0):
        return
    print_string = print_string[:-3]

    #Print the actual data
    for i,line in enumerate(lines):
        print(print_string.format(*line))
        if (i == 0 and separate_head):
            print("-"*(sum(widths)+3*(len(widths)-1)))