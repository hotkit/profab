"""Plugins that allow the AMI to be chosen.
"""
from profab.role.ami import ChooseAMI


class AddRole(ChooseAMI):
    """Data for Lucid AMIs.
    """
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
        },
        '64': {
            'ebs': {
                'ap-northeast-1' : 'ami-34d36635',
                'ap-southeast-1' : 'ami-4af18918',
                'eu-west-1': 'ami-5c417128',
                'us-east-1': 'ami-63be790a',
                'us-west-1' : 'ami-97c694d2',
            },
            'instance': {
                'ap-northeast-1' : 'ami-f0d065f1',
                'ap-southeast-1' : 'ami-a6f088f4',
                'eu-west-1': 'ami-844070f0',
                'us-east-1': 'ami-fbbf7892',
                'us-west-1' : 'ami-89c694cc',
            }
        }
    }

