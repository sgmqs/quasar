import json
import time

from .config import config
from .database import Database
from .queue import QuasarQueue
from .utils import unixtime_to_isotime as u2i
from .utils import strip_str as ss


db = Database()

class CioQueue(QuasarQueue):

    def process_message(self, message_data):
        print("Inserting record.")
        log_event(db, message_data)
        customer_event(db, message_data)
        if (message_data['data']['event_type'] == 'customer_subscribed' or
            message_data['data']['event_type'] == 'customer_unsubscribed'):
            legacy_sub_unsub(db, message_data)
        self.pub_message(message_data)
        time.sleep(1)


def log_event(db, message_data):
    db.query_str(''.join(("INSERT IGNORE INTO cio.event_log"
                          "(meta, data) VALUES (%s, %s)")),
                 (json.dumps(message_data['meta']), 
                  json.dumps(message_data['data'])))


def customer_event(db, message_data):
    db.query_str("INSERT INTO cio.customer_event VALUES (%s, %s, %s, %s)",
                 (message_data['data']['event_type'],
                  message_data['data']['event_id'],
                  u2i(message_data['data']['timestamp']),
                  message_data['data']['data']['customer_id']))

def legacy_sub_unsub(db, message_data):
    nsid = db.query_str(''.join(("SELECT northstar_id FROM quasar.users "
                              "WHERE email = %s")),
                          (message_data['data']['data']['email_address'],))
    print("Northstar ID is :{}".format(ss(nsid)))
    if message_data['data']['event_type'] == 'customer_subscribed':
        status = 'subscribed'
    else:
        status = 'unsubscribed'
    if ss(nsid) != "":
        db.query_str(''.join(("UPDATE quasar.users SET "
                              "customer_io_subscription_status = %s, "
                              "customer_io_subscription_timestamp = %s"
                              " WHERE northstar_id = %s")),
                     (status,
                      u2i(message_data['data']['timestamp']),
                      ss(nsid)))
    else:
        db.query_str("INSERT INTO cio.legacy_sub_backlog VALUES (%s, %s, %s)",
                     (status,
                      u2i(message_data['data']['timestamp']),
                      message_data['data']['data']['customer_id']))



queue = CioQueue()


def main():
    queue.start_consume()
