"""Make a connection to a region.
"""
from boto.ec2.connection import EC2Connection


def ec2_connect(aws_access_key_id, aws_secret_access_key,
        region=None):
    """Create and return a connection to an EC2 region.
    """
    bootstrap = EC2Connection(aws_access_key_id, aws_secret_access_key)
    if region == 'us-east-1':
        return bootstrap
