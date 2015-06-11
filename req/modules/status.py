"""
List status of all requirements
"""
import argparse

from .. import req


def parse_args(args):
    """
    Parse args
    """
    argparser = argparse.ArgumentParser(prog='req status')
    argparser.add_argument(
        'limit',
        help='Limit search to specific directory',
        default=None,
        nargs="?")
    argparser.add_argument(
        'ref', help='Git ref to query', default=None, nargs="?")
    argparser.add_argument(
        '--failing',
        help='Only display tests with failed or no results',
        action="store_true")
    return argparser.parse_args(args)


def status(limit=None, ref=None, filterfun=None):
    """
    Return a status report of all requirements under a directory
    """
    filterfun = filterfun if filterfun else lambda x: True
    objects = (reqobj for reqobj in req.get_requirements(limit, ref) if filterfun(reqobj))
    for reqobj in iter(objects):
        print(reqobj)
    return objects

def main(args):
    """
    Main
    """
    args = parse_args(args)
    def _filterfun(reqobj):
        """ Default filterfun """
        if args.failing:
            return reqobj.status() != True
        return True
    status(args.limit, args.ref, _filterfun)


if __name__ == '__main__':
    import sys
    main(sys.argv)

