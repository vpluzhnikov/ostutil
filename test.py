# -*- coding: utf-8 -*-
from regionres import get_full_capacity, get_allocated_capacity, get_project_max, get_mapped_resources, get_flavors
from common import get_session, get_nova_connecton, get_keystone_connection, get_ceilometer_connecton
import sys

if len(sys.argv) != 2:
    configfile = None
else:
    configfile = sys.argv[1]

session=get_session(configfile)
nova = get_nova_connecton(session)
keystone = get_keystone_connection(session)
ceilometer = get_ceilometer_connecton(session)

#print get_flavors(nova)
print get_mapped_resources(nova, keystone)
#for flavor in nova.flavors.list():
#    print flavor.__dict__
#for server in nova.servers.list():
#    print server.tenant_id
#    print server.flavor
#print get_full_capacity(nova)
#print get_allocated_capacity(nova,keystone)
#print get_project_max(ceilometer, '0c797009fbfb4513b236595875b91c18')