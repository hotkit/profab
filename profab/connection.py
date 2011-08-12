"""Make a connection to a region.
"""
from boto.ec2 import get_region
from boto.ec2.connection import EC2Connection


def ec2_connect(config):
    """Create and return a connection to an EC2 region.
    """
    bootstrap = EC2Connection(config.keys.api, config.keys.secret)
    if config.region == 'us-east-1':
        return bootstrap
    region_info = bootstrap.get_all_regions(
        region_names=[config.region])[0]
    return region_info.connect(aws_access_key_id=config.keys.api,
            aws_secret_access_key=config.keys.secret)
