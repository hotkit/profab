"""Plugins that allow the AMI to be chosen.
"""
from profab.role.ami import ChooseAMI
from profab import _logger
import urllib2
import re


RAW_PATTERN = r"<td><p> (\w+-\w+-\d+) </p></td>\n  <td><p> (\d+).+</p></td>\n  <td><p> (\w+) </p></td>\n.+\n.+ec2-run-instances (\w+-\w+) --instance-type (\w\d+[.]\w+)"
WEBSITE = "http://ubuntutym2.u-toyama.ac.jp/uec-images/releases/precise/release/"
COMPILED_PATTERN = re.compile(RAW_PATTERN)


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
            "32": {"ebs": {}, "instance": {}},
            "64": {"ebs": {}, "instance": {}}
        }
        for ami_tuple in ami_tuple_list:
            tmp[ami_tuple[1]][ami_tuple[2]][ami_tuple[0]] = ami_tuple[3]
        return tmp
    else:
        return None


FRESH_AMIS_DICT = struct_amis_dict()


class AddRole(ChooseAMI):
    """Data for Precise AMIs.
    """
    def ami(self, region, bits, size):
        # pylint: disable = E1101
        disk = 'ebs' if size == 't1.micro' else 'instance'
        amis = struct_amis_dict()
        return amis[str(bits)][disk].get(region, None)
