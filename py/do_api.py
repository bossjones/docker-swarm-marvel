#!/usr/bin/env python

"""
Borrowed from DigitalOcean external inventory script
======================================
"""

# (c) 2013, Evan Wies <evan@neomantra.net>
# (c) 2017, Ansible Project
# (c) 2017, Abhijeet Kasurde <akasurde@redhat.com>
#
# Inspired by the EC2 inventory plugin:
# https://github.com/ansible/ansible/blob/devel/contrib/inventory/ec2.py
#
# This file is part of Ansible,
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

######################################################################

import argparse
import ast
import os
import re
import requests
import sys
from time import time

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

try:
    import json
except ImportError:
    import simplejson as json


class DoManager:
    def __init__(self, api_token):
        self.api_token = api_token
        self.api_endpoint = 'https://api.digitalocean.com/v2'
        self.headers = {'Authorization': 'Bearer {0}'.format(self.api_token),
                        'Content-type': 'application/json'}
        self.timeout = 60

    def _url_builder(self, path):
        if path[0] == '/':
            path = path[1:]
        return '%s/%s' % (self.api_endpoint, path)

    def send(self, url, method='GET', data=None):
        url = self._url_builder(url)
        data = json.dumps(data)
        try:
            if method == 'GET':
                resp = requests.get(url, data=data, headers=self.headers, timeout=self.timeout)
                json_resp = resp.json()
        except ValueError as e:
            sys.exit("Unable to parse result from %s: %s" % (url, e))
        return json_resp

    def all_active_droplets(self):
        resp = self.send('droplets/')
        return resp['droplets']

    def all_regions(self):
        resp = self.send('regions/')
        return resp['regions']

    def all_images(self, filter_name='global'):
        params = {'filter': filter_name}
        resp = self.send('images/', data=params)
        return resp['images']

    def sizes(self):
        resp = self.send('sizes/')
        return resp['sizes']

    def all_ssh_keys(self):
        resp = self.send('account/keys')
        return resp['ssh_keys']

    def all_domains(self):
        resp = self.send('domains/')
        return resp['domains']

    def show_droplet(self, droplet_id):
        resp = self.send('droplets/%s' % droplet_id)
        return resp['droplet']

    def all_tags(self):
        resp = self.send('tags/')
        return resp['tags']


