"""
Verification related functions
"""
from . import req


def verify_field(key, reqobj):
    """
    Verify a single field
    """
    for verifier in get_verifiers(key):
        result = verifier(reqobj)
        assert result


def verify_obj(reqobj):
    """
    Verify a loaded object
    """
    for key in reqobj:
        _verify_single(key, reqobj)


def verify(reqfile):
    """
    Verify a requirement file
    """
    _verify_obj(req.get(reqfile))


