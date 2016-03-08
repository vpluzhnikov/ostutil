# -*- coding: utf-8 -*-
__author__ = 'vsevolodpluzhnikov'

from novaclient import client as client_nova
from ceilometerclient import client as client_ceilometer
from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client as client_keystone
from ConfigParser import ConfigParser
from novaclient.v2.quotas import QuotaSet

import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='ost.log',
    filemode='w')

logger = logging.getLogger(__name__)

def get_session(configfile):
    config = load_config(configfile)
    if config:
        try:
            auth = v3.Password(username=config['username'],
                password=config['password'],
                project_name=config['tenant_name'],
                auth_url=config['auth_url'],
                user_domain_name=config['domain'],
                project_domain_name=config['domain'],)
            sess = session.Session(auth=auth, verify=config['cacert'])
            return sess
        except:
            logger.error('Error for authentication with credentials from ' + configfile)
            return None
    else:
        return None

def get_keystone_connection(session):
    return client_keystone.Client(session=session)

def get_nova_connecton(session):
    return client_nova.Client(2, session=session)

def get_ceilometer_connecton(session):
    return client_ceilometer.Client(2, session=session)


def load_config(configfile):
    consettings = ConfigParser()
    consettings.read(configfile)
    try:
        logger.debug('Read config file ' + configfile)
        return dict(consettings.items('Connection'))
    except:
        logger.error('Error while reading configuration from ' + configfile)
        return None

