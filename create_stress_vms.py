# -*- coding: utf-8 -*-
from ostregion import region
from common import print_table
import sys
from time import sleep

if len(sys.argv) != 2:
    configfile = None
else:
    configfile = sys.argv[1]

r = region('ost.ini')

image = r.nova.images.find(name=r.config["test-image"])
net = r.nova.networks.find(label=r.config["test-net"])
flavor = r.nova.flavors.find(name=r.config["test-flavor"])

prefix = r.config["test-vm-prefix"]
total_vm_count = int(r.config["test-vm-count"])
vms_created = False
while not vms_created:
    if (total_vm_count - 10) > 10:
	num_vm = 10
    else:
	num_vm = total_vm_count
    for num in range(0,num_vm):
	vm_id = total_vm_count
	total_vm_count -= 1
	print "Creating vm with id = " + prefix+str(vm_id)
	server = r.nova.servers.create(name = prefix+str(vm_id), image = image.id, flavor = flavor.id, nics = [{'net-id':net.id}])
	sleep(1)
    print "Sleeping fo 10 seconds..."
    #sleep(10)
    if total_vm_count == 0:
	vms_created = True
ips = []
for serv in r.nova.servers.list():
    ips.append(serv.addresses)
print ips
    
    

#print server
#print image.__dict__, net.__dict__, flavor.__dict__
