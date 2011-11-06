"""Allow a security group to be added to the instance.
"""
from profab.role import Role


class Configure(Role):
    """Add a security group to a machine.

    May be added multiple times.
    """
    def run_kwargs(self, kwargs):
        """Add the security group to the kwargs for the run parameter.
        """
        if not kwargs.has_key('security_groups'):
            kwargs['security_groups'] = [self.parameter]
        else:
            kwargs['security_groups'].append(self.parameter)
        return kwargs

