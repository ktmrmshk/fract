'''
$ export PYTHONPATH=`pwd`/src
$ docker run -d --rm -p5672:5672 -p8080:15672 --name mq rabbitmq:3-management 
$ docker run -d --rm -p27017:27017 --name db mongo 

/etc/hosts
127.0.0.1 rabbitmq mongodb

'''


import unittest, json, logging, re, time
logging.basicConfig(level=logging.DEBUG)

from frmq import *
from fradb import *
from config import CONFIG
from fractman import *
from fractworker import *

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
        self.mqm.open(CONFIG['mq']['host'], CONFIG['mq']['port'])

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
        self.tp.open(CONFIG['mq']['host'], CONFIG['mq']['port'])

    def tearDown(self):
        self.tp.close()

    def test_push(self):
        self.tp.make_queue('kitaq2')
        self.tp.push('kitaq2', 'foobar123')
        

class test_TestGenPublisher(unittest.TestCase):
    def setUp(self):
        self.tgp = TestGenPublisher(CONFIG['mq']['host'], CONFIG['mq']['port'])


    def tearDown(self):
        pass
    def test_push(self):
        # clear queue
        self.mqm = RabbitMQMan()
        self.mqm.open(CONFIG['mq']['host'], CONFIG['mq']['port'])
        self.mqm.make_queue('fractq')
        self.mqm.purge('fractq')


        urllist=['http://abc1.com/', 'https://b.co/index.html']
        self.tgp.push('fractq', '12345678', urllist, 'prod.com', 'stag.com')

        dumper=TaskWorker()
        dumper.open(CONFIG['mq']['host'], CONFIG['mq']['port'])
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
        publisher = TestGenPublisher(CONFIG['mq']['host'], CONFIG['mq']['port'])
        publisher.push('fractq2', '12345678', urllist, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')

        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()



