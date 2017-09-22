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

def main():
    log_format = "%(asctime)s - %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)

    testQuasarQueue = QuasarQueue()
    testQuasarQueue.start()

if __name__ == "__main__":
    main()

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
            if strip_str(northstar_id[1]) != "":
                query_results = self.insert_record(message_data,
                                                   strip_str(
                                                       northstar_id[1]),
                                                   message_type)
                self.channel.basic_ack(method_frame.delivery_tag)
                logging.info("[Message {0}] Message processed."
                             "".format(message_data['meta']['request_id']))
                return True
            elif self.retry_counter <= 1000:
                self.channel.basic_publish(self.amqp_exchange, self.amqp_queue,
                                           self._body_encode(message_data),
                                           pika.BasicProperties(
                                               content_type='application/json',
                                               delivery_mode=2))
                self.channel.basic_ack(method_frame.delivery_tag)
                self.retry_counter += 1
                logging.info("[Message {0}] Message failed, requeueing "
                             "message and trying the next one."
                             "".format(message_data['meta']['request_id']))
                logging.info("Retry counter at {0}."
                             "".format(self.retry_counter))
                time.sleep(0.25)
            else:
                logging.info("Max retry counter reached, exiting for now.")
                sys.exit(0)
        else:
            self.channel.basic_ack(method_frame.delivery_tag)
            logging.info("[Message {0}] Message not sub or unsub. Dropping."
                         "".format(message_data['meta']['request_id']))