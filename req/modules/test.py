"""
Test a requirement
"""
import os
import argparse
import shlex

from .. import req
from .. import command as subprocess

TEST_FILE = 'test'


def parse_args(args):
    """
    Parse args
    """
    argparser = argparse.ArgumentParser(prog='req test')
    argparser.add_argument(
        'limit', help='Limit search to specific directory', default=None, nargs="?")
    return argparser.parse_args(args)


@req.Requirement.extend('test')
def test(self, store_result=True):
    """
    Run the test defined for a requirement
    """
    result = subprocess.call(
        shlex.split(self['Test']),
        stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        cwd=os.path.dirname(self.path())
    ) == 0
    if store_result:
        self.store_property('status', result)
    return result


def main(args):
    """
    Main
    """
    args = parse_args(args)
    results = list(tst.test() for tst in req.get_requirements(args.limit))
    print("{}/{} tests passed".format(sum(results), len(results)))
    exit(0 if all(results) else 1)


if __name__ == '__main__':
    import sys
    main(sys.argv)
