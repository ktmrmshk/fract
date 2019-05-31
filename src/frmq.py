import pika, json
from functools import partial
from fract import *
from frase import *

class MQMan(object):
    def __init__(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

class RabbitMQMan(MQMan):
    def __init__(self):
        pass

    def open(self, host='localhost'):
        self.conn = pika.BlockingConnection( pika.ConnectionParameters(host))
        self.ch = self.conn.channel()

    def make_queue(self, queuename):
        self.ch.queue_declare(queue=queuename, durable=True)

    def close(self):
        self.conn.close()

class TaskPublisher(RabbitMQMan):
    def push(self, queuename, body):
        self.ch.basic_publish(exchange='', routing_key=queuename, body=body, properties=pika.BasicProperties(delivery_mode=2))

class TaskWorker(RabbitMQMan):
    def callback(self, ch, method, properties, body):
        'must implement in child class'
        pass

    def consume(self, queuename):
        self.ch.basic_qos(prefetch_count=1)
        self.ch.basic_consume(queue=queuename, on_message_callback=self.callback)
        self.ch.start_consuming()
    
    def pullSingleMessage(self, queuename):
        '''
        return (method, properties, body)
        '''
        return self.ch.basic_get(queue=queuename, auto_ack=True)

class SimpleDumpWorker(TaskWorker):
    def callback(self, ch, method, properties, body):
        logging.debug(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

class FractWorker(TaskWorker):
    def __init__(self):
        '''
        fract_sub = {'testgen': callback_for_testgen, 'run': callback_for_run}
        '''
        super(FractWorker, self).__init__()
        self.fract_sub = {}
    
    def addCallback(self, cmd, callback, dumper=None):
        '''
        callback: function(msg)
        dumper: output adaptor function
        '''
        self.fract_sub[cmd] = partial(callback, dumper=dumper)

    def callback(self, ch, method, properties, body):
        msg = json.loads(body)
        cmd = msg['cmd']
        self.fract_sub[cmd](msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def pullSingleMessage(self, queuename):
        method, properties, body = self.ch.basic_get(queue=queuename, auto_ack=True)
        
        msg = json.loads(body)
        cmd = msg['cmd']
        self.fract_sub[cmd](msg)
        self.ch.basic_ack(delivery_tag=method.delivery_tag)


class FractSub(object):
    @staticmethod
    def sub_testgen(msg, dumper=None):
        assert msg['cmd'] == 'testgen'
        logging.debug('sub_testgen: msg => {}'.format(msg))
        
        fg = FraseGen()
        fg._gen_from_urllist(msg['urllist'], msg['src_ghost'], msg['dst_ghost'], msg['headers'], msg['options'], msg['mode'])
        if dumper != None:
            dumper(fg.testcases)
        else:
            ### As a temporary output
            for tc in fg.testcases:
                logging.debug('sub_testgen: ret => {}'.format(tc))


class TestGenPublisher(object):
    '''
    testgen message: 
 {
    "cmd": "testgen",
    "urllist": [
        "https://abc.com/",
        "..."
    ],
    "headers": {
        "User-Agent": "iPhone",
        "Referer": "http://abc.com"
    },
    "options": {
        "ignore_case": true
    },
    "mode": {
        "strict_redirect_cacheability": false
    },
    "src_ghost" : "e13100.a.akamaiedge.net",
    "dst_ghost" : "e13100.a.akamaiedge-staging.net"
}        
    '''
    def __init__(self):
        self.tp = TaskPublisher()
        self.tp.open()

    def push(self, queuename, urllist, src_ghost, dst_ghost, headers={}, options={}, mode={}):
        #queuename='fractq'
        self.tp.make_queue(queuename)
        msg=dict()
        msg['cmd'] = 'testgen'
        msg['urllist'] = urllist
        msg['headers'] = headers
        msg['options'] = options
        msg['src_ghost'] = src_ghost
        msg['dst_ghost'] = dst_ghost
        msg['mode'] = mode
        self.tp.push(queuename, json.dumps(msg))
        #self.tp.push(queuename, msg)

