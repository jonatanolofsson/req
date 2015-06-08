"""
Req main lib
"""
import json
import os
import hashlib

from . import filesystem
from . import command as subprocess
from . import db

GIT = ['git']
_THIS_DIR = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
VERIFIER_DIRECTORY = os.path.join(_THIS_DIR, 'verifiers')
TESTDIR = os.path.join(_THIS_DIR, 'testdirs')


class Requirement(object):
    """
    Requirement class
    """
    _data = {}
    _ref = None
    _objref = None
    _key = None
    _path = None
    def __init__(self, path, ref=None):
        """ Init """
        self._ref = ref
        self._path = os.path.abspath(path)
        self._objref = db.objref(self._ref)
        self._data = filesystem.load_yamlfile(self._path, ref)
        self._key = get_key(self.fullname())

    def status(self):
        """ Return the recorded teststatus of the requirement """
        return self.cdb().get(self.key(), {}).get('status', None)

    def store_property(self, prop, value):
        """ Store single property in database """
        cdb_ = self.cdb()
        reqdata = cdb_.get(self.key(), {})
        reqdata[prop] = value
        cdb_[self.key()] = reqdata

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
        return "{}\t{}\t{}\t{}".format(
            self.key(short=True),
            self.status(),
            self.path(),
            self['Title']
        )

    def __repr__(self):
        """ Repr """
        return json.dumps(self._data, sort_keys=True)

    def key(self, short=False):
        """ Return key """
        return self._key[0:10] if short else self._key

    def path(self):
        """ Get path """
        return self._path

    def ref(self):
        """ Get ref """
        return self._ref

    def fullname(self):
        """ Get path relative reqroot """
        return os.path.relpath(self._path, filesystem.reqroot())

    @staticmethod
    def extend(name):
        """ Extend the class with new methods """
        def _extend(fun):
            """ Extend the class with new methods """
            setattr(Requirement, name, fun)
        return _extend


def conf(ref=None):
    """ Load req configuration """
    return filesystem.load_yamlfile(os.path.join(filesystem.reqroot(),
                                                 filesystem.REQCONF_FILE), ref)


def get_key(reqfile):
    """ Get unique key for a given requirement """
    return hashlib.sha1(reqfile.encode('utf-8')).hexdigest()


def get(reqfile, ref=None):
    """ Retrieve contents of reqfile as yaml """
    if ref not in get.cache:
        get.cache[ref] = {}
    if reqfile not in get.cache[ref]:
        get.cache[ref][reqfile] = Requirement(reqfile, ref)
    return get.cache[ref][reqfile]
get.cache = {}


def get_requirements(limit=None, ref=None):
    """
    Get all requirements, optionally limited to a specific directory
    """
    path = os.path.abspath(limit) if limit else filesystem.reqroot()
    assert filesystem.reqroot() in path, "Directory is outside reqroot"
    if ref:
        yield from (get(line.split()[3], ref) for line in subprocess.get_output(
            GIT + ['ls-tree', '-r', ref, '--', path]
        ).splitlines() if line.endswith('.req'))
    else:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            yield from (get(os.path.join(root, file_))
                        for file_ in files if file_.endswith(".req"))

