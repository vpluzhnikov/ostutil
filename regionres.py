# -*- coding: utf-8 -*-
from common import get_nova_connecton
import logging

logger = logging.getLogger(__name__)

def get_full_capacity(nova):
    cpu_count = 0
    memory_count = 0
    disk_count = 0
    if nova:
        for host in nova.hosts.list():
            if host.service == u'compute':
                logger.info('Compute host ' + host.host_name + ' discovered.')
                compute_host = nova.hosts.get(host.host_name)[0]._info
#                print compute_host
                cpu_count += compute_host['resource']['cpu']
                memory_count += compute_host['resource']['memory_mb']
                disk_count += compute_host['resource']['disk_gb']
    else:
        logger.error('No active nova connection')
        return None
    return {u'cpu' : cpu_count, u'memory_mb' : memory_count, u'disk_gb' : disk_count}

def get_allocated_capacity(nova, keystone):
    if nova and keystone:
        for project in get_projects(keystone):
            quota = nova.client.get(project['id'])
            print quota.cores
            print quota.ram
            print quota.instances
    else:
        logger.error('No active keystone or nova connection')
        return None


def get_projects(keystone):
    projects = []
    if keystone:
        for project in keystone.projects.list():
            projects.append({u'name' : unicode(project.name), u'id' : unicode(project.id)})
    else:
        logger.error('No active keystone connection')
        return None
    logger.info('Total '+len(projects)+' projects discovered')
    return projects

