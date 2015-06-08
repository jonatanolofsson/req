"""
Verification related functions
"""
import os
import argparse

from .. import req
from .. import util

VERIFIER_DIRECTORY = 'verifiers'
ROOT_FIELD = 'root'


def get_verifiers(field):
    """
    Get all verifiers associated with a field
    """
    dirs = [os.path.join(req.reqdir(), VERIFIER_DIRECTORY),
            os.path.join(req.VERIFIER_DIRECTORY)]
    for dir_ in dirs:
        path = os.path.join(dir_, field + '.py')
        if os.path.exists(path):
            module = util.import_source(path)
            yield module.verify


def verify_field(key, reqobj):
    """
    Verify a single field
    """
    for verifier in get_verifiers(key):
        verifier(reqobj)


def verify_obj(reqobj):
    """
    Verify a loaded object
    """
    verify_field(ROOT_FIELD, reqobj)
    for key in reqobj:
        verify_field(key, reqobj)


def verify(reqfile):
    """
    Verify a requirement file
    """
    verify_obj(req.get(reqfile))


def parse_args(args):
    """
    Parse args
    """
    argparser = argparse.ArgumentParser(prog='req verify')
    argparser.add_argument('req', help='Requirement to verify')
    return argparser.parse_args(args)


def main(args):
    """
    Main
    """
    args = parse_args(args)
    verify(args.req)

if __name__ == '__main__':
    import sys
    main(sys.argv)
