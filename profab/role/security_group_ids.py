from profab.role import Role


class Configure(Role):
    """Add a security group to a machine.

    May be added multiple times.
    """
    def run_kwargs(self, kwargs):
        """Add the security group to the kwargs for the run parameter.
        """
        if not kwargs.has_key('security_group_ids'):
            kwargs['security_group_ids'] = [self.parameter]
        else:
            kwargs['security_group_ids'].append(self.parameter)
        return kwargs