"""Functions for handling the authentication between the controlling
machine and the virtual machines.
"""
import os
import socket

from profab import _logger


def get_keyname(config, cnx):
    """Return the keyname that is to be used.
    """
    hostname = socket.gethostname()
    get_private_key_filename(config, cnx)
    return hostname


def get_private_key_filename(config, cnx):
    """Fetch the key filename for this configuration and connection.
    """
    hostname = socket.gethostname()
    foldername = os.path.expanduser('~/.profab/%s/%s' % (
        config.client, cnx.region.name))
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
