"""Plugins that allow the AMI to be chosen.
"""
import collections
import json
import re
import urllib2

from profab import _logger
from profab.role import Role


class Configure(Role):
    """Ask for the specified Ubuntu release.
    """

    def ami(self, region, bits, size):
        """Return the AMI that was passed in to the role.
        """
        disk = 'ebs' if size == 't1.micro' else 'instance'
        amis = struct_amis_dict(self.parameter)
        return amis[str(bits)][disk].get(region, None)


def _fetch_html(url):
    """Return the HTML for the given URL (so we can patch it)
    """
    response = urllib2.urlopen(url)
    return response.read()


Ami = collections.namedtuple('Ami', ['zone', 'bits', 'instance_type', 'ami_id'])


def _get_ami_list(response, release):
    id_matcher = re.compile(r'>(\w+-[0-9a-fA-F]+)</a>')
    json_encoded = response.replace('\n', '').replace(',]', ']')
    raw_ami_list = filter(lambda l: l[1] == release, json.loads(json_encoded)['aaData'])
    platform_bits = dict(amd64='64', i386='32')

    ami_list = []
    for raw_ami in raw_ami_list:
        ami_id = id_matcher.findall(raw_ami[6])[0]
        bits = platform_bits[raw_ami[3]]
        ami_list.append(Ami(zone=raw_ami[0],
                            bits=bits,
                            instance_type=_get_instance_type(raw_ami[4]),
                            ami_id=ami_id))
    return ami_list


def _get_instance_type(raw_type):
    if raw_type == 'instance-store':
        return 'instance'
    return raw_type


def struct_amis_dict(release):
    """Download the AMI list HTML and parse it to find the AMI codes
    for the various versions of Ubuntu.
    """
    try:
        response = _fetch_html('http://cloud-images.ubuntu.com/locator/ec2/releasesTable')
    except urllib2.HTTPError, error:
        _logger.error(error.msg)
        return None
    ami_list = _get_ami_list(response, release)
    if ami_list:
        result_dict = dict()
        instance_types = set(map(lambda ami: ami.instance_type, ami_list))
        for bits in ("32", "64"):
            result_dict[bits] = {_type: {} for _type in instance_types}
        for ami in ami_list:
            try:
                result_dict[ami.bits][ami.instance_type][ami.zone] = ami.ami_id
            except:
                _logger.error(ami)
                raise
        return result_dict
    else:
        _logger.error("No AMIs found in HTML")
        return None
