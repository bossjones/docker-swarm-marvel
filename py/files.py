# pylint: disable=W0403
import yaml
import json
import os
import logging
from collections import OrderedDict

def load_json_file(file_path):
    with open(file_path, "r") as file_handle:
        content = file_handle.read().replace('\n', '')
    return json.loads(content, object_pairs_hook=OrderedDict)


def write_json_file(file_path, data):
    contents = json.dumps(data, indent=4, separators=(',', ': '))
    write_file(file_path, contents)


def write_file(file_path, contents):
    with open(file_path, "w") as file_handle:
        file_handle.write(contents)


def is_file_type(path, expected_ext):
    (base, ext) = os.path.splitext(path)
    return ext == (".%s" % expected_ext)


def file_as_str(path):
    return open(path, 'r').read()

def mkdir_if_dne(target):
    if not os.path.isdir(target):
        os.makedirs(target)

def load_yaml_file(file_path):
    with open(file_path, 'r') as stream:
        try:
            build_config = yaml.load(stream)
        except yaml.YAMLError as exc:
            logging.error("bad yaml")
            print exc
            sys.exit(1)
    return build_config
