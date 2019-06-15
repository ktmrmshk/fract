import pika, json
from functools import partial
from fract import *
from frase import *
from fradb import *
from frmq import *
import socket, time


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


