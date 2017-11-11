#!/usr/bin/env python
# -*- coding: utf-8 -*-
# source: https://stackoverflow.com/questions/29394535/convert-unicode-list-into-python-list
import json
import pprint
pp = pprint.PrettyPrinter(indent=4, width=80)

def str_to_json(a_str):
    filtered_json_data = {}
    json_data = json.loads(a_str)
    for i in json_data:
        if i['name'] == 'marvel-swarm-rules':
            filtered_json_data = i
            break
    return filtered_json_data


def do_firewall_uniq_add_inbound_rules(a_str, a_list_of_ips):
    a_json = str_to_json(a_str)

    for ip in a_list_of_ips:
        _ip = "{}/32".format(ip)
        inbound_schema = {
            "ports": "0-65535",
            "protocol": "tcp",
            "sources": {
                "addresses": [_ip]}}

        # inbound_schema['sources']['addresses'].append(_ip)

        a_json['inbound_rules'].append(inbound_schema)

        pp.pprint(a_json)

    return a_json

class FilterModule(object):
    ''' A filter to see if a sub string exists inside a list using regex. '''

    def filters(self):
        return {
            'do_firewall_uniq_add_inbound_rules': do_firewall_uniq_add_inbound_rules
        }
