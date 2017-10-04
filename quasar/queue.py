import json
import logging
import time

import pika

from .config import config
from .utils import QuasarException

log_format = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


class QuasarQueue:
    """Basic queue handling class for Quasar.

    This class sets up a connection to a queue, and provides the basic
    building blocks for handing queue messages and consumer start/stop.

    It's most direct function is to have the on_message method over-ridden
    by children classes to specify exactly how to handle each message.
    """

    def __init__(self,
                 amqp_uri=config.AMQP_URI,
                 amqp_queue=config.AMQP_QUEUE,
                 amqp_exchange=config.AMQP_EXCHANGE):
        """Setup MySQL and AMQP connections and credentials."""
        self.params = pika.URLParameters(amqp_uri)
        self.params.socket_timeout = 5
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=100)
        self.channel.queue_declare(amqp_queue, durable=True)

        self.amqp_uri = amqp_uri
        self.amqp_exchange = amqp_exchange
        self.amqp_queue = amqp_queue
        self.retry_counter = 0

    def start_consume(self, tag="quasar_consumer"):
        """Kick off consumer process to ingest messages.

        Stays active until killed by keyboard interrupt (Ctrl-c or equivalent).
        """
        logging.info("Starting {0} consumer..."
                     "".format(self.amqp_queue))
        self.channel.basic_consume(self.on_message, self.amqp_queue,
                                   consumer_tag=tag)
        try:
            self.channel.start_consuming()
            logging.info("{0} consumer started.".format(self.amqp_queue))
        except KeyboardInterrupt:
            self.stop_consume()
        self.connection.close()

    def stop_consume(self, tag="quasar_consumer"):
        self.channel.basic_cancel(tag)

    def on_message(self, channel, method_frame, header_frame,
                   body, output="true"):
        message_data = self.body_decode(body)
        if output == "true":
            print("Message received.")
            print("Message method_frame is {}".format(method_frame))
            print("Message header_frame is {}".format(header_frame))
            print("Message body is {}".format(body))
        print("Republishing message.")
        self.pub_message(message_data)
        print("Acking message.")
        self.ack_message(method_frame)
        print("Original message ack'd.")
        time.sleep(0.5)

    def ack_message(self, method_frame):
        self.channel.basic_ack(method_frame.delivery_tag)

    def pub_message(self, message_data):
        self.channel.basic_publish(self.amqp_exchange, self.amqp_queue,
                                   self.body_encode(message_data),
                                   pika.BasicProperties(
                                    content_type='application/json',
                                    delivery_mode=2))

    def body_decode(self, body):
        message_response = body.decode()
        try:
            return json.loads(message_response)
        except Exception as e:
            raise QuasarException(e)

    def body_encode(self, message_data):
        return json.dumps(message_data)
