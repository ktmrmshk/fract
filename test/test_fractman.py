from fractman import *
from fradb import *
from fract import *

import unittest, json, logging, re, time, random
from config import CONFIG

logging.basicConfig(level=logging.DEBUG)

class test_TestGenMan(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_is_queue_empty(self):
        self.tgm=TestGenMan('123456789')
        self.assertTrue( self.tgm.is_queue_empty('abc123') )

    def test_num_task_completed(self):
        # push some result to db
        sessionid = str(random.random())
        mj =  mongojson(CONFIG['db']['host'], CONFIG['db']['port'])
        dat = [{'score': 1}, {'score':2}, {'score':3}]
        mj.push_many(dat, 'testdb', sessionid)

        self.tgm=TestGenMan(sessionid)
        self.tgm.cmd='testdb'
        self.assertTrue( self.tgm.num_task_completed() == 3) 

    def test_push(self):
        sessionid = str(random.random())
        urllist=['https://space.ktmrmshk.com/', 'https://space.ktmrmshk.com/js/mobile.js']

        self.tgm=TestGenMan(sessionid)
        self.tgm.pub.purge(CONFIG['mq']['queuename'])
        self.tgm.push(CONFIG['mq']['queuename'], urllist, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')

        self.assertTrue( self.tgm.num_task == 2)
        self.assertTrue( self.tgm.is_queue_empty(CONFIG['mq']['queuename']) == False)
        self.assertTrue( self.tgm.pub.get_queue_size(CONFIG['mq']['queuename']) == 1)

    def test_split_list(self):
        self.tgm=TestGenMan('123')

        l = [0,1,2,3,4,5,6,7,8,9]
        ret=list()
        for i in self.tgm.split_list(l, 3):
            ret.append(i)
        
        self.assertTrue( [0,1,2] in ret)
        self.assertTrue( [6,7,8] in ret)
        self.assertTrue( [9] in ret)

    def test_push_urllist_from_file(self):
        sessionid = str(random.random())
        self.tgm=TestGenMan(sessionid)
        self.tgm.pub.purge(CONFIG['mq']['queuename'])

        self.tgm.push_urllist_from_file('urllist4test.txt', 10, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')

        self.assertTrue( self.tgm.pub.get_queue_size(CONFIG['mq']['queuename']) == 4)

    def test_save(self):
        # push some result to db
        sessionid = str(random.random())
        mj =  mongojson(CONFIG['db']['host'], CONFIG['db']['port'])
        dat = [{'score': 1}, {'score':2}, {'score':3}]
        mj.clean('testdb', sessionid)
        mj.push_many(dat, 'testdb', sessionid)

        self.tgm=TestGenMan(sessionid)
        self.tgm.cmd='testdb'
        self.tgm.num_task = 3
        self.tgm.save('test_save')
        with open('test_save') as f:
            read_dat = json.load(f)
            self.assertTrue( len(read_dat) == len(dat) )

        #self.assertTrue( self.tgm.num_task_completed() == 3) 

    def test_save_except_inactive_testcase(self):
        # push testdata to mongo
        mj =  mongojson(CONFIG['db']['host'], CONFIG['db']['port'])
        mj.clean('testgen', '123456')
        mj.input('testcasejson4mongodbtest.json', 'testgen', '123456')
        tgm=TestGenMan('123456')
        tgm.num_task = 4
        tgm.save('test_save_except_inactive_testcase.json')
        with open('test_save_except_inactive_testcase.json') as f:
            d=json.load(f)
            self.assertTrue(len(d)==3)


class test_RunMan(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_push(self):
        sessionid = str(random.random())
        rm=RunMan(sessionid)

        # push data to mq
        testcases=None #FractClient(fract_suite_file='testcase4test.json')
        with open('testcase4test.json') as f:
            testcases=json.load(f)
        rm.pub.purge(CONFIG['mq']['queuename'])
        rm.push(CONFIG['mq']['queuename'], testcases)
        
        # pull from mq
        m, p, b = rm.pub.pull_single_msg(CONFIG['mq']['queuename'])
        msg = json.loads(b)
        self.assertTrue( msg['cmd'] == 'run')
        self.assertTrue('sessionid' in msg)
        #print(msg['testcases'])
        self.assertTrue(msg['testcases'][0]['TestType'] == 'hassert')

        
    def test_push_testcase_from_file(self):
        sessionid = str(random.random())
        rm=RunMan(sessionid)
        
        rm.pub.purge(CONFIG['mq']['queuename'])
        chunksize=5
        rm.push_testcase_from_file('testcase4test.json', chunksize)
        m, p, b = rm.pub.pull_single_msg(CONFIG['mq']['queuename'])
        msg = json.loads(b)
        self.assertTrue( msg['cmd'] == 'run')
        self.assertTrue('sessionid' in msg)
        self.assertTrue( len(msg['testcases']) == chunksize )

    def test_save(self):
        sessionid = str(random.random())
        rm=RunMan(sessionid)
        
        # test data push to mongo
        mj =  mongojson(CONFIG['db']['host'], CONFIG['db']['port'])
        with open('resultcase4test_sub.json') as f:
            results=json.load(f)
        mj.push_many(results, 'run', sessionid)

        
        rm.num_task=len(results)
        rm.save('resultcase4test_sub.json', 'test_save_ret.json', 'test_save_diff.json', 'test_save_summary.json')


#    def test_save2(self):
#        sessionid = '20190610185033196701'
#        rm=RunMan(sessionid)
#        mj =  mongojson()
#        rm.num_task=mj.count({}, 'run', sessionid)
#        rm.save('../src/bigtest.json','test_save_ret.json', 'test_save_diff.json', 'test_save_summary.json')
#


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
