from fabric.api import env
from fabric.state import connections


def start_connection(*args, **kwargs):
    print "Fabric is connecting to machine", env.host_string
    connections['ubuntu@%s:22' % env.host_string] = True
    return ''
