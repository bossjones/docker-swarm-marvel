# pylint: disable=W0403
import os
import logging
import files
import config
from config import Config as ConfigObject
from config import NullConfig as NullObject
import pprint
pp = pprint.PrettyPrinter(indent=4, width=80)

class Object(ConfigObject):
    def __init__(self, path):
        data = files.load_yaml_file(path)
        super(Object, self).__init__(data)
        self.fqpath = os.path.abspath(path)
        self.location = os.path.dirname(self.fqpath)
        # TODO: Change this default to be a fixure at another point in time
        self.configs = self._get_key_or_default('configs', {})
        self.ref_server_names = None

    def _get_key_or_default(self, key, default):
        stored = self.__getattr__(key)()
        return default if stored is None else stored

    def get_ansible_user(self):
        return None if not "ansible_user" in self.configs else self.configs["ansible_user"]

    def get_service_ports(self):
        return [] if not "service_ports" in self.configs else self.configs["service_ports"]

    def get_whitelist_ip_cidrs(self):
        return {} if not "whitelist_ip_cidrs" in self.configs else self.configs["whitelist_ip_cidrs"]

    def get_datacenter_type(self):
        # TODO: Change this default to be 'local' at another point in time
        return 'digitalocean' if not "datacenter_type" in self.configs else self.configs["datacenter_type"]

    def get_all_tags(self):
        # TODO: Change this default to be 'local' at another point in time
        return [] if not "all_tags" in self.configs else self.configs["all_tags"]

    def get_firewall_tag_name(self):
        # TODO: Change this default to be 'local' at another point in time
        return None if not "firewall_tag_name" in self.configs else self.configs["firewall_tag_name"]

    def get_servers_to_find(self):
        # TODO: Change this default to be 'local' at another point in time
        return [] if not "servers_to_find" in self.configs else self.configs["servers_to_find"]

    def get_server_names_list(self):
        """ Return Example ['avengers-tower', 'latveria', 'baxter'] """
        self.ref_server_names = [s_names['name'] for s_names in self.get_servers_to_find()]
        return self.ref_server_names
