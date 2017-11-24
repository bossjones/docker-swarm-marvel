
import pprint
import re

def j2_to_file(fname):
    return re.sub(".j2", "", fname)

mapping = {
    "jinjaToFile": j2_to_file
}
