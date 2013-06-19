"""Choose the latest AMI for Ubuntu Lucid.
"""
from profab.role.ami.ubuntu import Configure


class AddRole(Configure):
    """Data for Lucid AMIs.
    """
    def __init__(self):
        super(AddRole, self).__init__('lucid')

