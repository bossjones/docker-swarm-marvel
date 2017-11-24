# FIXME: Doesn't work currently

# source:
# https://stackoverflow.com/questions/29394535/convert-unicode-list-into-python-list

import re
from ansible import errors

def to_slash_32(a_var):
    a_var = str(a_var)
    if re.search(r".*(/32)", a_var):
        return a_var
    else:
        return "{}/32".format(a_var)

class FilterModule(object):
    ''' A filter to see if a sub string exists inside a list using regex. '''

    def filters(self):
        return {
            'to_slash_32': to_slash_32
        }
