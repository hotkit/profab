"""Plugins that allow the AMI to be chosen.
"""
from profab.role import Role


class AddRole(Role):
    """Returns the right Lucid AMI name.
    """
    def ami(self, region):
        """Return the AMI that was passed in to the role.
        """
        return {
            'ap-northeast-1' : 'ami-32d36633',
            'ap-southeast-1' : 'ami-44f18916',
            'eu-west-1': 'ami-52417126',
            'us-east-1': 'ami-2cc83145',
            'us-west-1' : 'ami-95c694d0',
        }[region]
