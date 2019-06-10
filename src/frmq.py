import pika, json
from functools import partial
from fract import *
from frase import *
from fradb import *
from config import CONFIG
import socket, time


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

    def open(self, host=CONFIG['mq']['host'], port=CONFIG['mq']['port']):
#        while True:
#            try:
#                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                    s.connect((host,port))
#            except ConnectionRefusedError as e:
#                print(e)
#                print('...retry connect...')
#                time.sleep(2)
#                continue
#            else:
#                break
#
        self.conn = pika.BlockingConnection( pika.ConnectionParameters(host, port, connection_attempts=20))
        self.ch = self.conn.channel()

    def make_queue(self, queuename):
        self.qret = self.ch.queue_declare(queue=queuename, durable=True)

    def close(self):
        self.conn.close()

    def get_queue_size(self, queuename):
        ret = self.ch.queue_declare(queue=queuename, durable=True, passive=True)
        return ret.method.message_count

    def purge(self, queuename):
        self.make_queue(queuename)
        self.ch.queue_purge(queuename)

    def delete(self, queuename):
        self.make_queue(queuename)
        self.ch.queue_delete(queuename)

    def pull_single_msg(self, queuename):
        '''
        return (method, properties, body)
        '''
        return self.ch.basic_get(queue=queuename, auto_ack=True)


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
    
    def addCallback(self, cmd, callback):
        '''
        callback: function(msg)
        dumper: output adaptor function
        '''
        self.fract_sub[cmd] = partial(callback)

    def callback(self, ch, method, properties, body):
        msg = json.loads(body)
        cmd = msg['cmd']
        self.fract_sub[cmd](msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def pull_single_msg(self, queuename):
        method, properties, body = self.ch.basic_get(queue=queuename, auto_ack=True)
        
        msg = json.loads(body)
        cmd = msg['cmd']
        self.fract_sub[cmd](msg)
        self.ch.basic_ack(delivery_tag=method.delivery_tag)



class FractSubtask(object):
    @staticmethod
    def do_task(msg):
        pass

class Subtask_TestGen(FractSubtask):
    @staticmethod
    def do_task(msg):
        assert msg['cmd'] == 'testgen'
        logging.debug('sub_testgen: msg => {}'.format(msg))
        
        fg = FraseGen()
        fg._gen_from_urllist(msg['urllist'], msg['src_ghost'], msg['dst_ghost'], msg['headers'], msg['options'], msg['mode'])

        # export results to mongo
        mj=mongojson()
        mj.push_many(fg.testcases, msg['cmd'], msg['sessionid'], lambda i : i.query)

class Subtask_Run(FractSubtask):
    @staticmethod
    def do_task(msg):
        assert msg['cmd'] == 'run'
        logging.debug('sub_run: msg => {}'.format(msg))

        testcases = msg['testcases']
        fclient = FractClient(fract_suite_json=json.dumps(testcases) )
        fclient.run_suite()        

        # export results to mongo
        mj=mongojson()
        if len(fclient._result_suite) > 0:
            # resultl = list()
            # for node_result in fclient._result_suite:
            #     resultl.append(node_result.__str__())
            mj.push_many(fclient._result_suite, msg['cmd'], msg['sessionid'], lambda i : i.query)
        if len(fclient._failed_result_suite) > 0:
            # resultl = list()
            # for node_result in fclient._result_suite:
            #     resultl.append(node_result.__str__())
            mj.push_many(fclient._failed_result_suite, msg['cmd'], msg['sessionid'] + '_failed', lambda i : i.query)



'''
This Class is used only for testing. Don't use in production. 
'''
class TestGenPublisher(object):
    '''
    testgen message: 
 {
    "cmd": "testgen",
    "sessionid" : 20190430123121,
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

    def push(self, queuename, sessionid, urllist, src_ghost, dst_ghost, headers={}, options={}, mode={}):
        #queuename='fractq'
        self.tp.make_queue(queuename)
        msg=dict()
        msg['cmd'] = 'testgen'
        msg['urllist'] = urllist
        msg['sessionid'] = sessionid
        msg['headers'] = headers
        msg['options'] = options
        msg['src_ghost'] = src_ghost
        msg['dst_ghost'] = dst_ghost
        msg['mode'] = mode
        self.tp.push(queuename, json.dumps(msg))
        #self.tp.push(queuename, msg)


