# NOTE: This is from from chamberlain
import yaml
from copy import copy
import jinja2
import os
import subprocess
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4, width=80)

# ORIG
################################################################################################
# source: https://github.com/alexey-medvedchikov/ansible-pgha-example/blob/749c661f481ba8d178ea2f5434ce047eb9c911c7/scripts/ansible-bastion.py
################################################################################################
J2_SSH_CONFIG = """
Host {{ bastion_host }}
  User                   {{ bastion_user }}
  HostName               {{ bastion_host }}
  ProxyCommand           none
  BatchMode              yes
  PasswordAuthentication no
  ControlMaster          auto
  ControlPath            ~/.ssh/mux-%r@%h:%p
  ControlPersist         15m
Host *
  ServerAliveInterval 60
  TCPKeepAlive        yes
  ProxyCommand        ssh -q -A {{ bastion_user }}@{{ bastion_host }} nc %h %p
  ControlMaster       auto
  ControlPath         ~/.ssh/mux-%r@%h:%p
  ControlPersist      8h
  User                ansible
  StrictHostKeyChecking no
  Compression         yes
  CompressionLevel    9
"""
J2_SSH_CONFIG_PATH = 'bastion.ssh_config'

J2_ANSIBLE_CFG = """
[ssh_connection]
ssh_args = -o ControlPersist=15m -F {{ ssh_config }} -q
scp_if_ssh = True
control_path = ~/.ssh/mux-%%r@%%h:%%p
"""
J2_ANSIBLE_CFG_PATH = 'bastion.ansible.cfg'
################################################################################################

# source: https://github.com/arjenmeek/ansible-common/blob/master/roles/local_sshconf/templates/ssh_config.j2
# NOTE: Use filtered_droplets to render this
SSH_CONFIG_TEMPLATE = """
{% for host_name,host_value in droplets.items() %}
{% set droplet_name = host_value['name'] %}
{% set droplet_ip_address = host_value['ip_address'] %}
Host {{ droplet_name }}
  HostName {{ droplet_ip_address }}
  Port 22
  User {{ user_name }}
  IdentityFile ~/.ssh/id_rsa_digitalocean
  ServerAliveInterval 240
  ServerAliveCountMax 2
  PasswordAuthentication no
  IdentitiesOnly yes
  LogLevel FATAL
{% endfor %}
"""

ANSIBLE_CFG_TEMPLATE = """
[defaults]
transport=ssh
inventory={{ workspace_dir }}/hosts
system_errors = False
host_key_checking = False
ask_sudo_pass = False
retry_files_enabled = False
library = {{ workspace_dir }}/library
sudo_user = root
forks=20
# This is to set the default language to communicate between the module and the system. By default, the value is value LANG on the controller or, if unset, en_US.UTF-8 (it used to be C in previous versions):
# module_lang    = C
module_lang    = en_US.UTF-8

[ssh_connection]
# DC/OS ssh
# ssh_args= -o ControlMaster=auto -o ControlPersist=60s -o ProxyCommand="/usr/bin/nc -x localhost:1230 %h %p"
ssh_args= -o ControlMaster=auto -o ControlPersist=60s -F {{ workspace_dir }}/ssh_config
control_path = ~/.ssh/{{ product }}-%%r@%%h:%%p

[persistent_connection]
# Configures the persistent connection timeout value in seconds.  This value is
# how long the persistent connection will remain idle before it is destroyed.
# If the connection doesn't receive a request before the timeout value
# expires, the connection is shutdown. The default value is 30 seconds.
connect_timeout = 60
"""

DIGITAL_OCEAN_TEMPLATE = """
# Ansible DigitalOcean external inventory script settings
#

[digital_ocean]

# The module needs your DigitalOcean API Token.
# It may also be specified on the command line via --api-token
# or via the environment variables DO_API_TOKEN or DO_API_KEY
#
#api_token = 123456abcdefg


# API calls to DigitalOcean may be slow. For this reason, we cache the results
# of an API call. Set this to the path you want cache files to be written to.
# One file will be written to this directory:
#   - ansible-digital_ocean.cache
#
cache_path = {{ do_cache_path }}


# The number of seconds a cache file is considered valid. After this many
# seconds, a new API call will be made, and the cache file will be updated.
#
cache_max_age = 300

# Use the private network IP address instead of the public when available.
#
use_private_network = False

# Pass variables to every group, e.g.:
#
#   group_variables = { 'ansible_user': 'root' }
#
group_variables = {}
"""

SERVERS_INVENTORY_TEMPLATE = """
{% for host_name,host_value in droplets.items() %}
{% set droplet_name = host_value['name'] %}
{% set droplet_ip_address = host_value['ip_address'] %}
[{{ droplet_name }}]
{{ droplet_ip_address }}

{% endfor %}

[all:vars]
ansible_python_interpreter="/usr/bin/{{ python_bin }}"
"""

LOCAL_HOSTS_TEMPLATE = """
[digitalocean]
localhost ansible_connection=local

[groupA]
localhost
"""

def render_file(content, filepath, context):
    """Render Jinja2 template from string to temporary file. Return new file
    path.
    :param content: Jinja2 template string
    :param filepath: path to store file
    :param context: context for template
    :type content: str
    :type filepath: str
    :type context: mapping
    :rtype: None
    """

    assert content != None
    assert filepath != None
    assert context != None

    template = jinja2.Template(content)
    with open(filepath, 'w') as fp:
        fp.write(template.render(context))

def show_rendered_file(filepath):
    try:
        with open(filepath, 'r') as fp:
            rendered_file = fp.read()
    except IOError:
        # TODO: Throw this exception, don't pass
        pass

    print "RENDERED FILE: {}".format(filepath)
    pp.pprint(rendered_file)

def generate_project(params, jobs):
    project = copy(params)
    project["jobs"] = jobs
    return yaml.safe_dump([{"project": project}],
                          encoding='utf-8',
                          allow_unicode=True)


def template_name(repo):
    return "project-%s.yml" % repo.replace("/", "_")
