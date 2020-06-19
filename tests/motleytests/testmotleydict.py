import unittest
from motleylog.motleydict import MotleyDict
class TestMotleyDict(unittest.TestCase):
    def test_motleydict(self):
        d1 = MotleyDict({"aaa" : "awesome", "bbb" : "bad"})
        self.assertEqual("awesome",d1["aaa"])
        self.assertEqual("bad",d1["bbb"])
        self.assertEqual("{ccc}",d1["ccc"])

if __name__=='__main__':
    unittest.main()
