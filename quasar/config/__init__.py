import os
import sys

from . import dev as config

env = os.environ['ENV']

if env == "PROD" or env == "STAGING":
    sys.path.append(os.environ.get("HOME"))
    import config as config
