"""EC2 specific functionality needed to talk to its hypervisor outside
    of the context of a server.
"""
from boto.ec2 import regions

from profab import _logger


def get_all_reservations(config):
    """Return all reservations known to this connection.
    """
    reservations = []
    region_list = regions(aws_access_key_id=config.keys.api,
        aws_secret_access_key=config.keys.secret)
    for region in region_list:
        _logger.info("Searching %s", region)
        cnx = region.connect(aws_access_key_id=config.keys.api,
            aws_secret_access_key=config.keys.secret)
        for reservation in cnx.get_all_instances():
            _logger.info("Found %s %s", reservation,
                [str(i.id) for i in reservation.instances])
            reservations.append(reservation)
    return reservations

