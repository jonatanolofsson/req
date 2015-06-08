"""
Command interface
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from subprocess import *

def get_output(*args, **kwargs):
    """ Get subprocess output """
    return check_output(*args, **kwargs).decode('utf-8')


