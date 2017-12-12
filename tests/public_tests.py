import unittest
import numpy as np
import os.path
import cv2
import pickle
import inspect
from os.path import join


import adder

verbose = True
class TestAdder(unittest.TestCase):
    def setUp(self):
        self._adder = adder.Adder();
            
    def test_1(self):
        np.testing.assert_equal(3,self._adder.add(1,2));
        if(verbose):
            print(inspect.stack()[0][3],' Passed')
        
    def test_2(self):
        np.testing.assert_equal(1,self._adder.add(1,0));
        if(verbose):
            print(inspect.stack()[0][3],' Passed')
        
    def test_3(self):
        np.testing.assert_equal(0,self._adder.add(1,-1));
        if(verbose):
            print(inspect.stack()[0][3],' Passed')

                
def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdder)
    result = unittest.TextTestRunner().run(suite)
    return (result.testsRun,len(result.failures),len(result.errors))

if __name__ == '__main__':
    all_tests = False
    if(all_tests):
        unittest.main()
    else:
        suite = unittest.TestSuite()
        suite.addTest(TestAdder('test_1'))
        #suite.addTest(TestVB('test_multiple_phi'))
        runner=unittest.TextTestRunner()
        runner.run(suite)
