import json

from .database import Database
from .queue import QuasarQueue
from .utils import unixtime_to_isotime as u2i
from .utils import strip_str


db = Database()


class CioQueue(QuasarQueue):

    def process_message(self, message_data):
        print(''.join(("Processing C.IO event id: "
                       "{}.")).format(message_data['data']['event_id']))
        log_event(db, message_data)
        customer_event(db, message_data)
        event_type = message_data['data']['event_type']
        if (event_type == 'customer_subscribed' or
                event_type == 'customer_unsubscribed'):
            legacy_sub_unsub(db, message_data)


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
    if message_data['data']['event_type'] == 'customer_subscribed':
        status = 'subscribed'
    else:
        status = 'unsubscribed'
    if strip_str(nsid) != "":
        db.query_str(''.join(("UPDATE quasar.users SET "
                              "customer_io_subscription_status = %s, "
                              "customer_io_subscription_timestamp = %s"
                              " WHERE northstar_id = %s")),
                     (status,
                      u2i(message_data['data']['timestamp']),
                      strip_str(nsid)))
    else:
        db.query_str("INSERT INTO cio.legacy_sub_backlog VALUES (%s, %s, %s)",
                     (status,
                      u2i(message_data['data']['timestamp']),
                      message_data['data']['data']['customer_id']))


def legacy_update_users():
    backlog = db.query("SELECT * FROM cio.legacy_sub_backlog")
    for entry in backlog:
        nsid = db.query_str(''.join(("SELECT northstar_id FROM quasar.users "
                                     "WHERE northstar_id = %s")),
                            (entry[2],))
        if strip_str(nsid) != "":
            db.query_str(''.join(("UPDATE quasar.users SET "
                                  "customer_io_subscription_status = %s, "
                                  "customer_io_subscription_timestamp = %s "
                                  "WHERE northstar_id = %s")),
                         (entry[0], entry[1], entry[2]))
            db.query_str(''.join(("DELETE FROM cio.legacy_sub_backlog "
                                  "WHERE northstar_id = %s")),
                         (entry[2],))
            print("Northstar ID {} c.io status updated.".format(entry[2]))
        else:
            print("Northstar ID {} staying in backlog.".format(entry[2]))


queue = CioQueue()


def main():
    queue.start_consume()


def legacy_cio_backfill():
    legacy_update_users()
