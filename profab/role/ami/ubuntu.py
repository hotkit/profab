"""Plugins that allow the AMI to be chosen.
"""
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


RAW_PATTERN = r"""(\w+-\w+-\d+).+\n""" \
    r"""\s+<td><p>\s+(32|64)-\w+.+\n""" \
    r"""\s+<td><p>\s+(\w+).+\n""" \
    r""".+(\w\w\w-\w+)\s+</p></td>$"""
WEBSITE = "http://uec-images.ubuntu.com/releases/%s/release/"
COMPILED_PATTERN = re.compile(RAW_PATTERN, re.MULTILINE)


def _fetch_html(url):
    """Return the HTML for the given URL (so we can patch it)
    """
    response = urllib2.urlopen(url)
    return response.read()


def struct_amis_dict(release):
    """Download the AMI list HTML and parse it to find the AMI codes
    for the various versions of Ubuntu.
    """
    try:
        html = _fetch_html(WEBSITE % release)
    except urllib2.HTTPError, error:
        _logger.error(error.msg)
        return None
    ami_tuple_list = COMPILED_PATTERN.findall(html)
    if ami_tuple_list:
        tmp = {
            "32": {"ebs": {}, "instance": {}, "hvm": {}},
            "64": {"ebs": {}, "instance": {}, "hvm": {}},
        }
        for ami_tuple in ami_tuple_list:
            try:
                tmp[ami_tuple[1]][ami_tuple[2]][ami_tuple[0]] = ami_tuple[3]
            except:
                _logger.error(ami_tuple)
                raise
        return tmp
    else:
        _logger.error("No AMIs found in HTML")
        return None

