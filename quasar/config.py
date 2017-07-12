import os
import sys

from types import SimpleNamespace

env = os.environ.get("ENV")
default = {
    "CAMPAIGN_ACTIVITY_TABLE": "table",
    "ROGUE_PROGRESS_TABLE": "rogue",
    "DS_ROGUE_API_KEY": "dummy",
    "ROGUE_URI": "http://uri",
    "MYSQL_HOST": "127.0.0.1",
    "MYSQL_PORT": 6603,
    "MYSQL_USER": "root",
    "MYSQL_PASSWORD": "password",
    "MYSQL_DATABASE": "quasar",
    "host": "127.0.0.1",
    "port": 6603,
    "user": "root",
    "pw": "password",
    "mc_user": "user",
    "mc_pw": "password",
    "ns_client_id": "123",
    "ns_client_secret": "secret",
    "AMQP_URI": "amqp://user:password@localhost:5672/vhost?query",
    "AMQP_QUEUE": "queue",
    "AMQP_EXCHANGE": "exchage",
    "MYSQL_TABLE": "customerio"

}

config = SimpleNamespace(**default)

if env == "PROD" or env == "STAGING":
    sys.path.append(os.environ.get("HOME"))
    import config as config
