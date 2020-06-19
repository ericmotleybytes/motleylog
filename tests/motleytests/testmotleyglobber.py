import unittest
import motleylog.motleyglobber as globber
class TestMotleyGlobber(unittest.TestCase):
    def test_globber(self):
        samples = {
            "*.thing" : {
                "regex"   : "^.*\.thing$",
                "matches" : ["hello.thing", ".thing", "Bork.thing","a.b.thing"],
                "misses"  : ["hellothing", "thing", "Borkthing", "hello.thing2" ]
            },
            "do*.thing": {
                "regex"  : "^do.*\.thing$",
                "matches": ["dohello.thing", "do.thing", "doDO.thing", "do.get.thing"],
                "misses" : ["dohellothing", "dothing", "DOthing", "Do.get.thing"]
            }
        }
        for glob in samples:
            expRegex = samples[glob]["regex"]
            actRegex = globber.glob_to_re(glob)
            self.assertEqual(expRegex,actRegex)
            matches  = samples[glob]["matches"]
            for m in matches:
                result = globber.string_matches_glob(m,glob)
                self.assertTrue(result,f"{m} did not match {glob}.")
            misses   = samples[glob]["misses"]
            for m in misses:
                result = globber.string_matches_glob(m,glob)
                self.assertFalse(result,f"{m} unexpectantly matched {glob}.")

if __name__=='__main__':
    unittest.main()
