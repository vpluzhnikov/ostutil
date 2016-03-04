# -*- coding: utf-8 -*-
from regionres import get_full_capacity, get_allocated_capacity
from common import get_session, get_nova_connecton, get_keystone_connection
import sys

if len(sys.argv) != 2:
    configfile = None
else:
    configfile = sys.argv[1]

session=get_session(configfile)
nova = get_nova_connecton(session)
keystone = get_keystone_connection(session)

print get_full_capacity(nova)
print get_allocated_capacity(nova,keystone)
