# -*- coding: utf-8 -*-
from ostregion import region
import sys

if len(sys.argv) != 2:
    configfile = None
else:
    configfile = sys.argv[1]

r = region('ost.ini')
print r._getflavors()
