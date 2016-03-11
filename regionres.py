# -*- coding: utf-8 -*-
from common import get_nova_connecton
import logging

logger = logging.getLogger(__name__)

def get_project_max(ceilometer, project):
    query = [dict(field='project_id', op='eq', value=project), dict(field='meter',op='eq',value='cpu_util')]
    return ceilometer.statistics.list('cpu_util', q=query, period=1000)

def get_projects_utilization(keystone, ceilometer):
    cpu_count = 0
    memory_count = 0
    disk_count = 0
    projects = {}
    if keystone and ceilometer:
        for project in get_projects(keystone):
            projects.update(get_project_max(ceilometer, unicode(project['id'])))
    else:
        logger.error('No active keystone or ceilometer connection')
        return None
    return projects

def get_full_capacity(nova):
    cpu_count = 0
    memory_count = 0
    disk_count = 0
    if nova:
        for host in nova.hosts.list():
            if host.service == u'compute':
                logger.info('Compute host ' + host.host_name + ' discovered.')
                compute_host = nova.hosts.get(host.host_name)[0]._info
                cpu_count += compute_host['resource']['cpu']
                memory_count += compute_host['resource']['memory_mb']
                disk_count += compute_host['resource']['disk_gb']
    else:
        logger.error('No active nova connection')
        return None
    return {u'cpu' : cpu_count, u'memory_mb' : memory_count, u'disk_gb' : disk_count}

def get_allocated_capacity(nova, keystone):
    projects = []
    total_cpu = 0
    total_ram = 0
    total_instances = 0
    if nova and keystone:
        for project in get_projects(keystone):
            quota = nova.quotas.get(project['id'])
            total_cpu += quota.cores
            total_ram += quota.ram
            total_instances += quota.instances
            project.update({'cpu' : quota.cores, 'ram': quota.ram, 'instances' : quota.instances})
            projects.append(project)
        return {u'cpu' : total_cpu,
                u'memory_mb' : total_ram,
                u'instances' : total_instances,
                u'project_list' : projects }
    else:
        logger.error('No active keystone or nova connection')
        return None

def get_mapped_resources(nova, keystone):
    search_opts = {
        'all_tenants': 1,
        }
    projects = {}
    for project in get_projects(keystone):
        projects.update ({ project['id'] : {'name' : project['name']} })
    flavors = get_flavors(nova)
    total_cpu = 0
    total_ram = 0
    total_instances = 0
    if nova and keystone:
        for server in nova.servers.list(search_opts):
            if 'count' in projects[server.tenant_id].keys():
                projects[server.tenant_id]['instances'] += 1
            else:
                projects[server.tenant_id]['count'] = 1
            if 'cpu' in projects[server.tenant_id].keys():
                projects[server.tenant_id]['cpu'] += flavors[server.flavor['id']]['vcpus']
            else:
                projects[server.tenant_id]['cpu'] = flavors[server.flavor['id']]['vcpus']
            if 'ram' in projects[server.tenant_id].keys():
                projects[server.tenant_id]['ram'] += flavors[server.flavor['id']]['ram']
            else:
                projects[server.tenant_id]['ram'] = flavors[server.flavor['id']]['ram']
            total_cpu += flavors[server.flavor['id']]['vcpus']
            total_ram += flavors[server.flavor['id']]['ram']
            total_instances += 1
        return {u'cpu' : total_cpu,
                u'memory_mb' : total_ram,
                u'instances' : total_instances,
                u'project_list' : projects }
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
    logger.info('Total '+str(len(projects))+' projects discovered')
    return projects

def get_flavors(nova):
    flavors = {}
    if nova:
        for flavor in nova.flavors.list():
            flavors.update({ flavor.id : {'name' : flavor.name,
                                          'ram' : flavor.ram,
                                          'vcpus' : flavor.vcpus}})
    else:
        logger.error('No active nova connection')
        return None
    return flavors
