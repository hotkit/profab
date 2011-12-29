"""Plugins that allow the AMI to be chosen.
"""
from profab.role.ami import ChooseAMI


class AddRole(ChooseAMI):
    """Data for Natty AMIs.
    """
    # http://ubuntutym2.u-toyama.ac.jp/uec-images/natty/20111117/
    AMIS = {
        '32': {
            'ebs': {
                'ap-northeast-1' : 'ami-0cf94e0d',
                'ap-southeast-1' : 'ami-26dfa574',
                'eu-west-1': 'ami-1993ae6d',
                'us-east-1': 'ami-639b530a',
                'us-west-1' : 'ami-cb56098e',
                'us-west-2' : 'ami-ce8d00fe',
            },
            'instance': {
                'ap-northeast-1' : 'ami-b6fa4db7',
                'ap-southeast-1' : 'ami-68dfa53a',
                'eu-west-1': 'ami-6393ae17',
                'us-east-1': 'ami-659a520c',
                'us-west-1' : 'ami-61560924',
                'us-west-2' : 'ami-d08d00e0',
            }
        },
        '64': {
            'ebs': {
                'ap-northeast-1' : 'ami-14f94e15',
                'ap-southeast-1' : 'ami-d2dfa580',
                'eu-west-1': 'ami-0593ae71',
                'us-east-1': 'ami-719b5318',
                'us-west-1' : 'ami-d3560996',
                'us-west-2' : 'ami-328c0102',
            },
            'instance': {
                'ap-northeast-1' : 'ami-d6fa4dd7',
                'ap-southeast-1' : 'ami-3adfa568',
                'eu-west-1': 'ami-5f93ae2b',
                'us-east-1': 'ami-519a5238',
                'us-west-1' : 'ami-71560934',
                'us-west-2' : 'ami-d68d00e6',
            }
        }
    }

