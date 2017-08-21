from profab.role import Role


class Configure(Role):
    """Allows a specific size to be chosen.
    """
    def subnet_id(self):
        """Return the subnet id that was specified.
        """
        return self.parameter