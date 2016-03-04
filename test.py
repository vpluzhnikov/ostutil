# -*- coding: utf-8 -*-
from regionres import get_avaiable_hosts, get_projects
from common import get_session, get_nova_connecton, get_keystone_connection
import sys

if len(sys.argv) != 2:
    configfile = None
else:
    configfile = sys.argv[1]

session=get_session(configfile)

#print get_nova_connecton(session)
print get_projects(get_keystone_connection(session))
#print get_avaiable_hosts(get_nova_connecton(session))
