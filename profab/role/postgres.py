"""Sets up and configures Postgres on the machine
"""
from profab.role import Role


class AddRole(Role):
    """Adds the default Postgres configuration.
    """
    packages = ['postgresql']

