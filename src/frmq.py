import pika, json
from fract import *
from frase import *

class MQMan(object):
    def __init__(self):
        pass


class RabbitMQMan(MQMan):
    def __init__(self, host='localhost'):
        self.conn = pika.BlockingConnection( pika.ConnectionParameters(host='localhost'))
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
    }
}        
    '''
    def __init__(self):
        self.tp = TaskPublisher()

    def push(self, urllist, headers={}, options={}, mode={}):
        queuename='testgen'
        self.tp.make_queue(queuename)
        msg=dict()
        msg['cmd'] = 'testgen'
        msg['urllist'] = urllist
        msg['headers'] = headers
        msg['options'] = options
        msg['mode'] = mode
        self.tp.push(queuename, json.dumps(msg))
        #self.tp.push(queuename, msg)

