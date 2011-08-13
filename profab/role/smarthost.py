"""Sets up exim4 on the host and configures it as a smart host.
"""
from fabric.operations import sudo

from profab.role import Role


class AddRole(Role):
    """Adds exim4 to the server and configures it as a smart host relaying
    for local IP numbers only.
    """
    packages = ['exim4']

    def configure(self, server):
        """Re-configures exim4 to be a smart host.
        """
        sudo(
            '''sed -i.bak -r -e '''
                '''"s/dc_eximconfig_configtype='local'/'''
                    '''dc_eximconfig_configtype='internet'/g" '''
                '''/etc/exim4/update-exim4.conf.conf''')
        sudo('service exim4 restart')
