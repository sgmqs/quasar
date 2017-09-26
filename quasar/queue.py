from datetime import datetime
import json
import logging
import re
import sys
import time

import pika

from .config import config
from .utils import strip_str, QuasarException

log_format = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


class QuasarQueue:
    """This class handles queue tasks for Blink Quasar Customer.io Queue.

    This first class is to MVP our migration to Customer.io using queueing
    in our ETL pipeline, a first for DS.

    Basic setup for now is assuming only connecting to a single queue.
    For future version, re-factoring so this class handles all the queue
    connection niceties and can connect to any queue URI using pika is
    probably better.
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
            self.channel.stop_consuming()
        self.connection.close()


    def stop_consume(self, tag="quasar_consumer"):
        self.channel.basic_cancel(tag)


    def test_consumer(self, tag="test_consumer"):
        logging.info("Starting {0} test consumer for one message.")
        self.channel(basic_consume(self.on_test_message, self.amqp_queue,
                                   consumer_tag=tag))
        stop_consume(tag)

    def test_on_message(self, channel, method_frame, header_frame, body, process_message):
        self.channel.basic_publish(self.amqp_exchange, self.amqp_queue,
                                           self._body_encode(message_data),
                                           pika.BasicProperties(
                                               content_type='application/json',
                                               delivery_mode=2))
        message_data = self._body_decode(body)
        print("Decoding one message.")
        print("Message contents is: {}").format(body)
        self.channel.basic_ack(method_frame.delivery_tag)
        print("Message republished to queue.")
        sys.exit(0)

    @on_message
    def test_on_message():
        pub_message(self, message_data)


        
    def on_message(self, channel, method_frame, header_frame, body, process_message):
    def on_message(process_message):
    """Decorator to handle messages ingested from queue.

    Body is automatically JSON decoded and message ID is logged.
    """
        def parse_message(*args, **kwargs):
            message_data = self._body_decode(body)
            logging.info("[Message {0}]: Received."
                "".format(message_data['meta']['request_id']))
            process_message(message_data)
        return parse_message

    def ack_message(self, method_frame):
        self.channel.basic_ack(method_frame.delivery_tag)

    def pub_message(self, message_data):
        self.channel.basic_publish(self.amqp_exchange, self.amqp_queue,
                                   self._body_encode(message_data),
                                   pika.BasicProperties(
                                    content_type='application/json',
                                    delivery_mode=2))

    def _body_decode(self, body):
        message_response = body.decode()
        try:
            return json.loads(message_response)
        except Exception as e:
            raise QuasarException(e)

    def _body_encode(self, message_data):
        return json.dumps(message_data)
