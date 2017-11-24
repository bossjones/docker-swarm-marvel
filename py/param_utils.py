"""Utility tools to render version paramaters that will but consumed by jinja templates"""

import re
import logging
import string
import collections

def convert_unicode_to_str(data, encoding='utf-8'):

    # ==============================================
    # http://stackoverflow.com/a/1254499/42171
    # ==============================================
    if isinstance(data, basestring):
        return data.encode(encoding) if isinstance(data, unicode) else \
            data
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_unicode_to_str, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_unicode_to_str, data))
    else:
        return data


def make_firewall_inbound_rule(address, protocol='tcp', ports='1-65535'):
    """
    Return (String) - Eg. protocol:tcp,ports:1-65535,address:192.168.1.42/32
    """
    return "protocol:{protocol},ports:{ports},address:{address}".format(address=address, protocol=protocol, ports=ports)

def make_slash_32_from_ip(a_var):
    """
    a_var (String) - eg. 192.168.99.104
    Return (String) - eg. 192.168.99.104/32
    """
    # print("BEFORE string: a_var = '{}' of type '{}'".format(a_var,type(a_var)))
    if isinstance(a_var, unicode):
        a_var = a_var.encode('utf-8')
    # print("AFTER string: a_var = '{}' of type '{}'".format(a_var,type(a_var)))
    if re.search(r".*(/32)", a_var):
        return a_var
    else:
        return "{}/32".format(a_var)

def get_default_outbound_rules():
    return {"outbound_rules":['protocol:icmp,address:0.0.0.0/0,address:::/0',
                              'protocol:tcp,ports:all,address:0.0.0.0/0',
                              'address:::/0,protocol:udp,ports:all,address:0.0.0.0/0,address:::/0']
           }

def return_tag_match(tag_partial, tag_list):
    """
    Given

    tag_list (list) - Eg all_tags= [ 'role:marvel-swarm-manager',
                                     'role:marvel-swarm-agent',
                                     'name:stark-tower',
                                     'name:necropolis',
                                     'name:baxter',
                                     'name:latveria',
                                     'region:nyc3',
                                     'cluster:swarm-marvel',
                                     'firewall:marvel-swarm-rules',
                                     'server:stark-tower',
                                     'server:necropolis',
                                     'server:baxter',
                                     'server:latveria' ]

    tag_partial (String) - EG nyc3
    """

    # NOTE: Example output
    # In[30]: match_list = return_tag_match('baxter', all_tags)

    # In[31]: match_list
    # Out[31]: ['name:baxter', 'server:baxter']

    temp_tag_list=[]
    for i in tag_list:
        _regex = r".*{}.*".format(tag_partial)
        tag_match = re.match(_regex, i)
        if tag_match:
            temp_tag_list.append(tag_match.group(0))
    return temp_tag_list
