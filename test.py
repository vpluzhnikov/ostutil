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
rows.append(("RAM (Mb)", str(r.fullcapacity['ram_mb']),  str(r.alloccapacity['ram_mb']),
             str(r.runningcapacity['running_ram_mb']), str(r.utilizedcapacity['total_ram_util%']) ))
print_table(rows)
print ""
print "PROJECT STATISTICS"
print ""
rows = []
rows.append(("Project Name",
             "Total CPU",
             "Running CPU",
             "Total RAM",
             "Running RAM",
             "Running VMs",
             "Utilized% CPU",
             "Utilized% RAM" ))
for project in r.projects.keys():
    rows.append((
        r.projects[project]['name'],
        str(r.projects[project]['alloc_cpu']),
        str(r.projects[project]['running_cpu']),
        str(r.projects[project]['alloc_ram_mb']),
        str(r.projects[project]['running_ram']),
        str(r.projects[project]['running_instances']),
        str(r.projects[project]['total_cpu%']),
        str(r.projects[project]['total_ram%']) ))
print_table(rows)




