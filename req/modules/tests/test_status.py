"""
Test status command
"""
import os
import unittest
import subprocess
_THIS_DIR = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
_REQDIR = os.path.dirname(os.path.dirname(os.path.dirname(_THIS_DIR)))
_REQBINDIR = os.path.join(_REQDIR, 'bin')
REQ = [os.path.join(_REQBINDIR, 'req')]

class StatusTest(unittest.TestCase):
    """ TestStatus """
    def test_status(self):
        """ test status call """
        result = subprocess.check_call(REQ + ['status'], cwd=_THIS_DIR,
                                       stdout=subprocess.DEVNULL)
        self.assertEqual(result, 0)

    def test_narrow(self):
        """ test status call with extra directory argument """
        result = subprocess.check_call(REQ + ['status', '.'], cwd=_THIS_DIR,
                                       stdout=subprocess.DEVNULL)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
