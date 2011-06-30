"""Helper functions for the entry point scripts.

"""


def process_arguments(*args):
    """Convert the arguments into a list of commands or options and values.
    """
    args = list(args) # Convert tuple to list
    args.reverse() # We really wanted head() here...
    instructions = []
    while len(args):
        print args
        head = args.pop()
        print args, head
        if head.startswith('--'):
            instructions.append((head[2:], args.pop()))
        else:
            instructions.append((head, None))
    return instructions
