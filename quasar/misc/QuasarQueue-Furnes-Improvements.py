import pika

import json


class BlinkQueue:
    """ This class handles queue tasks for Blink Quasar Customer.io Queue.

    This first class is to MVP our migration to Customer.io using queueing
    in our ETL pipeline, a first for DS.

    Basic setup for now is assuming only connecting to a single queue.
    For future version, re-factoring so this class handles all the queue
    connection niceties and can connect to any queue URI using pika is
    probably better.
    """

    def __init__(self, queue_url, queue_name):
        self.params = pika.URLParameters(queue_url)
        self.params.socket_timeout = 5
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue_name, durable=True)
        self.queue_name = queue_name

    def handleMessage(self, channel, method_frame, header_frame, body):
        self.handler(self, channel, method_frame, header_frame, body)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def getMessages(self, on_message):
        self.handler = on_message
        self.channel.basic_consume(self.handleMessage, self.queue_name)

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.connection.close()

    def getOneMessage(self):
        method_frame, header_frame, body = (
            self.channel.basic_get(self.queue_name))
        if method_frame:
            message_response = body.decode()
            message_data = json.loads(message_response)
            # print(message_data['data']['data']['email_address'])
            print(message_data)
        else:
            print("No messages in queue!")
