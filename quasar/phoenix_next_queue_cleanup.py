import time

from .queue import QuasarQueue


class PhoenixNextCleanupQueue(QuasarQueue):

    def process_message(self, message_data):
        try:
            event_type = message_data['data']['event_type']
            print("It's a C.IO event, republishing {}!".format(message_data['data']['event_id']))
            time.sleep(0.01)
            self.pub_message(message_data)
        except KeyError:
            print("Phoenix-next event, acking!")


queue = PhoenixNextCleanupQueue()


def main():
    queue.start_consume()
