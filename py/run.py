#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import argparse
from config_file import Object as ConfigObject
import logging
import os
import pprint
import sys

from application import Application
import files
import log
import updaters
pp = pprint.PrettyPrinter(indent=4, width=80)

# Example from opts
# python py/run.py generate --config examples/build-config-example.yml --jinja-file py/Dockerfile.j2 --product boss --dry-run
# Namespace(cmd1='generate',
#           config='examples/build-config-example.yml',
#           dry_run=True,
#           jinja_file='py/Dockerfile.j2',
#           product='boss',
#           verbose=False,
#           workspace='/Users/user/dev/bossjones/docker-swarm-marvel')


class Runner(object):

    def __init__(self):
        """Main execution path """

        # Read settings, environment variables, and CLI arguments
        self.read_cli_args()
        self.load_app()

        if self.args.dry_run:
            print "Dry run mode, not writing anything to disk"
            pp.pprint(self.app.config.__dict__)
            sys.exit(0)

        self.app.template_command_to_use(self.args)

    def load_app(self):
        """Initalize app settings"""
        self.app = Application(self.args)
        self.app.bootstrap()

    def read_cli_args(self):
        """ Command line argument processing """
        # https://stackoverflow.com/questions/37930737/how-to-write-argparse-in-python-using-abstract-base-class
        parser = argparse.ArgumentParser(description='Generate Various files from Jinja2 templates')
        sp1 = parser.add_subparsers(dest='cmd1')
        ps3 = sp1.add_parser('generate')
        ps3.add_argument("-d",
                         "--dry-run",
                         action="store_true",
                         help="Whether to autoupdate parameters or not")
        ps3.add_argument("-w",
                         "--workspace",
                         dest="workspace",
                         type=str,
                         default=os.getcwd(),
                         help="Where to search for configs. Defaults to cwd")
        ps3.add_argument("-j",
                         "--jinja-file",
                         help=".j2 file to render")
        ps3.add_argument("-p",
                         "--product",
                         help="product name eg 'boss'")
        ps3.add_argument("-c",
                         "--config",
                         dest="config",
                         help="Configuration location.")
        ps3.add_argument("-v",
                         "--verbose",
                         action="store_true",
                         help="Verbose output.")

        self.args = parser.parse_args()
        print self.args

def main(argv=None):
    Runner()


if __name__ == "__main__":
    sys.path.insert(0, ".")
    main()
