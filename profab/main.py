"""Helper functions for the entry point scripts.

"""


def process_arguments(*args):
    """Do the initial argument parse phase. This produces tuples of role
    instructions
    """
    args = list(args) # Convert tuple to list
    args.reverse() # We really wanted head() here, but no matter...
    instructions = []
    while len(args):
        head = args.pop()
        if head.startswith('--'):
            instructions.append((head[2:], args.pop()))
        else:
            instructions.append((head, None))
    return instructions
