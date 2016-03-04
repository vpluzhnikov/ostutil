# -*- coding: utf-8 -*-
from common import get_nova_connecton
import logging

logger = logging.getLogger(__name__)

def get_avaiable_hosts(nova):
    cpu_count = 0
    memory_count = 0
    disk_count = 0
    if nova:
        for host in nova.hosts.list():
            if host.service == u'compute':
                logger.info("Compute host " + host.host_name + " discovered.")
                compute_host = nova.hosts.get(host.host_name)[0]._info
#                print compute_host
                cpu_count += compute_host['resource']['cpu']
                memory_count += compute_host['resource']['memory_mb']
                disk_count += compute_host['resource']['disk_gb']
    else:
        return None
    return {'cpu' : cpu_count, 'memory_mb' : memory_count, 'disk_gb' : disk_count}

def get_projects(keystone):
    projects = {}
    if keystone:
        for project in keystone.projects.list():
            project.update({'name' : project._info['name'], 'id' : project._info['name']})
    else:
        return None
    return projects
