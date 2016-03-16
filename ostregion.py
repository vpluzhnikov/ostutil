# -*- coding: utf-8 -*-
__author__ = 'vsevolodpluzhnikov'


from common import load_config, build_query
import logging
from novaclient import client as client_nova
from ceilometerclient import client as client_ceilometer
from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client as client_keystone


class region:

    def __init__(self, configfile):
        """
        Following class attributes initialized in __init__:
        nova - client for nova service
        keystone - client for keystone service
        ceilometer - client for ceilometer service
        hosts - all hosts for region
        servers - all servers in region
        """
        self.logger = logging.getLogger(__name__)
        self.config = load_config(configfile)
        if self.config:
            try:
                auth = v3.Password(username=self.config['username'],
                    password=self.config['password'],
                    project_name=self.config['tenant_name'],
                    auth_url=self.config['auth_url'],
                    user_domain_name=self.config['domain'],
                    project_domain_name=self.config['domain'],)
                self.session = session.Session(auth=auth, verify=self.config['cacert'])
                self.nova = client_nova.Client(2, session=self.session)
                self.keystone = client_keystone.Client(session=self.session)
                self.ceilometer = client_ceilometer.Client(2, session=self.session)
                self.hosts = self.nova.hosts.list()
                self.servers = self.nova.servers.list(search_opts = { 'all_tenants': 1 })
                self.projects = self._getprogects()
                self.flavors = self._getflavors()
                self.fullcapacity = self._get_full_capacity()
                self.alloccapacity = self._get_allocated_capacity()
                self.connected = True
            except:
                self.logger.error('Error for authentication with credentials from ' + configfile)
                self.connected = False


    def _getprogects(self):
        self.logger.info('Reading projects from region')
        projects = {}
        if self.keystone:
            for project in self.keystone.projects.list():
                projects.update( { unicode(project.id) : { u'name' : unicode(project.name)}})
        else:
            self.loggers.error('No active keystone connection')
            return None
        self.logger.info('Total '+str(len(projects))+' projects discovered')
        return projects

    def _getflavors(self):
        self.logger.info('Reading flavors from region')
        flavors = {}
        if self.nova:
            for flavor in self.nova.flavors.list():
                flavors.update({ flavor.id : {'name' : flavor.name,
                                              'ram' : flavor.ram,
                                              'vcpus' : flavor.vcpus}})
        else:
            self.logger.error('No active nova connection')
            return None
        return flavors

    def _get_full_capacity(self):
        self.logger.info('Get full capacity from region')
        cpu = 0
        ram = 0
        disk = 0
        if self.nova:
            for host in self.nova.hosts.list():
                if host.service == u'compute':
                    self.logger.info('Compute host ' + host.host_name + ' discovered.')
                    compute_host = self.nova.hosts.get(host.host_name)[0]._info
                    cpu += compute_host['resource']['cpu']
                    ram += compute_host['resource']['memory_mb']
                    disk += compute_host['resource']['disk_gb']
        else:
            self.logger.error('No active nova connection')
            return None
        return {u'cpu' : cpu,
                u'ram_mb' : ram,
                u'disk_gb' : disk}

    def _get_allocated_capacity(self):
        self.logger.info('Get allocated capacity for projects in region')
        cpu = 0
        ram = 0
        instances = 0
        if self.nova and self.keystone:
            for project in self.projects.keys():
                quota = self.nova.quotas.get(project)
                cpu += quota.cores
                ram += quota.ram
                instances += quota.instances
                self.projects[project].update({'alloc_cpu' : quota.cores,
                                               'alloc_ram_mb': quota.ram,
                                               'alloc_instances' : quota.instances})
            return {u'alloc_cpu' : cpu,
                    u'ram_mb' : ram,
                    u'alloc_instances' : instances,
                    }
        else:
            self.logger.error('No active keystone or nova connection')
            return None


    def get_running_capacity(self):
        cpu = 0
        ram = 0
        instances = 0
        for project in self.projects.keys():
            self.projects[project]['running_instances'] = 0
            self.projects[project]['running_cpu'] = 0
            self.projects[project]['running_ram'] = 0
        if self.nova and self.keystone:
            for server in self.servers:
                self.projects[server.tenant_id]['running_instances'] += 1
                self.projects[server.tenant_id]['running_cpu'] += self.flavors[server.flavor['id']]['vcpus']
                self.projects[server.tenant_id]['running_ram'] += self.flavors[server.flavor['id']]['ram']
                cpu += self.flavors[server.flavor['id']]['vcpus']
                ram += self.flavors[server.flavor['id']]['ram']
                instances += 1
            return {u'running_cpu' : cpu,
                    u'running_ram_mb' : ram,
                    u'running_instances' : instances,
                    }
        else:
            self.logger.error('No active keystone or nova connection')
            return None

    def get_utilization(self):
        total_cpu_util = 0
        total_ram_util = 0
        for project in self.projects.keys():
            self.projects[project]['utilized_instances'] = 0
            self.projects[project]['utilized_cpu%'] = 0
            self.projects[project]['utilized_ram%'] = 0
        if self.servers:
            for server in self.servers:
                try:
                    cpu_stat =  self.ceilometer.statistics.list('cpu_util', q=build_query(server.id, 'cpu_util'))
                    self.projects[server.tenant_id]['utilized_cpu%'] += cpu_stat[0].max
                except:
                    self.logger.error('Cannot get cpu statistics for server id = '+server.id)
                try:
                    mem_stat =  self.ceilometer.statistics.list('memory', q=build_query(server.id, 'memory'))
                    self.projects[server.tenant_id]['utilized_ram%'] += float(mem_stat[0].max) / \
                                                                        float(self.flavors[server.flavor['id']]['ram'])
                except:
                    self.logger.error('Cannot get memory statistics for server id = '+server.id)
        else:
            self.logger.error('No servers discovered')
        for project in self.projects.keys():
            if ((u'running_instances' in self.projects[project].keys())
                and ('utilized_instances' in self.projects[project].keys())
                and ('alloc_cpu' in self.projects[project].keys())):
                self.projects[project]['total_cpu%'] = ( float(self.projects[project]['utilized_cpu%']) /
                                                         float(self.projects[project]['utilized_instances']) ) * \
                                                       ( float(self.projects[project]['running_cpu']) /
                                                         float(self.projects[project]['alloc_cpu']))
                total_cpu_util += self.projects[project]['total_cpu%']
                self.projects[project]['total_ram%'] = ( float(self.projects[project]['utilized_ram%']) /
                                                         float(self.projects[project]['utilized_instances']) ) *\
                                                       ( float(self.projects[project]['running_cpu']) /
                                                         float(self.projects[project]['alloc_cpu']))
                total_cpu_util += self.projects[project]['utilized_ram%']
            else:
                self.logger.error('No running capacity or utilized capacity for project = '+project)
                self.projects[project]['total_cpu%'] = 0
                self.projects[project]['total_ram%'] = 0
        if len(self.projects.keys()) > 0:
            return {
                u'total_cpu_util%' : total_cpu_util,
                u'total_ram_util%' : total_ram_util,
            }
