"""
Requirement temporal result database handling
"""
import json
from . import command as subprocess
GIT = ['git']
_DB_NOTESREF = 'reqs'

class CommitDB(object):
    """ Object representing a specific point in history """
    _ref = None
    _data = None
    def __init__(self, ref):
        """ Init """
        self._ref = ref

    def _load_data(self):
        """ Load data from db """
        if self._data is None:
            self._data = load(self._ref)

    def __setitem__(self, req, data):
        """ Store data in database """
        self._load_data()
        self._data[req] = data
        store(self._data, self._ref)

    def __getitem__(self, arg):
        """ Get value from database """
        self._load_data()
        return self._data[arg]

    def get(self, arg, default=None):
        """ Get value if key exists, else default """
        self._load_data()
        return self._data[arg] if arg in self._data else default

    def __contains__(self, arg):
        """ Check if data exists for a given requirement """
        self._load_data()
        return arg in self._data

    @staticmethod
    def get_db(ref):
        """ Retrieve a Commit object """
        if ref not in CommitDB.get_db.cache:
            CommitDB.get_db.cache[ref] = CommitDB(ref)
        return CommitDB.get_db.cache[ref]
CommitDB.get_db.cache = {}

def _read_db(ref, namespace=_DB_NOTESREF):
    """ Read database contents from GIT """
    try:
        return subprocess.get_output(GIT + ['notes', '--ref', namespace, 'show', ref],
                                     stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None


def _write_db(ref, data, namespace=_DB_NOTESREF):
    """ Write data to the database """
    subprocess.check_call(GIT + ['notes', '--ref', namespace, 'add', '-f', '-m', data, ref],
                          stderr=subprocess.DEVNULL)


def objref(ref=None):
    """ Get reference to object tree """
    def _get_index_hash():
        """ Get the hash of the current index """
        return subprocess.get_output(GIT + ['write-tree']).strip()


    def _get_tree_hash():
        """ Get the tree hash of a ref """
        return subprocess.get_output(GIT + ['rev-parse', ref + '^{tree}']).strip()

    return _get_tree_hash() if ref else _get_index_hash()


def store(data, ref=None, namespace=_DB_NOTESREF):
    """ Store data in the database """
    _write_db(objref(ref), json.dumps(data, sort_keys=True), namespace)


def load(ref=None, namespace=_DB_NOTESREF):
    """ Load data from the database """
    data = _read_db(objref(ref), namespace)
    return json.loads(data) if data else {}
