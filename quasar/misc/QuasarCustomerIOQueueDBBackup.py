from datetime import datetime
import json
import logging
import MySQLdb
import re

import pika

from .config import config

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
                 amqp_exchange=config.AMQP_EXCHANGE,
                 mysql_host=config.MYSQL_HOST,
                 mysql_port=config.MYSQL_PORT,
                 mysql_user=config.MYSQL_USER,
                 mysql_password=config.MYSQL_PASSWORD,
                 mysql_database=config.MYSQL_DATABASE,
                 mysql_table=config.MYSQL_TABLE,
                 blink_backup_table=config.BLINK_BACKUP_TABLE):
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
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database
        self.mysql_table = mysql_table
        self.blink_backup_table = blink_backup_table

        self.mysql_connection = self._create_connection(mysql_host,
                                                        mysql_port,
                                                        mysql_user,
                                                        mysql_password,
                                                        mysql_database)
        self.mysql_cursor = self.mysql_connection.cursor()

    def start(self):
        """Kick off consumer process to ingest messages.

        Stays active until killed by keyboard interrupt (Ctrl-c or equivalent).
        """
        logging.info("Starting Blink consumer...")
        self.channel.basic_consume(self.on_message, self.amqp_queue)
        try:
            self.channel.start_consuming()
            logging.info("Blink consumer started.")
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.connection.close()

    def on_message(self, channel, method_frame, header_frame, body):
        """Parse message once one arrives in queue.

        The body of the message is decoded via JSON decoder. As long as the
        queue isn't empty, the messages are parsed and processed by the
        _process_message private method which inserts the records in the
        Quasar DB and discards them if they're not type sub or sunsub.
        """
        message_data = self._body_decode(body)
        logging.info("[Message {0}]: Received."
                     "".format(message_data['meta']['request_id']))

        return self._process_message(method_frame, message_data)

    def _process_message(self, method_frame, message_data):
        logging.info("[Message {0}] Processing message..."
                     "".format(message_data['meta']['request_id']))
        message_type = self._message_type(message_data)

        if message_type:
            email_address = message_data['data']['data']['email_address']
            northstar_id = self.mysql_query("SELECT northstar_id "
                                            "FROM {1} WHERE email = \"{0}\";"
                                            "".format(email_address,
                                                      self.mysql_table))
            if self._bare_str(northstar_id[1]) != "":
                logging.info("Procesing Northstar ID: {0}."
                             "".format(northstar_id[1]))
                self.insert_record(message_data,
                                   self._bare_str(northstar_id[1]),
                                   message_type)
                self.channel.basic_ack(method_frame.delivery_tag)
                logging.info("[Message {0}] Message processed."
                             "".format(message_data['meta']['request_id']))
                return True
            else:
                logging.info("[Message {0}] Message failed. "
                             "Putting message content in backup table."
                             "".format(message_data['meta']['request_id']))
                self.backup_results = self.backup_record(message_data,
                                                         message_type)
                self.channel.basic_ack(method_frame.delivery_tag)
                logging.info("Backed up email {0}.".format(email_address))
        else:
            self.channel.basic_ack(method_frame.delivery_tag)
            logging.info("[Message {0}] Message not sub or unsub. Dropping."
                         "".format(message_data['meta']['request_id']))

    def _create_connection(self, mysql_host, mysql_port, mysql_user,
                           mysql_password, mysql_database):
        try:
            conn = MySQLdb.connect(host=mysql_host,
                                   port=mysql_port,
                                   user=mysql_user,
                                   passwd=mysql_password,
                                   db=mysql_database,
                                   use_unicode=True,
                                   charset='utf8')
        except MySQLdb.InterfaceError as e:
            conn = False
            raise QuasarQueueException(e)
        finally:
            return conn

    def _create_disconnect(self):
        self.mysql_cursor.close()
        return self.mysql_connection()

    def _body_decode(self, body):
        message_response = body.decode()

        try:
            return json.loads(message_response)
        except Exception as e:
            raise QuasarQueueException(e)

    def _body_encode(self, message_data):
        return json.dumps(message_data)

    def _message_type(self, message_data):
        message_type = message_data['data']['event_type']
        if message_type == 'customer_subscribed':
            customer_io_subscription_status = 'subscribed'
            return customer_io_subscription_status
        elif message_type == 'customer_unsubscribed':
            customer_io_subscription_status = 'unsubscribed'
            return customer_io_subscription_status
        else:
            return False

    def _bare_str(self, base_value):
        """Convert value to string and strips special characters."""
        base_string = str(base_value)
        strip_special_chars = re.sub(r'[()<>/"\,\'\\]', '', base_string)
        return str(strip_special_chars)

    def mysql_query(self, query):
        """Parse and run DB query.

        On error, raise exception and log why.
        """
        try:
            self.mysql_cursor.execute(query)
            self.mysql_connection.commit()
            results = self.mysql_cursor.fetchall()
            return True, results
        except MySQLdb.DatabaseError as e:
            raise QuasarQueueException(e)

    def insert_record(self, message_object, northstar_id, message_type):
        """Insert email and timestamp event into Quasar DB.

        Using derived Northstar ID associated with e-mail address the email
        status of subscribed or unsubscribed is put in to the Quasar DB along
        with the recorded timestamp.
        """
        customer_io_subscription_status = message_type
        customer_io_subscription_timestamp = (
            datetime.fromtimestamp(
                message_object['data']['timestamp']).isoformat())
        query_status = self.mysql_query("UPDATE {3} SET "
                                        "customer_io_subscription_status = "
                                        "\"{0}\", "
                                        "customer_io_subscription_timestamp = "
                                        "\"{1}\" WHERE northstar_id = \"{2}\""
                                        "".format(
                                            customer_io_subscription_status,
                                            customer_io_subscription_timestamp,
                                            northstar_id, self.mysql_table))

        return query_status[0]

    def backup_record(self, message_object, message_type):
        """Backup email, Customer IO Status, and timestamp into Quasar DB.

        If record doesn't have Northstar ID when consumed from Customer.io
        queue, or can't be parsed for some other reason, this records the
        pertinent data into a backup DB table.

        Rob Spectre originally used an internal queueing mechanism, but with
        live traffic, there's some errors that were generated I couldn't get
        through in time for our deadline, hence this placeholder class.
        """
        email = message_object['data']['data']['email_address']
        customer_io_subscription_status = message_type
        customer_io_subscription_timestamp = (
            datetime.fromtimestamp(
                message_object['data']['timestamp']).isoformat())
        query_status = self.mysql_query("REPLACE INTO {3} "
                                        "VALUES (\"{0}\", \"{1}\", "
                                        "\"{2}\")".format(
                                            email,
                                            customer_io_subscription_status,
                                            customer_io_subscription_timestamp,
                                            self.blink_backup_table))

        return query_status[0]


class QuasarQueueException(Exception):
    """Donated exception handling code by Rob Spectre.

    This logs any error message we need to pass in.
    """

    def __init__(self, message):
        """Log errors with formatted messaging."""
        logging.error("ERROR: {0}".format(message))
        pass
