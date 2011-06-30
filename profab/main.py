"""Helper functions for the entry point scripts.

"""


def process_arguments(*args):
    """Convert the arguments into a list of commands or options and values.
    """
    instructions = []
    for arg in args:
        instructions.append(arg)
    return instructions
