import logging
import re
import time

# DoSomething Helper Functions - Code Reused Across Lots of our ETL Scripts

# String Parser


def strip_str(base_value):
    """Convert value to string and strips special characters.

    None becomes empty string
    """
    base_string = str(base_value)
    if base_string == 'None':
        return ''
    else:
        strip_special_chars = re.sub(r'[()<>/"\,\'\\]', '', base_string)
        return str(strip_special_chars)


class Duration:
    """Simple duration tracker.

    Object starts tracking time when instantiated, and then when
    duration function is called records and prints then returns
    duration time in seconds.
    """
    def __init__(self):
        start_time = time.time()

    def duration(self):
        run_time = self.start_time - time.time()
        print('Duration in seconds: ', run_time)
        return run_time

class QuasarException(Exception):
    """Donated exception handling code by Rob Spectre.

    This logs any error message we need to pass in.
    """

    def __init__(self, message):
        """Log errors with formatted messaging."""
        logging.error("ERROR: {0}".format(message))
        pass

