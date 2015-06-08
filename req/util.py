"""
req utilities
"""
import os
import importlib.machinery

def walkup(leaf):
    """
    Visit all parent directories of leaf (including leaf)
    """
    new_dir = os.path.dirname(leaf)
    while new_dir != leaf:
        yield leaf
        leaf, new_dir = new_dir, os.path.dirname(new_dir)


def _get_libpath(path):
    """
    Convert a path to a libpath, putting '.' between each directory
    of the absolute path
    """
    return '.'.join(
        os.path.splitdrive(os.path.dirname(
            os.path.abspath(path)))[1].strip('\\/').split('/')
        + [os.path.splitext(os.path.basename(path))[0]])


def import_source(source_file, module_name=None):
    """
    Import python module from source
    """
    module_name = module_name or _get_libpath(source_file)
    return importlib.machinery.SourceFileLoader(module_name, source_file).load_module()

def print_table(data):
    """
    Print data as formatted table
    """
    for line in data.values():
        print("\t".join((str(x) for x in line.values())))
