'''
$ export PYTHONPATH=`pwd`/src
$ docker run -d --rm -p5672:5672 -p8080:15672 --name mq rabbitmq:3-management 
$ docker run -d --rm -p27017:27017 --name db mongo 

'''


import unittest, json, logging, re, time
logging.basicConfig(level=logging.DEBUG)

from frmq import *
from fradb import *
from config import CONFIG
from fractman import *
from fractworker import *
from frmq import *

class test_TaskWorker(unittest.TestCase):
    def setUp(self):
        self.tw = TaskWorker()
        self.tw.open(CONFIG['mq']['host'], CONFIG['mq']['port'])

    def tearDown(self):
        self.tw.close()
    def test_callbackd(self):
        pass
    #def test_comsume(self):
    #    self.tw.comsume('kitaq')

class test_SimpleDumpWorker(unittest.TestCase):
    def setUp(self):
        self.sdw = SimpleDumpWorker()
        self.sdw.open(CONFIG['mq']['host'], CONFIG['mq']['port'])

    def tearDown(self):
        self.sdw.close()
    def test_consume(self):
        #self.sdw.consume('kitaq')
        pass


class test_FractWorker(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass


    def test_sub_testgen_with_mongo_dumper(self):
        # publish testgen
        urllist=['https://space.ktmrmshk.com/', 'https://space.ktmrmshk.com/js/mobile.js']
        publisher = TestGenPublisher(CONFIG['mq']['host'], CONFIG['mq']['port'])
        publisher.push('fractq', '1981121111', urllist, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')

        ### spawn worker
        worker = FractWorker()
        worker.open(CONFIG['mq']['host'], CONFIG['mq']['port'])

        ## Clean up collection
        mj = mongojson()
        mj.clean('testgen', '1981121111')


        worker.addCallback('testgen', Subtask_TestGen.do_task)
        #worker.consume('fractq')
        worker.pull_single_msg('fractq')
        
        # check
        ret = mj.find({}, 'testgen', '1981121111')
        self.assertTrue( len(ret) == 2 )

        mj.clean('testgen', '1981121111')

    def test_subtask_run(self):
        
        ### spawn worker
        worker = FractWorker()
        worker.open(CONFIG['mq']['host'], CONFIG['mq']['port'])
        worker.addCallback('run', Subtask_Run.do_task)


        # push msg
        sessionid = str(random.random())
        rm=RunMan(sessionid)

        rm.pub.purge(CONFIG['mq']['queuename'])
        chunksize=5
        rm.push_testcase_from_file('testcase4test.json', chunksize)
        
        # count number of testcase in this testcases file
        num_test=0
        with open('testcase4test.json') as f:
            tests = json.load(f)
            num_test=len(tests)
               
        # pull msg and do task
        worker.pull_single_msg(CONFIG['mq']['queuename'])
        
        # check the testresult
        mj = mongojson()
        
        ret = mj.find({}, 'run', sessionid)
        self.assertTrue( len(ret) == chunksize )



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()



