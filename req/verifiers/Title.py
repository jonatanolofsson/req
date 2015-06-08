"""
Title verifier
"""

def verify(reqobj):
    """
    Verify title
    """
    assert len(reqobj['Title']) > 0, "Title is empty"
