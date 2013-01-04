"""Choose the latest AMI for Ubuntu Precise.
"""
from profab.role.ami import ChooseAMI
from profab import _logger
import urllib2
import re


RAW_PATTERN = r"""(\w+-\w+-\d+).+\n""" \
    """\s+<td><p>\s+(32|64)-\w+.+\n""" \
    """\s+<td><p>\s+(\w+).+\n""" \
    """.+(\w\w\w-\w+)\s+</p></td>$"""
WEBSITE = "http://ubuntutym2.u-toyama.ac.jp" \
    "/uec-images/releases/precise/release/"
COMPILED_PATTERN = re.compile(RAW_PATTERN, re.MULTILINE)


def struct_amis_dict():
    try:
        response = urllib2.urlopen(WEBSITE)
    except urllib2.HTTPError, e:
        _logger.error(e.msg)
        return None
    html = response.read()
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


class AddRole(ChooseAMI):
    """Data for Precise AMIs.
    """
    def ami(self, region, bits, size):
        # pylint: disable = E1101
        disk = 'ebs' if size == 't1.micro' else 'instance'
        amis = struct_amis_dict()
        return amis[str(bits)][disk].get(region, None)
