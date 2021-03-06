import sys
sys.path.append('../src/')
import unittest, json, logging, os
from fradb import *
from config import CONFIG


logging.basicConfig(level=logging.DEBUG)

inputjsonfile = './cmdline_test_input/testcase_redirection.json'
outputjsonfile = './cmdline_test_output/mongodb_output.json'


class test_Mongo(unittest.TestCase):
    def test_getInstance(self):
        m1 = Mongo.getInstance('localhost', 27017)
        m2 = Mongo.getInstance('localhost', 27017)
        self.assertTrue(m1 is m2)

        m3 = Mongo.getInstance('127.0.0.1', 27017)
        self.assertTrue(m1 is not m3)

class test_mongojson(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_inputandoutput(self):
        logging.info('Testing: MongoDB input and output Start')
        mj = mongojson(CONFIG['db']['host'], CONFIG['db']['port'])
        mj.input(inputjsonfile, 'testdb', 'testcollection')
        mj.output(outputjsonfile, 'testdb', 'testcollection')
        self.assertTrue(os.path.isfile(outputjsonfile))
        if os.path.isfile(outputjsonfile):
            with open(outputjsonfile, mode='r') as rf:
                self.assertTrue('fract.akamaized-staging.net' in rf.read())
        logging.info('Testing: MongoDB input and output End')

    def test_push_many_find(self):
        
        class testobj(object):
            def __init__(self, name, age):
                self.dat = {'name':name, 'age':age}
            def __str__(self):
                return json.dumps(self.dat)
        d_list = []
        d_list.append( testobj('akamai', 99) )
        d_list.append( testobj('gcp', 14) )
        d_list.append( testobj('aws', 42) )
        d_list.append( testobj('sato', 29) )

        mj = mongojson(CONFIG['db']['host'], CONFIG['db']['port'])
        mj.clean('test_push_many_find', 'testcol')
        mj.push_many(d_list, 'test_push_many_find', 'testcol', lambda i : i.dat)

        ret = mj.find({}, 'test_push_many_find', 'testcol')
        self.assertTrue( len(ret) == 4 )
        
        
    def test_count(self):
        d_list=[]
        d_list.append({'name': 'akamai', 'age': 20})
        d_list.append({'name': 'taro', 'age': 21})
        d_list.append({'name': 'hanako', 'age': 20})
        d_list.append({'name': 'sato', 'age': 23})
        d_list.append({'name': 'jiro', 'age': 20})
        
        mj = mongojson(CONFIG['db']['host'], CONFIG['db']['port'])
        mj.clean('test_count', 'testcol')
        mj.push_many(d_list, 'test_count', 'testcol')

        self.assertTrue( mj.count({}, 'test_count', 'testcol') == 5)
        self.assertTrue( mj.count({'age': 20}, 'test_count', 'testcol') == 3)

    def test_output_with_filter(self):
        d_list=[]
        d_list.append({'name': 'akamai', 'age': 20})
        d_list.append({'name': 'taro', 'age': 21})
        d_list.append({'name': 'hanako', 'age': 20})
        d_list.append({'name': 'sato', 'age': 23})
        d_list.append({'name': 'jiro', 'age': 20})
        
        mj = mongojson(CONFIG['db']['host'], CONFIG['db']['port'])
        mj.clean('test_count', 'testcol')
        mj.push_many(d_list, 'test_count', 'testcol')

        self.assertTrue( mj.count({'age': 20}, 'test_count', 'testcol') == 3)
        mj.output('test_output_with_filter.json', 'test_count', 'testcol', {'age': 20})
        with open('test_output_with_filter.json') as f:
            d=json.load(f)
            self.assertTrue(len(d) == 3)





if __name__ == '__main__':
    print('Version 0.1')
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
