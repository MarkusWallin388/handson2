import md
md.run_md()
import sys, unittest
import os

class MdTests(unittest.TestCase):
    
    def test(self):
        
        

        self.assertTrue(os.path.exists('cu.traj'))


if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(MdTests)]
    testsuite = unittest.TestSuite(tests)
    tests = [unittest.TestLoader().loadTestsFromTestCase(MdTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())