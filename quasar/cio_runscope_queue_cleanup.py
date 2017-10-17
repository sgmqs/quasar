import time

from .queue import QuasarQueue

class RunscopeQueue(QuasarQueue):

    def process_message(self, message_data):
        email = message_data['data']['data']['email_address']
        print("Email is {}.".format(email))
        if email.startswith('juy+runscope-register'):
            print("Email {} ack'd and cleared from queue.".format(email))
        else:
            print("Requeueing email {}.".format(email))
            self.pub_message(message_data)


queue = RunscopeQueue()

def main():
    queue.start_consume()
