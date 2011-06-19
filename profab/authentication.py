import os
import socket

from boto.ec2.connection import EC2Connection

from profab import _logger


def get_keyname(config, cnx):
    hostname = socket.gethostname()
    get_private_key_filename(config, cnx)
    return hostname


def get_private_key_filename(config, cnx):
    hostname = socket.gethostname()
    foldername = os.path.expanduser('~/.profab/%s' % config.client)
    pathname = '%s/%s.pem' % (foldername, hostname)
    if not os.access(foldername, os.F_OK):
        os.mkdir(foldername)

    keys = cnx.get_all_key_pairs()
    for key in keys:
        if key.name == hostname:
            _logger.debug("Already found key on EC2 for hostname %s", hostname)
            return pathname
    _logger.info("No key pair found for host %s on EC2."
        " Creating new key pair.", hostname)
    pem = cnx.create_key_pair(hostname)
    pem.save(foldername)
    return pathname
