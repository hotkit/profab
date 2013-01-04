"""Choose the latest AMI for Ubuntu Lucid.
"""
from profab.role.ami import ChooseAMI, struct_amis_dict


class AddRole(ChooseAMI):
    """Data for Lucid AMIs.
    """
    def ami(self, region, bits, size):
        # pylint: disable = E1101
        disk = 'ebs' if size == 't1.micro' else 'instance'
        amis = struct_amis_dict('lucid')
        return amis[str(bits)][disk].get(region, None)

