# -*- coding: utf-8 -*-
__author__ = 'vsevolodpluzhnikov'


from common import load_config
import logging
from novaclient import client as client_nova
from ceilometerclient import client as client_ceilometer
from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client as client_keystone
from ConfigParser import ConfigParser


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
                self.projects = self.__getprogects__()
                self.flavors = self.__getflavors__()
                self.fullcapacity = self.__get_full_capacity__()
                self.alloccapacity = self.__get_allocated_capacity__()
            except:
                logger.error('Error for authentication with credentials from ' + configfile)
                self.connected = False


    def __getprogects__(self):
        self.logger('Reading projects from region')
        projects = {}
        if self.keystone:
            for project in self.keystone.projects.list():
                projects.update( { unicode(project.id) : { u'name' : unicode(project.name)}})
        else:
            logger.error('No active keystone connection')
            return None
        self.logger.info('Total '+str(len(projects))+' projects discovered')
        return projects

    def __getflavors__(self):
        self.logger('Readingflavors from region')
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

    def __get_full_capacity__(self):
        self.logger('Get full capacity from region')
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

    def __get_allocated_capacity__(self):
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
