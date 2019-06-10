'''
$ export PYTHONPATH=`pwd`/src
$ docker run -d --rm -p5672:5672 -p8080:15672 rabbitmq:3-management

'''


import unittest, json, logging, re, time
logging.basicConfig(level=logging.DEBUG)

from frmq import *
from fradb import *
from config import CONFIG
from fractman import *

class test_MQMan(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_init(self):
        mqm=MQMan()
        mqm.open()

class test_RabbitMQMan(unittest.TestCase):
    def setUp(self):
        self.mqm = RabbitMQMan()
        self.mqm.open()

    def tearDown(self):
        self.mqm.close()
    
    def test_init(self):
        pass 

    def test_make_queue(self):
        self.mqm.make_queue('kitaq')

    def test_get_queue_size(self):
        self.mqm.make_queue('kitaq')
        self.assertTrue(type(self.mqm.get_queue_size('kitaq')) == type(123))

    def test_purge(self):
        self.mqm.make_queue('kitaq')
        self.mqm.ch.basic_publish(exchange='', routing_key='kitaq', body="test123", properties=pika.BasicProperties(delivery_mode=2))
        self.mqm.ch.basic_publish(exchange='', routing_key='kitaq', body="test123", properties=pika.BasicProperties(delivery_mode=2))
        self.mqm.ch.basic_publish(exchange='', routing_key='kitaq', body="test123", properties=pika.BasicProperties(delivery_mode=2))
        self.mqm.ch.basic_publish(exchange='', routing_key='kitaq', body="test123", properties=pika.BasicProperties(delivery_mode=2))
        
        self.mqm.purge('kitaq')
        time.sleep(0.5)
        self.assertTrue(self.mqm.get_queue_size('kitaq') == 0)

    def test_delete(self):
        self.mqm.make_queue('kitaq')
        self.mqm.ch.basic_publish(exchange='', routing_key='kitaq', body="test123", properties=pika.BasicProperties(delivery_mode=2))
        self.mqm.ch.basic_publish(exchange='', routing_key='kitaq', body="test123", properties=pika.BasicProperties(delivery_mode=2))
        self.mqm.ch.basic_publish(exchange='', routing_key='kitaq', body="test123", properties=pika.BasicProperties(delivery_mode=2))
        self.mqm.ch.basic_publish(exchange='', routing_key='kitaq', body="test123", properties=pika.BasicProperties(delivery_mode=2))
        
        self.mqm.delete('kitaq')
        #time.sleep(0.1)
        self.mqm.make_queue('kitaq')
        self.assertTrue(self.mqm.get_queue_size('kitaq') == 0)


class test_TaskPublisher(unittest.TestCase):
    def setUp(self):
        self.tp = TaskPublisher()
        self.tp.open()

    def tearDown(self):
        self.tp.close()

    def test_push(self):
        self.tp.make_queue('kitaq2')
        self.tp.push('kitaq2', 'foobar123')
        
class test_TaskWorker(unittest.TestCase):
    def setUp(self):
        self.tw = TaskWorker()
        self.tw.open()

    def tearDown(self):
        self.tw.close()
    def test_callbackd(self):
        pass
    #def test_comsume(self):
    #    self.tw.comsume('kitaq')

class test_SimpleDumpWorker(unittest.TestCase):
    def setUp(self):
        self.sdw = SimpleDumpWorker()
        self.sdw.open()

    def tearDown(self):
        self.sdw.close()
    def test_consume(self):
        #self.sdw.consume('kitaq')
        pass

class test_TestGenPublisher(unittest.TestCase):
    def setUp(self):
        self.tgp = TestGenPublisher()


    def tearDown(self):
        pass
    def test_push(self):
        # clear queue
        self.mqm = RabbitMQMan()
        self.mqm.open()
        self.mqm.make_queue('fractq')
        self.mqm.purge('fractq')


        urllist=['http://abc1.com/', 'https://b.co/index.html']
        self.tgp.push('fractq', '12345678', urllist, 'prod.com', 'stag.com')

        dumper=TaskWorker()
        dumper.open()
        dumper.make_queue('fractq')
        m,p,b = dumper.pull_single_msg('fractq')
        
        self.assertTrue(json.loads(b)['urllist'] == urllist)
        self.assertTrue(json.loads(b)['src_ghost'] == 'prod.com')
        self.assertTrue(json.loads(b)['dst_ghost'] == 'stag.com')
        #self.assertTrue( b['urllist'] == urllist)
        logging.debug(b)

    def test_push_for_multi_workertest(self):
        # publish testgen
        urllist=['https://space.ktmrmshk.com/', 'https://space.ktmrmshk.com/js/mobile.js']
        publisher = TestGenPublisher()
        publisher.push('fractq2', '12345678', urllist, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')

        

class test_FractWorker(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass


    def test_sub_testgen_with_mongo_dumper(self):
        # publish testgen
        urllist=['https://space.ktmrmshk.com/', 'https://space.ktmrmshk.com/js/mobile.js']
        publisher = TestGenPublisher()
        publisher.push('fractq', '1981121111', urllist, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')

        ### spawn worker
        worker = FractWorker()
        worker.open()

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
        worker.open()
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



