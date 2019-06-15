import pika, json
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

    def open(self, host, port=5672, connection_attempts=20):
        self.conn = pika.BlockingConnection( pika.ConnectionParameters(host, port, connection_attempts=connection_attempts))
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
    def __init__(self, host, port):
        self.tp = TaskPublisher()
        self.tp.open(host, port)

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


