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
vms_deleted = False
vol_list = []
while not vms_deleted:
    if (total_vm_count - 10) > 10:
	num_vm = 10
    else:
	num_vm = total_vm_count
    for num in range(0,num_vm):
	vm_id = total_vm_count
	total_vm_count -= 1
	print "Deleting vm with id = " + prefix+str(vm_id)
	server = r.nova.servers.find(name = prefix+str(vm_id))
	vol_list += r.nova.volumes.get_server_volumes(server.id)
	server.delete()
    if total_vm_count == 0:
	vms_deleted = True

print "Cleanup for volumes"
sleep(5)

for vol in vol_list:
    r.nova.volumes.delete(vol.id)

