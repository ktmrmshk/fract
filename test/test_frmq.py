'''
$ export PYTHONPATH=`pwd`/src
$ docker run -d --rm -p5672:5672 rabbitmq:latest

'''


import unittest, json, logging, re
logging.basicConfig(level=logging.DEBUG)

from frmq import *
class test_MQMan(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_init(self):
        mqm=MQMan()

class test_RabbitMQMan(unittest.TestCase):
    def setUp(self):
        self.mqm = RabbitMQMan()
    def tearDown(self):
        self.mqm.close()
    
    def test_init(self):
        pass 

    def test_make_queue(self):
        self.mqm.make_queue('kitaq')

class test_TaskPublisher(unittest.TestCase):
    def setUp(self):
        self.tp = TaskPublisher()
    def tearDown(self):
        self.tp.close()

    def test_push(self):
        self.tp.make_queue('kitaq')
        self.tp.push('kitaq', 'foobar123')
        
class test_TaskWorker(unittest.TestCase):
    def setUp(self):
        self.tw = TaskWorker()
    def tearDown(self):
        self.tw.close()
    def test_callback(self):
        pass
    #def test_comsume(self):
    #    self.tw.comsume('kitaq')

class test_SimpleDumpWorker(unittest.TestCase):
    def setUp(self):
        self.sdw = SimpleDumpWorker()
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
        urllist=['http://abc1.com/', 'https://b.co/index.html']
        self.tgp.push(urllist)

        dumper=TaskWorker()
        dumper.make_queue('testgen')
        m,p,b = dumper.pullSingleMessage('testgen')
        
        self.assertTrue(json.loads(b)['urllist'] == urllist)
        #self.assertTrue( b['urllist'] == urllist)
        logging.debug(b)
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()



