"""
Root reqobj verifier
"""

def verify(reqobj):
    """
    Verify basic structure of reqobj
    """
    required_fields = {'Title', 'Description', 'Id'}
    missing_fields = [key for key in required_fields if key not in reqobj]
    if len(missing_fields) > 0:
        print("Missing fields: {}".format(", ".join(missing_fields)))
        return False
    return True
