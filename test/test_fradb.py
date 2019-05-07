import sys
sys.path.append('../src/')
import unittest, json, logging, os
from fradb import mongojson

inputjsonfile = './cmdline_test_input/testcase_redirection.json'
outputjsonfile = './cmdline_test_output/mongodb_output.json'

class test_Mongo(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_inputandoutput(self):
        logging.info('Testing: MongoDB input and output Start')
        mj = mongojson()
        mj.input(inputjsonfile, 'testdb', 'testcollection')
        mj.output(outputjsonfile, 'testdb', 'testcollection')
        self.assertTrue(os.path.isfile(outputjsonfile))
        if os.path.isfile(outputjsonfile):
            with open(outputjsonfile, mode='r') as rf:
                self.assertTrue('fract.akamaized-staging.net' in rf.read())
        logging.info('Testing: MongoDB input and output End')

if __name__ == '__main__':
    print('Version 0.1')
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()