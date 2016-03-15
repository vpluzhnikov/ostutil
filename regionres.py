# -*- coding: utf-8 -*-
from common import get_nova_connecton
import logging

logger = logging.getLogger(__name__)

def get_resource_max(ceilometer, resource):
    query = [dict(field='resource_id', op='eq', value=resource), dict(field='meter',op='eq',value='cpu_util')]
    return ceilometer.statistics.list('cpu_util', q=query)

def get_projects_utilization(nova, keystone, ceilometer):
    projects = {}
    search_opts = {
        'all_tenants': 1,
        }
    for project in get_projects(keystone):
        projects.update ({ project['id'] : {'name' : project['name']} })
    if nova and keystone and ceilometer:
        for server in nova.servers.list(search_opts=search_opts):
            print get_resource_max(ceilometer, server.id)
        return None
    else:
        logger.error('No active keystone or nova or ceilometer connection')
        return None

#def get_projects_utilization(keystone, ceilometer):
#    cpu_count = 0
#    memory_count = 0
#    disk_count = 0
#    projects = {}
#    if keystone and ceilometer:
#        for project in get_projects(keystone):
#            projects.update(get_project_max(ceilometer, unicode(project['id'])))
#    else:
#        logger.error('No active keystone or ceilometer connection')
#        return None
#    return projects
