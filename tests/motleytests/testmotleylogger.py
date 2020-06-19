import unittest
from io import StringIO
from unittest.mock import patch
from motleylog.motleylogger import MotleyLogger
class TestMotleyLogger(unittest.TestCase):
    def test_motleylogger_instantiate(self):
        logger = MotleyLogger("")
        with patch('sys.stdout', new=StringIO()) as capturedOutput:
            logger.info(__name__ + ": Message 1")
        capout = capturedOutput.getvalue().strip()
        self.assertTrue(capout.find("INFO")>=0)
        self.assertTrue(capout.find("Message 1")>=0)

if __name__=='__main__':
    unittest.main()
