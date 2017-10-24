from .config import config
from .database import Database
from .queue import QuasarQueue

import json
import time

db = Database()

class CioQueue(QuasarQueue):

    def process_message(self, message_data):
        print("Inserting record.")
        query = ''.join(("INSERT IGNORE INTO {} (meta, data) VALUES ('{}', "
                         "'{}')")).format(config.CIO_EVENT_TABLE,
                                          json.dumps(message_data['meta']),
                                          json.dumps(message_data['data']))
        print(query)
        db.query(query)
        time.sleep(0.1)
        self.pub_message(message_data)


queue = CioQueue()


def main():
    queue.start_consume()
