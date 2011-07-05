"""Use an EIP on an instance. This is best used when a server is first
started otherwise there might be connection problems during the
session.
"""
from profab.role import Role


class Configure(Role):
    """Assign an EIP to the server.
    """
    def started(self):
        """Add the EIP to the server just after it has booted.
        """
        self.server.cnx.associate_address(
            self.server.instance.id, self.parameter)
        self.server.eip = self.parameter
