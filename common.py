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