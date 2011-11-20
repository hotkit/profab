"""Plugins that allow the AMI to be chosen.
"""
from profab.role.ami import ChooseAMI


class AddRole(ChooseAMI):
    """Data for Oneiric AMIs.
    """
    # http://ubuntutym2.u-toyama.ac.jp/uec-images/oneiric/20111109/
    AMIS = {
        '32': {
            'ebs': {
                'ap-northeast-1' : 'ami-741ca875',
                'ap-southeast-1' : 'ami-f0fb81a2',
                'eu-west-1': 'ami-e3d6eb97',
                'us-east-1': 'ami-0bcb0262',
                'us-west-1' : 'ami-ed0857a8',
            },
            'instance': {
                'ap-northeast-1' : 'ami-321ca833',
                'ap-southeast-1' : 'ami-08fb815a',
                'eu-west-1': 'ami-65d6eb11',
                'us-east-1': 'ami-43c9002a',
                'us-west-1' : 'ami-b10956f4',
            }
        },
        '64': {
            'ebs': {
                'ap-northeast-1' : 'ami-7e1ca87f',
                'ap-southeast-1' : 'ami-fafb81a8',
                'eu-west-1': 'ami-dbd6ebaf',
                'us-east-1': 'ami-1dcb0274',
                'us-west-1' : 'ami-ef0857aa',
            },
            'instance': {
                'ap-northeast-1' : 'ami-4e1ca84f',
                'ap-southeast-1' : 'ami-26fb8174',
                'eu-west-1': 'ami-4fd6eb3b',
                'us-east-1': 'ami-ebc90082',
                'us-west-1' : 'ami-4b08570e',
            }
        }
    }

