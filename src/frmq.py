import pika

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

class SimpleDumpWorker(TaskWorker):
    def callback(self, ch, method, properties, body):
        print(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)



