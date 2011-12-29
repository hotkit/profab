"""All role plug ins go in this directory.
"""


class Role(object):
    """Base class for roles.
    """
    # By default require no packages
    packages = []

    def __init__(self, parameter = None):
        self.parameter = parameter


    def region(self):
        """Called to determine the region to connect to when starting a new
        instance.
        """
        pass


    def size(self):
        """Called to determine the instance size to be started.
        """
        pass


    def bits(self, size):
        """Returns the number of bits that the AMI operating system should
        match.
        """
        pass


    def ami(self, region, bits, size):
        """Called to determine the AMI type to use when starting a new
        instance.
        """
        pass


    def run_kwargs(self, kwargs):
        """Called to customise other parameters to the instance run command.
        """
        # This method can't be a function as sub-classes will want access
        # to self
        # pylint: disable = R0201
        return kwargs


    def started(self, server):
        """Called just after the instance is started up, but before it has
        been confirmed that the instance is fully booted.
        """
        pass


    def configure(self, server):
        """Used to ensure that the role configuration is properly done.
        """
        pass
