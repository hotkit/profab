"""Make a connection to a region.
"""
from boto.ec2.connection import EC2Connection


DEFAULT_REGION = 'us-east-1'


def ec2_connect(config, region = DEFAULT_REGION):
    """Create and return a connection to an EC2 region.
    """
    bootstrap = EC2Connection(config.keys.api, config.keys.secret)
    if region == DEFAULT_REGION:
        return bootstrap
    region_info = bootstrap.get_all_regions(
        region_names=[region])[0]
    return region_info.connect(aws_access_key_id=config.keys.api,
            aws_secret_access_key=config.keys.secret)
