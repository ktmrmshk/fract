import unittest, json, logging, re

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
        self.sdw.consume('kitaq')



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()



