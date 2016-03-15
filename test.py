# -*- coding: utf-8 -*-
from ostregion import region
import sys

if len(sys.argv) != 2:
    configfile = None
else:
    configfile = sys.argv[1]

r = region('ost.ini')
print r.__dict__
#print get_mapped_resources(nova, keystone)
#print get_projects_utilization(keystone, ceilometer)
#for flavor in nova.flavors.list():
#    print flavor.__dict__
#for server in nova.servers.list():
#    print server.tenant_id
#    print server.flavor
#print get_full_capacity(nova)
#print get_allocated_capacity(nova,keystone)
#print get_project_max(ceilometer, '0c797009fbfb4513b236595875b91c18')
