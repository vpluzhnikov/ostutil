__author__ = 'vsevolodpluzhnikov'

from novaclient import client
from ConfigParser import ConfigParser
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='ost.log',
    filemode='w')

logger = logging.getLogger(__name__)

def load_config():
    consettings = ConfigParser()
    consettings.read('ost.ini')
    try:
        logger.debug('Read config file')
        return dict(consettings.items('Connection'))
    except:
        return None

def get_nova_connecton():
    config = load_config()
    if config:
        try:
            logger.debug('Establishing connection to nova')
            nova = client.Client(config['api_version'], config['username'], config['password'], config['tenant_name'],
                config['auth_url'], cacert = config['cacert'])
        except:
            return None
    else:
        return None
    return nova