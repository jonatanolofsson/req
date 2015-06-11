"""
Verification related functions
"""
import os
import argparse
import yaml

from .. import req
from .. import util
from .. import filesystem

VERIFIER_DIRECTORY = 'verifiers'
ROOT_FIELD = 'root'


def get_verifiers(field):
    """
    Get all verifiers associated with a field
    """
    dirs = [os.path.join(req.VERIFIER_DIRECTORY)]
    if 'VerifierDirectory' in req.conf():
        dirs.append(os.path.join(filesystem.reqroot(), req.conf()['VerifierDirectory']))
    for dir_ in dirs:
        path = os.path.join(dir_, field + '.py')
        if os.path.exists(path):
            module = util.import_source(path)
            yield module.verify

@req.extend(req.Requirement)
def verify_field(self, field):
    """
    Verify a single field
    """
    results = []
    for verifier in get_verifiers(field):
        results.append(verifier(self))
    return all(results)


@req.extend(req.Requirement)
def verify(self):
    """
    Verify a loaded object
    """
    results = [self.verify_field(ROOT_FIELD)]
    # pylint: disable=protected-access
    for key in self._data:
        results.append(self.verify_field(key))
    return all(results)


def parse_args(args):
    """
    Parse args
    """
    argparser = argparse.ArgumentParser(prog='req verify')
    argparser.add_argument(
        'limit',
        help='Limit search to specific directory',
        default=None,
        nargs="?")
    return argparser.parse_args(args)


def verify_module(module):
    """
    Verify a single module
    """
    try:
        yml = filesystem.load_yamlfile(module, multiple=True)
        return True
    except yaml.YAMLError as err:
        print('Yaml parsing failed: ', err)
        return False
    return all('Id' in config for config in yml)


def main(args):
    """
    Main
    """
    args = parse_args(args)
    results = []
    for module in req.get_modules(args.limit):
        result = verify_module(module)
        results.append(result)
        print("Module", module, result)
    print("{}/{} module verifications passed".format(sum(results), len(results)))

    if not all(results):
        print("Module verifications failed. Exiting.")
        exit(2)
    else:
        print('-'*40)

    results = []
    for reqobj in req.get_requirements(args.limit):
        result = reqobj.verify()
        try:
            id_ = reqobj.id()
        except KeyError:
            id_ = None

        print(reqobj.module(), id_, "[Pass]" if result else "[Fail]")
        results.append(result)
    print("{}/{} verifications passed".format(sum(results), len(results)))
    exit(0 if all(results) else 1)

if __name__ == '__main__':
    import sys
    main(sys.argv)
