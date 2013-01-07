"""Choose the latest AMI for Ubuntu Precise.
"""
from profab.role.ami.ubuntu import Configure


class AddRole(Configure):
    """Data for Precise AMIs.
    """
    def __init__(self):
        super(AddRole, self).__init__('precise')

