import re
from ansible import errors

# source: https://github.com/drmalex07/ansible-plugins/blob/c18acf8a27ab070c6fd12a3598e28783be1beaa5/filter_plugins/comprehension.py
# Return true if list is empty, false if not
# Q: Why don't you just use {{ fact_public_subnets_array | length > 0 }} ?
# A: Wanted something simpler than that, and it was only 12 lines of python to implement.
# Hoping that we can start creating more custom filters now that we have several examples to look at for inspiration
# Usage Example: "{{ fact_public_subnets_array | is_empty_list }}"

def is_empty_list(a_list):
    if not isinstance(a_list, list):
        a_list = list(a_list)

    n = len(a_list)
    try:
        if n == 0:
            return True
        else:
            return False
    except Exception, e:
        raise errors.AnsibleFilterError('is_empty_list plugin error: %s, evaluates: "%s"' % str(e),str(list(a_list)) )

def is_empty_list_print(a_list):
    try:
        if not list(a_list) and len(list(a_list)) == 0:
            return "list:{} len:{}".format(list(a_list),len(list(a_list)))
        else:
            return False
    except Exception, e:
        raise errors.AnsibleFilterError('is_empty_list plugin error: %s, evaluates: "%s"' % str(e),str(list(a_list)) )

class FilterModule(object):
    ''' A filter to see if a sub string exists inside a list using regex. '''
    def filters(self):
        return {
            'is_empty_list' : is_empty_list,
            'is_empty_list_print' : is_empty_list_print
        }