class DigitalOceanInventory(object):

    ###########################################################################
    # Main execution path
    ###########################################################################

    def __init__(self):
        """Main execution path """

        # DigitalOceanInventory data
        self.data = {}  # All DigitalOcean data
        self.inventory = {}  # Ansible Inventory

        self.use_private_network = False
        self.group_variables = {}

        # Read settings, environment variables, and CLI arguments
        self.read_settings()
        self.read_environment()
        # self.read_cli_args()

        # Verify credentials were set
        if not hasattr(self, 'api_token'):
            msg = 'Could not find values for DigitalOcean api_token. They must be specified via either ini file, ' \
                  'command line argument (--api-token), or environment variables (DO_API_TOKEN)\n'
            sys.stderr.write(msg)
            sys.exit(-1)

        self.manager = DoManager(self.api_token)

        self.load_from_digital_ocean('droplets')
        self.build_inventory()
        json_data = self.inventory

    ###########################################################################
    # Script configuration
    ###########################################################################

    def read_settings(self):
        """ Reads the settings from the digital_ocean.ini file """
        config = ConfigParser.SafeConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'digital_ocean.ini')
        config.read(config_path)

        # Credentials
        if config.has_option('digital_ocean', 'api_token'):
            self.api_token = config.get('digital_ocean', 'api_token')

        # Cache related
        if config.has_option('digital_ocean', 'cache_path'):
            self.cache_path = config.get('digital_ocean', 'cache_path')
        if config.has_option('digital_ocean', 'cache_max_age'):
            self.cache_max_age = config.getint('digital_ocean', 'cache_max_age')

        # Private IP Address
        if config.has_option('digital_ocean', 'use_private_network'):
            self.use_private_network = config.getboolean('digital_ocean', 'use_private_network')

        # Group variables
        if config.has_option('digital_ocean', 'group_variables'):
            self.group_variables = ast.literal_eval(config.get('digital_ocean', 'group_variables'))

    def read_environment(self):
        """ Reads the settings from environment variables """
        # Setup credentials
        if os.getenv("DO_API_TOKEN"):
            self.api_token = os.getenv("DO_API_TOKEN")
        if os.getenv("DO_API_KEY"):
            self.api_token = os.getenv("DO_API_KEY")

    ###########################################################################
    # Data Management
    ###########################################################################

    def load_from_digital_ocean(self, resource=None):
        """Get JSON from DigitalOcean API """

        if resource == 'droplets' or resource is None:
            self.data['droplets'] = self.manager.all_active_droplets()
        if resource == 'regions' or resource is None:
            self.data['regions'] = self.manager.all_regions()
            self.cache_refreshed = True
        if resource == 'images' or resource is None:
            self.data['images'] = self.manager.all_images()
            self.cache_refreshed = True
        if resource == 'sizes' or resource is None:
            self.data['sizes'] = self.manager.sizes()
            self.cache_refreshed = True
        if resource == 'ssh_keys' or resource is None:
            self.data['ssh_keys'] = self.manager.all_ssh_keys()
            self.cache_refreshed = True
        if resource == 'domains' or resource is None:
            self.data['domains'] = self.manager.all_domains()
            self.cache_refreshed = True
        if resource == 'tags' or resource is None:
            self.data['tags'] = self.manager.all_tags()
            self.cache_refreshed = True

    def build_inventory(self):
        """ Build Ansible inventory of droplets """
        self.inventory = {
            'all': {
                'hosts': [],
                'vars': self.group_variables
            },
            '_meta': {'hostvars': {}}
        }

        # add all droplets by id and name
        for droplet in self.data['droplets']:
            for net in droplet['networks']['v4']:
                if net['type'] == 'public':
                    dest = net['ip_address']
                else:
                    continue

            self.inventory['all']['hosts'].append(dest)

            self.inventory[droplet['id']] = [dest]
            self.inventory[droplet['name']] = [dest]

            # groups that are always present
            for group in ('region_' + droplet['region']['slug'],
                          'image_' + str(droplet['image']['id']),
                          'size_' + droplet['size']['slug'],
                          'distro_' + DigitalOceanInventory.to_safe(droplet['image']['distribution']),
                          'status_' + droplet['status']):
                if group not in self.inventory:
                    self.inventory[group] = {'hosts': [], 'vars': {}}
                self.inventory[group]['hosts'].append(dest)

            # groups that are not always present
            for group in (droplet['image']['slug'],
                          droplet['image']['name']):
                if group:
                    image = 'image_' + DigitalOceanInventory.to_safe(group)
                    if image not in self.inventory:
                        self.inventory[image] = {'hosts': [], 'vars': {}}
                    self.inventory[image]['hosts'].append(dest)

            if droplet['tags']:
                for tag in droplet['tags']:
                    if tag not in self.inventory:
                        self.inventory[tag] = {'hosts': [], 'vars': {}}
                    self.inventory[tag]['hosts'].append(dest)

            # hostvars
            info = self.do_namespace(droplet)
            self.inventory['_meta']['hostvars'][dest] = info

    ###########################################################################
    # Cache Management
    ###########################################################################

    ###########################################################################
    # Utilities
    ###########################################################################
    @staticmethod
    def to_safe(word):
        """ Converts 'bad' characters in a string to underscores so they can be used as Ansible groups """
        return re.sub("[^A-Za-z0-9\-.]", "_", word)

    @staticmethod
    def do_namespace(data):
        """ Returns a copy of the dictionary with all the keys put in a 'do_' namespace """
        info = {}
        for k, v in data.items():
            info['do_' + k] = v
        return info
