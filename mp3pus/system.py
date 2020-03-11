import os
import sys


def show_error(msg, code=1):
    print(
        os.path.basename(sys.argv[0]),
        'error',
        msg,
        sep=':',
        file=sys.stderr)
    sys.exit(code)


def check_dep(dep):
    for each in os.getenv('PATH').split(':'):
        if os.path.exists(os.path.join(each, dep)):
            return False
    return True
