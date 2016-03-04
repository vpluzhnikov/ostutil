# -*- coding: utf-8 -*-
from regionres import get_avaiable_hosts
from common import get_session, get_nova_connecton
import sys

if len(sys.argv) != 2:
    configfile = None
else:
    configfile = sys.argv[1]

session=get_session(configfile)

print get_avaiable_hosts(get_nova_connecton(session))