import unittest
from motleylog.motleylogconfig import MotleyLogConfig as MLC
class TestMotleyLogConfig(unittest.TestCase):

    def test_set_get_trace_level_num(self):
        self.assertEqual(8,MLC.get_trace_level_num())
        MLC.set_trace_level_num(5)
        self.assertEqual(5,MLC.get_trace_level_num())
        self.assertEqual(5,MLC.TRACE_LEVEL_NUM)

    def test_set_get_trace_level_name(self):
        self.assertEqual("TRACE",MLC.get_trace_level_name())
        MLC.set_trace_level_name("TRACK")
        self.assertEqual("TRACK",MLC.get_trace_level_name())
        self.assertEqual("TRACK",MLC.TRACE_LEVEL_NAME)

    def test_set_get_trace_method_name(self):
        self.assertEqual("trace",MLC.get_trace_method_name())
        MLC.set_trace_method_name("track")
        self.assertEqual("track",MLC.get_trace_method_name())
        self.assertEqual("track",MLC.TRACE_METHOD_NAME)

if __name__ == '__main__':
    unittest.main()
