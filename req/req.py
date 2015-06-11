"""
Req main lib
"""
import json
import os
import re

from . import filesystem
from . import command as subprocess
from . import db

GIT = ['git']
_THIS_DIR = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
VERIFIER_DIRECTORY = os.path.join(_THIS_DIR, 'verifiers')
TESTDIR = os.path.join(_THIS_DIR, 'testdirs')
_FULLNAMEFORMAT = '{}[{}]'

# pylint: disable=invalid-name
class Requirement(object):
    """
    Requirement class
    """
    ALLOWED_STATES = ['ok']
    _data = {}
    _ref = None
    _objref = None
    _path = None
    _module = None
    def __init__(self, module, config, ref=None):
        """ Init """
        self._ref = ref
        self._objref = db.objref(self._ref)
        self._data = config
        self._module = os.path.relpath(module, filesystem.reqroot())
        self._path = os.path.abspath(self._module)

    def status(self):
        """ Return the recorded teststatus of the requirement """
        return self.cdb().get(self.id(), {}).get('status', None)

    def state(self):
        """ Get state """
        return self['State'] if 'State' in self and self['State'] in Requirement.ALLOWED_STATES \
            else None

    def store_property(self, prop, value):
        """ Store single property in database """
        cdb_ = self.cdb()
        reqdata = cdb_.get(self.id(), {})
        reqdata[prop] = value
        cdb_[self.id()] = reqdata

    def id(self):
        """ Return requirement id """
        return self['Id']

    def cdb(self):
        """ Access the commit database """
        return db.CommitDB.get_db(self._ref)

    def __getitem__(self, arg):
        """ Get property """
        return self._data[arg]

    def get(self, arg, default=None):
        """ Get property, oor default """
        return self._data[arg] if arg in self._data else default

    def __contains__(self, arg):
        """ Check if data exists """
        return arg in self._data

    def __str__(self):
        """ String representation of object """
        return '\t'.join((str(x) for x in [
            self.status(),
            self.state(),
            self.module(),
            self.id(),
            self['Title']
        ]))

    def __repr__(self):
        """ Repr """
        return json.dumps(self._data, sort_keys=True)

    def path(self):
        """ Get path """
        return self._path

    def module(self):
        """ Get module name """
        return self._module

    def ref(self):
        """ Get ref """
        return self._ref

    def fullname(self):
        """ Get path relative reqroot """
        return _FULLNAMEFORMAT.format(self._module, self['Id'])

def extend(eclass, name=None):
    """ Extend the class with new methods """
    def _extend(fun):
        """ Extend the class with new methods """
        setattr(eclass, fun.__name__ if name is None else name, fun)
    return _extend


def conf(ref=None):
    """ Load req configuration """
    if conf.conf is None:
        conf.conf = filesystem.load_yamlfile(os.path.join(filesystem.reqroot(),
                                                          filesystem.REQCONF_FILE), ref)
    return conf.conf
conf.conf = None


def load_module(reqfile, ref=None):
    """ Retrieve contents of reqfile as yaml """
    if ref not in load_module.cache:
        load_module.cache[ref] = {}
    if reqfile not in load_module.cache[ref]:
        load_module.cache[ref][reqfile] = [
            Requirement(reqfile, config, ref)
            for config in filesystem.load_yamlfile(reqfile, ref, True)]
    return load_module.cache[ref][reqfile]
load_module.cache = {}


def parse_limit(limit):
    """ Parse limit argument """
    idpatterns = None
    if limit:
        result = re.match(r'(?P<path>[^\[]+)?(\[(?P<idpatterns>.+)\]$)?', limit).groupdict("")
        path = os.path.abspath(result['path'])
        if result['idpatterns'] is not None:
            idpatterns = result['idpatterns'].split(',')
    else:
        path = filesystem.reqroot()
    assert filesystem.reqroot() in path, "Directory is outside reqroot"
    return path, idpatterns



def get_modules(limit=None, ref=None):
    """
    Get all requirement modules
    """
    path, _ = parse_limit(limit)
    if ref:
        yield from (line.split()[3] for line in subprocess.get_output(
            GIT + ['ls-tree', '-r', ref, '--', path]
        ).splitlines() if line.endswith('.req'))
    else:
        if os.path.isfile(path):
            yield path
        else:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                yield from (os.path.join(root, f) for f in files if f.endswith(".req"))


def get_requirements(limit=None, ref=None):
    """
    Get all requirements, optionally limited to a specific directory
    """
    path, idpatterns = parse_limit(limit)
    def _filterfun(reqobj):
        """ Filter requirements """
        return idpatterns is None or \
            any(re.match(idpattern, reqobj.id()) for idpattern in idpatterns)

    yield from (reqobj for module in get_modules(path, ref)
                for reqobj in load_module(module, ref)
                if _filterfun(reqobj))

