# pylint: disable=W0403
import os
import logging
import files
import config
from config import Config as ConfigObject
from config import NullConfig as NullObject
import pprint
import do_api

pp = pprint.PrettyPrinter(indent=4, width=80)

class DigitalOceanDynamicConfig(ConfigObject):
    def __init__(self, path=None):
        if path:
            data = files.load_yaml_file(path)
        else:
            data = do_api.DigitalOceanInventory().data
        super(DigitalOceanDynamicConfig, self).__init__(data)

        # TODO: Change this default to be a fixure at another point in time
        self.all_droplets = self._get_key_or_default('droplets', {})
        self.ref_droplet_objs = {}

    def _get_key_or_default(self, key, default):
        stored = self.__getattr__(key)()
        return default if stored is None else stored

    def filter_droplets(self, list_to_find):
        """
        list_to_find (list of str) - Eg. ['latveria', 'baxter', 'avengers-tower']
        """
        for _droplet in self.all_droplets:
            if _droplet['name'] in list_to_find:
                tmp_ip_address = None
                for _ip in _droplet['networks']['v4']:
                    if _ip['type'] == 'public':
                        tmp_ip_address = _ip['ip_address']
                droplet_entry = {
                    'name': _droplet['name'],
                    'ip_address': tmp_ip_address,
                    'memory': _droplet['memory'],
                    'disk': _droplet['disk'],
                    'id': _droplet['id'],
                    'tags': _droplet['tags'],
                    'vcpus': _droplet['vcpus']
                    }
                self.ref_droplet_objs[_droplet['name']] = droplet_entry
        return self.ref_droplet_objs
