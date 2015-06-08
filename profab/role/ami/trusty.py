"""Choose the latest AMI for Ubuntu Trusty.
"""
from profab.role.ami.ubuntu import Configure


class AddRole(Configure):
    """Data for Trusty AMIs.
    """
    def __init__(self):
        super(AddRole, self).__init__('trusty')

