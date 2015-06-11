"""
Filesystem related methods
"""
import os
import yaml

from . import command as subprocess
from . import util

GIT = ['git']
REQCONF_FILE = '.reqconfig'


def read_file(path, ref=None):
    """
    Read file from filesystem or git tree
    """
    def _load_file_from_fs():
        """
        Read and parse file from filesystem
        """
        with open(path) as file_:
            return file_.read()

    def _load_file_from_git():
        """
        Load file from git tree
        """
        blob_sha1 = subprocess.get_output(
            GIT + ['ls-tree', ref, path]
        ).split()[2]
        return subprocess.get_output(
            GIT + ['cat-file', 'blob', blob_sha1]
        )

    return _load_file_from_git() if ref else _load_file_from_fs()


def load_yamlfile(reqfile, ref=None, multiple=False):
    """
    Load requirement file
    """
    data = read_file(reqfile, ref)
    return yaml.load_all(data) if multiple else yaml.load(data)


def reqroot():
    """
    Get .req-dir
    """
    def _find_reqroot():
        """
        Find reqroot
        """
        for dir_ in util.walkup(os.getcwd()):
            if os.path.exists(os.path.join(dir_, REQCONF_FILE)):
                return dir_

        raise Exception("Not inside req directory")

    cwd = os.getcwd()
    if cwd not in reqroot.cache:
        reqroot.cache[cwd] = _find_reqroot()
    return reqroot.cache[cwd]
reqroot.cache = {}

