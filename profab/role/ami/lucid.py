"""Plugins that allow the AMI to be chosen.
"""
from profab.role import Role


AMIS = {
    '32': {
        'ebs': {
            'ap-northeast-1' : 'ami-32d36633',
            'ap-southeast-1' : 'ami-44f18916',
            'eu-west-1': 'ami-52417126',
            'us-east-1': 'ami-2cc83145',
            'us-west-1' : 'ami-95c694d0',
        },
        'instance': {
            'ap-northeast-1' : 'ami-96d06597',
            'ap-southeast-1' : 'ami-1cf0884e',
            'eu-west-1': 'ami-945f6fe0',
            'us-east-1': 'ami-81b275e8',
            'us-west-1' : 'ami-73c69436',
        }
    }
}

class AddRole(Role):
    """Returns the right Lucid AMI name.
    """
    def ami(self, region):
        """Return the AMI that was passed in to the role.
        """
        return AMIS['32']['instance'].get(region, None)
