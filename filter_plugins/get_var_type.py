import re
from ansible import errors

# Not sure what type of object you're dealing with in ansible? Use this filter to print that info out.
# Usage Example: "{{ fact_public_subnets_array | get_var_type }}"

def get_var_type(a_var):
    try:
        return str(type(a_var))
    except Exception, e:
        raise errors.AnsibleFilterError('a_var plugin error: %s, evaluates: "%s"' % str(e),str(a_var) )

class FilterModule(object):
    ''' A filter to see if a sub string exists inside a list using regex. '''
    def filters(self):
        return {
            'get_var_type' : get_var_type
        }
