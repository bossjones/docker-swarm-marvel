# -*- coding: utf-8 -*-
import sys
import signal
import logging
import os

# source: https://stackoverflow.com/questions/21961693/how-to-print-all-variables-values-when-debugging-python-with-pdb-without-specif


def debug_nice(locals_dict, keys=[]):
    globals()['types'] = `__import__`('types')
    exclude_keys = ['copyright', 'credits', 'False',
                    'True', 'None', 'Ellipsis', 'quit']
    exclude_valuetypes = [types.BuiltinFunctionType,
                          types.BuiltinMethodType,
                          types.ModuleType,
                          types.TypeType,
                          types.FunctionType]
    return {k: v for k, v in locals_dict.iteritems() if not
            (k in keys or
                k in exclude_keys or
                type(v) in exclude_valuetypes) and
            k[0] != '_'}

# source: http://blender.stackexchange.com/questions/1879/is-it-possible-to-dump-an-objects-properties-and-methods

def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


def catchall_debugger():
    import sys

    from IPython.core.debugger import Tracer  # noqa
    from IPython.core import ultratb

    sys.excepthook = ultratb.FormattedTB(mode='Verbose',
                                         color_scheme='Linux',
                                         call_pdb=True,
                                         ostream=sys.__stdout__)
