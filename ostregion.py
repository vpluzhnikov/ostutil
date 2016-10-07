# -*- coding: utf-8 -*-
__author__ = 'vsevolodpluzhnikov'


from common import load_config, build_query
import logging
from novaclient import client as client_nova
from ceilometerclient import client as client_ceilometer
from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client as client_keystone
from glanceclient import client as client_glance


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
                self.glance = client_glance.Client(2, session=self.session)
                self.hosts = self.nova.hosts.list()
                self.servers = self.nova.servers.list(search_opts = { 'all_tenants': 1 })
                self.projects = self.getprojects()
                self.flavors = self.getflavors()
                self.connected = True
            except:
                self.logger.error('Error for authentication with credentials from ' + configfile)
                self.connected = False


    def getprojects(self):
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

    def getflavors(self):
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
