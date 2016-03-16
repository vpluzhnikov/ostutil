# -*- coding: utf-8 -*-
from ostregion import region
from common import print_table
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
rows = []
rows.append(("Resource", "Total", "Allocated", "Running", "Utilized%"))
rows.append(("CPU", str(r.fullcapacity['cpu']), str(r.alloccapacity['alloc_cpu']),
             str(r.runningcapacity['running_cpu']), str(r.utilizedcapacity['total_cpu_util%'])))
rows.append(("RAM", str(r.fullcapacity['ram_mb']),  str(r.alloccapacity['alloc_ram_mb']),
             str(r.runningcapacity['running_ram_mb']), str(r.utilizedcapacity['total_ram_util%']) ))
print_table(rows)


#print "REGION STATISTICS"
#print ""
#print "CPU"
#print "Total;Allocated;Running;Utilized%"
#print str(r.fullcapacity['cpu']) + ";" + str(r.alloccapacity['alloc_cpu']) + ";" \
#      + str(r.runningcapacity['running_cpu']) + ";" + str(r.utilizedcapacity['total_cpu_util%'])
#print ""
#print "RAM"
#print "Total;Allocated;Running;Utilized%"
#print str(r.fullcapacity['memory_mb']) + ";" + str(r.alloccapacity['alloc_ram_mb']) + ";"\
#      + str(r.runningcapacity['running_ram_mb']) + ";" + str(r.utilizedcapacity['total_ram_util%'])
#


