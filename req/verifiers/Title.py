"""
Title verifier
"""

def verify(reqobj):
    """
    Verify title
    """
    if len(reqobj['Title']) == 0:
        print("Title is empty")
        return False
    return True
