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

class test_TaskPublisher(unittest.TestCase):
    def setUp(self):
        self.tp = TaskPublisher()
        self.tp.open()

    def tearDown(self):
        self.tp.close()

    def test_push(self):
        self.tp.make_queue('kitaq')
        self.tp.push('kitaq', 'foobar123')
        
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
        urllist=['http://abc1.com/', 'https://b.co/index.html']
        self.tgp.push('fractq', urllist, 'prod.com', 'stag.com')

        dumper=TaskWorker()
        dumper.open()
        dumper.make_queue('fractq')
        m,p,b = dumper.pullSingleMessage('fractq')
        
        self.assertTrue(json.loads(b)['urllist'] == urllist)
        self.assertTrue(json.loads(b)['src_ghost'] == 'prod.com')
        self.assertTrue(json.loads(b)['dst_ghost'] == 'stag.com')
        #self.assertTrue( b['urllist'] == urllist)
        logging.debug(b)
        

class test_FractWorker(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_sub_testgen(self):
        # publish testgen
        urllist=['https://space.ktmrmshk.com/', 'https://space.ktmrmshk.com/js/mobile.js']
        publisher = TestGenPublisher()
        publisher.push('fractq', urllist, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')

        ### spawn worker
        worker = FractWorker()
        worker.open()
        worker.addCallback('testgen', FractSub.sub_testgen)
        #worker.consume('fractq')
        worker.pullSingleMessage('fractq')
        
    def test_sub_testgen_with_dumper(self):
        # publish testgen
        urllist=['https://space.ktmrmshk.com/', 'https://space.ktmrmshk.com/js/mobile.js']
        publisher = TestGenPublisher()
        publisher.push('fractq', urllist, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')

        ### spawn worker
        worker = FractWorker()
        worker.open()

        def testcases_filedumper(testcases):
            with open('test_sub_testgen_with_dumper_out.json', 'w') as f:
                f.write('[')
                cnt=0
                for tc in testcases:
                    if cnt!=0:
                        f.write(',')
                    f.write('{}'.format(tc))
                    cnt+=1
                else:
                    f.write(']')

        worker.addCallback('testgen', FractSub.sub_testgen, testcases_filedumper)
        #worker.consume('fractq')
        worker.pullSingleMessage('fractq')
        
        # check
        with open('test_sub_testgen_with_dumper_out.json') as f:
            raw=f.read()
        j=json.loads(raw)
        self.assertTrue( len(j) == 2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()



