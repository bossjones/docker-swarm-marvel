# source: https://stackoverflow.com/questions/29394535/convert-unicode-list-into-python-list
import ast
from ansible import errors

# Eg. converts u'[]' -> []
# Or
# Eg. u'["","aa","bb","cc"]' -> ['', 'aa', 'bb', 'cc']
# Usage Example: "{{ fact_public_subnets_array | unicode_str_to_list }}"

def unicode_str_to_list(a_var):
    # NOTE: If the variable comes in as a list aleardy, convert it into a unicode string first. This happens when we have a populated array.
    # Otherwise, if the list isn't populated, it comes in as a unicode string already.
    if isinstance(a_var, list):
        a_var = str(a_var)
    try:
        return ast.literal_eval(a_var)
    except Exception, e:
        raise errors.AnsibleFilterError('a_var plugin error: %s, evaluates: "%s"' % str(e),str(a_var) )

class FilterModule(object):
    ''' A filter to see if a sub string exists inside a list using regex. '''
    def filters(self):
        return {
            'unicode_str_to_list' : unicode_str_to_list
        }
