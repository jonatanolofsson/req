"""
Root reqobj verifier
"""

def verify(reqobj):
    """
    Verify basic structure of reqobj
    """
    required_fields = {'Title', 'Description'}
    missing_fields = [key for key in required_fields if key not in reqobj]
    assert len(missing_fields) == 0, "Missing fields: {}".format(", ".join(missing_fields))
