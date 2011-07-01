"""All role plug ins go in this directory.
"""

class Role(object):
    """Base class for roles.
    """
    def __init__(self, server, parameter = None):
        self.server = server
        self.parameter = parameter


    def configure(self):
        """Used to ensure that the role configuration is properly done.
        """
        pass
