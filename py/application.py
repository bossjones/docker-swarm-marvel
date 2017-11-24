# pylint: disable=W0403
# NOTE: This is a main container of application logic

from collections import OrderedDict
import config
from config import Config
import logging
import os
import pprint
import shutil
import stat

from config_file import Object as ConfigFileObject
from dynamic_config import DigitalOceanDynamicConfig
from files import is_file_type, load_yaml_file, mkdir_if_dne
from param_utils import get_default_outbound_rules, make_firewall_inbound_rule, make_slash_32_from_ip, return_tag_match
from updaters import j2_to_file
pp = pprint.PrettyPrinter(indent=4, width=80)

from templates import SSH_CONFIG_TEMPLATE, ANSIBLE_CFG_TEMPLATE, DIGITAL_OCEAN_TEMPLATE, SERVERS_INVENTORY_TEMPLATE, LOCAL_HOSTS_TEMPLATE, render_file, show_rendered_file

# Example from opts
# python py/run.py generate --config examples/build-config-example.yml --jinja-file py/Dockerfile.j2 --product boss --dry-run
# Namespace(cmd1='generate',
#           config='examples/build-config-example.yml',
#           dry_run=True,
#           jinja_file='py/Dockerfile.j2',
#           product='boss',
#           verbose=False,
#           workspace='/Users/user/dev/bossjones/docker-swarm-marvel')

