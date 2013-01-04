"""Choose the latest AMI for Ubuntu Precise.
"""
from profab.role.ami import ChooseAMI, struct_amis_dict


class AddRole(ChooseAMI):
    """Data for Precise AMIs.
    """
    def ami(self, region, bits, size):
        # pylint: disable = E1101
        disk = 'ebs' if size == 't1.micro' else 'instance'
        amis = struct_amis_dict()
        return amis[str(bits)][disk].get(region, None)

