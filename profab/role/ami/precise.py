"""Plugins that allow the AMI to be chosen.
"""
from profab.role.ami import ChooseAMI
from profab import _logger
import urllib2
import re

raw_pattern=r"<td><p> (\w+-\w+-\d+) </p></td>\n  <td><p> (\d+).+ </p></td>\n  <td><p> (\w+) </p></td>\n.+\n.+ec2-run-instances (\w+-\w+) --instance-type (\w\d+[.]\w+)"
website="http://ubuntutym2.u-toyama.ac.jp/uec-images/releases/precise/release/"

def struct_amis_dict():
    try:
        response=urllib2.urlopen(website)
    except HTTPError,e:
        _logger.error(e.msg)
        return None
    html=response.read()
    compiled_pattern=re.compile(raw_pattern)
    ami_tuple_list=compiled_pattern.findall(html)
    if ami_tuple_list:
        tmp={"32":{"ebs":{},"instance":{}},"64":{"ebs":{},"instance":{}}}
        for ami_tuple in ami_tuple_list:
            tmp[ami_tuple[1]][ami_tuple[2]][ami_tuple[0]]=ami_tuple[3]
        return tmp
    else:
        return None


class AddRole(ChooseAMI):
    """Data for Precise AMIs.
    """
    AMIS=struct_amis_dict()