class Application(object):

    def __init__(self, opts):
        self.config = Config({})
        self.dynamic_config = DigitalOceanDynamicConfig()
        self.folder_name = self.set_folder_name(opts)
        self.load_config(opts.config)
        self.jinja_file = opts.jinja_file
        self.rendered_file_name = j2_to_file(opts.jinja_file)
        self.lookup_servers = self.config.get_server_names_list()
        self.filtered_droplets = self.dynamic_config.filter_droplets(self.lookup_servers)

        self.cmd_mapping = {
            "Dockerfile": self.render_dockerfile,
            "ansible.cfg": self.render_ansible_cfg,
            "ssh_config": self.render_ssh_config,
            "digital_ocean.ini": self.render_digital_ocean_ini,
            "servers": self.render_dynamic_inventory,
            "hosts": self.render_ansible_hosts_file,
            "all_templates": self.render_all
        }

    def load_config(self, cfg_file):
        self.config = ConfigFileObject(cfg_file)

    def set_folder_name(self, opts):
        folder_name = "{}/{}-inventory".format(opts.workspace, opts.product)
        if not os.path.exists(folder_name):
            mkdir_if_dne(folder_name)
        return folder_name

    def bootstrap(self):
        """Wrapper function to call all required bootstrap commands to render merged config object"""
        self.merge_ip_address_list()
        self.create_firewall_rules()
        self.populate_droplet_tags()

    def create_firewall_rules(self):
        """
        Generate inbound_rules and outbound_rules for each droplet.

        outbound_rules: is using a fixture

        inbound_rules: dynamically creates a list of firewall descriptions based
        on ip address in whitelist + existing running server ips from dynamic config
        """
        # dynamically create inbound rule list ( standard across all servers )
        _inbound_rules = []
        for i in self.config.configs['whitelist_ip_cidrs']['ip_cidrs']:
            _ip = make_slash_32_from_ip(i)
            _firewall_rule = make_firewall_inbound_rule(_ip)
            _inbound_rules.append(_firewall_rule)

        # Override dictonary keys
        for d in self.filtered_droplets.keys():
            self.filtered_droplets[d]['inbound_rules'] = _inbound_rules
            self.filtered_droplets[d]['outbound_rules'] = get_default_outbound_rules()

    def populate_droplet_tags(self):
        """
        For each droplet, assign proper droplet tags to it.
        EG. filtered_droplets['latveria']['tags'] = ['cluster:swarm-marvel', 'name:latveria', 'server:latveria']
        """
        for d in self.filtered_droplets.keys():
            # EG. if name=avengers-tower and tag name:stark-tower exists

            # NOTE: Get matching tag values
            matched_tags = return_tag_match(self.filtered_droplets[d]['name'], self.config.configs['all_tags'])

            if matched_tags:
                self.filtered_droplets[d]['tags'].extend(matched_tags)

            cluster_tags = return_tag_match('cluster', self.config.configs['all_tags'])

            if cluster_tags:
                self.filtered_droplets[d]['tags'].extend(cluster_tags)

    def merge_ip_address_list(self):
        """Merge dynamically found ip addresses into known whitelist ip array."""
        for k,v in self.filtered_droplets.iteritems():
            _ip = make_slash_32_from_ip(v['ip_address'].encode('utf-8')) if isinstance(v['ip_address'], unicode) else \
            make_slash_32_from_ip(v['ip_address'])
            self.config.configs['whitelist_ip_cidrs']['ip_cidrs'].append(_ip)

        # NOTE: Make sure values are sorted/unique list(set[<some_list>]) gives you unique items
        tmp_whitelist_ip_cidrs = list(set(self.config.configs['whitelist_ip_cidrs']['ip_cidrs']))

        # Overwrite list with sorted/unique one
        self.config.configs['whitelist_ip_cidrs']['ip_cidrs'] = tmp_whitelist_ip_cidrs

    def render_ansible_cfg(self, opts):
        # FIXME: Throw error if required keys aren't set in dict below
        ansible_cfg_file = "{}/ansible.cfg".format(self.folder_name)
        render_file(ANSIBLE_CFG_TEMPLATE, ansible_cfg_file, {'workspace_dir': self.folder_name, 'product': opts.product})

    def render_ssh_config(self, opts):
        # FIXME: Throw error if required keys aren't set in dict below
        ssh_config_file = "{}/ssh_config".format(self.folder_name)
        render_file(SSH_CONFIG_TEMPLATE, ssh_config_file, {'droplets': self.filtered_droplets, 'user_name': self.config.configs['ansible_user']})

    def render_digital_ocean_ini(self, opts):
        # FIXME: Throw error if required keys aren't set in dict below
        digital_ocean_ini = "{}/digital_ocean.ini".format(self.folder_name)
        render_file(DIGITAL_OCEAN_TEMPLATE, digital_ocean_ini, {'do_cache_path': '/tmp'})

    def render_dynamic_inventory(self, opts):
        # FIXME: Throw error if required keys aren't set in dict below
        servers_dyn_inventory = "{}/servers".format(self.folder_name)
        render_file(SERVERS_INVENTORY_TEMPLATE, servers_dyn_inventory, {'droplets': self.filtered_droplets, 'python_bin': 'python3'})

    def render_dockerfile(self, opts):
        print "[render_dockerfile]: one day i'll implement this"
        print "opts: {}".format(opts)
        pass

    def render_ansible_hosts_file(self, opts):
        # FIXME: Throw error if required keys aren't set in dict below
        ansible_hosts_file = "{}/hosts".format(self.folder_name)
        render_file(LOCAL_HOSTS_TEMPLATE, ansible_hosts_file, {})

    def render_all(self, opts):
        self.render_ansible_cfg(opts)
        self.render_ssh_config(opts)
        self.render_digital_ocean_ini(opts)
        self.render_dynamic_inventory(opts)
        self.render_ansible_hosts_file(opts)
        self.clone_digital_ocean_py(opts)

    def clone_digital_ocean_py(self, opts):
        do_py_file = os.path.join(self.folder_name,'digital_ocean.py')
        shutil.copy2(os.path.join(os.path.dirname(__file__),'digital_ocean.py'),do_py_file)
        os.chmod(do_py_file, stat.S_IRUSR | stat.S_IXUSR|stat.S_IWUSR)

    def template_command_to_use(self, opts):
        # fingure out what type of render command to run
        for c in self.cmd_mapping.iteritems():
            if c[0] in os.path.basename(opts.jinja_file):
                print "Returning: {}".format(c[1])
                return c[1](opts)

        print "Sorry, c[0] did not match filename os.path.basename(opts.jinja_file) skipping..."
