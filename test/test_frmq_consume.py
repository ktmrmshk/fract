'''
$ export PYTHONPATH=`pwd`/src
$ docker run -d --rm -p5672:5672 -p8080:15672 rabbitmq:3-management

$ fraui -v workerup ...
'''


import unittest, json, logging, re
logging.basicConfig(level=logging.DEBUG)

from frmq import *
class test_TestGenPublisher(unittest.TestCase):
    def setUp(self):
        self.tgp = TestGenPublisher()

    def tearDown(self):
        pass

    def test_push_for_workertest10(self):
        # publish testgen
        for i in range(10):
            urllist=['https://space.ktmrmshk.com/', 'https://space.ktmrmshk.com/js/mobile.js']
            publisher = TestGenPublisher()
            publisher.push('fractq', urllist, 'e13100.a.akamaiedge.net', 'e13100.a.akamaiedge-staging.net')



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
