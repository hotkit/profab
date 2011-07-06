"""All role plug ins go in this directory.
"""


class Role(object):
    """Base class for roles.
    """
    # By default require no packages
    packages = []

    def __init__(self, server, parameter = None):
        self.server = server
        self.parameter = parameter


    def started(self):
        """Called just after the instance is started up, but before it has
        been confirmed that the instance is fully booted.
        """
        pass


    def configure(self):
        """Used to ensure that the role configuration is properly done.
        """
        pass
