# -*- coding: utf-8 -*-
from ostregion import region
import sys

if len(sys.argv) != 2:
    configfile = None
else:
    configfile = sys.argv[1]

r = region('ost.ini')
r.get_running_capacity()
r.get_utilization()
print "REGION STATISTICS"
print ""
print "CPU"
print "Total;Allocated;Running;Utilized%"
print str(r.fullcapacity['cpu']) + ";" + str(r.alloccapacity['alloc_cpu']) + ";" \
      + str(r.runningcapacity['running_cpu']) + ";" + str(r.utilizedcapacity['total_cpu_util%'])
print ""
print "RAM"
print "Total;Allocated;Running;Utilized%"
print str(r.fullcapacity['memory_mb']) + ";" + str(r.alloccapacity['alloc_ram_mb']) + ";"\
      + str(r.runningcapacity['running_ram_mb']) + ";" + str(r.utilizedcapacity['total_ram_util%'])


#print r.fullcapacity
#print "--- ALLOCATED CAPACITY ---"
#print r.alloccapacity
#print "--- RUNNING CAPACITY ---"
#print r.get_running_capacity()
#print "--- UTILIZED CAPACITY ---"
#print r.get_utilization()

